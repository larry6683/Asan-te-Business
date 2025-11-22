from config.config import Config
from sqlalchemy import func
from src.public.tables import (
    Beneficiary, BeneficiarySize, AppUser, BeneficiaryUser, BeneficiaryUserPermissionRole,
    Cause, BeneficiaryCausePreference, CausePreferenceRank,
    BeneficiaryShop, BeneficiarySocialMedia  # ✅ ADDED TABLES
)
from database.db_manager import DatabaseManager
from converters.beneficiary_converter import BeneficiaryConverter
from utils.error_handler import ErrorHandler
from utils.validator import Validator
from utils.cause_mapper import CauseMapper
from codegen.beneficiary.beneficiary_pb2 import (
    GetBeneficiaryRequest, GetBeneficiaryResponse,
    GetBeneficiaryByUserEmailRequest, GetBeneficiaryByUserEmailResponse,
    CreateBeneficiaryRequest, CreateBeneficiaryResponse,
    Beneficiary as ProtoBeneficiary, Cause as ProtoCause # ✅ ADDED Cause Alias
)
from codegen.beneficiary.beneficiary_pb2_grpc import BeneficiaryServiceServicer

class BeneficiaryService(BeneficiaryServiceServicer):
    
    # ✅ HELPER: Map Database Object -> Proto Message
    def _map_to_proto(self, session, domain_beneficiary):
        # 1. Shop URL
        shop = session.query(BeneficiaryShop).filter(
            BeneficiaryShop.beneficiary_id == domain_beneficiary.id
        ).first()
        shop_url = shop.shop_url if shop else ""

        # 2. Social Media Links
        socials = session.query(BeneficiarySocialMedia).filter(
            BeneficiarySocialMedia.beneficiary_id == domain_beneficiary.id
        ).all()
        social_links = [s.social_media_link for s in socials] if socials else []

        # 3. Causes with Ranks
        cause_prefs = session.query(BeneficiaryCausePreference).filter(
            BeneficiaryCausePreference.beneficiary_id == domain_beneficiary.id
        ).all()
        
        proto_causes = []
        for pref in cause_prefs:
            cause_rec = session.query(Cause).filter(Cause.cause_id == pref.cause_id).first()
            rank_rec = session.query(CausePreferenceRank).filter(
                CausePreferenceRank.cause_preference_rank_id == pref.cause_preference_rank_id
            ).first()
            
            if cause_rec:
                proto_causes.append(ProtoCause(
                    name=cause_rec.cause_name,
                    rank=rank_rec.cause_preference_rank_name if rank_rec else "UNRANKED"
                ))

        return ProtoBeneficiary(
            id=domain_beneficiary.id,
            beneficiary_name=domain_beneficiary.beneficiary_name,
            email=domain_beneficiary.email,
            website_url=domain_beneficiary.website_url,
            phone_number=domain_beneficiary.phone_number,
            location_city=domain_beneficiary.location_city,
            location_state=domain_beneficiary.location_state,
            ein=domain_beneficiary.ein,
            beneficiary_description=domain_beneficiary.beneficiary_description,
            beneficiary_size=BeneficiaryConverter.size_to_string(domain_beneficiary.beneficiary_size),
            shop_url=shop_url,              # ✅ New Field
            social_media_links=social_links, # ✅ New Field
            causes=proto_causes             # ✅ New Field
        )

    def GetBeneficiary(self, request: GetBeneficiaryRequest, context):
        response = GetBeneficiaryResponse()
        
        try:
            if not Validator.is_not_empty(request.beneficiary_id):
                response.errors.append(ErrorHandler.invalid_parameter('beneficiary_id'))
                return response
            
            with DatabaseManager.get_session() as session:
                db_beneficiary = session.query(Beneficiary).filter(
                    Beneficiary.beneficiary_id == request.beneficiary_id
                ).first()
                
                if not db_beneficiary:
                    response.errors.append(
                        ErrorHandler.not_found('Beneficiary', request.beneficiary_id)
                    )
                    return response
                
                domain_beneficiary = BeneficiaryConverter.to_domain(db_beneficiary)
                # ✅ Use Helper
                response.beneficiary.CopyFrom(self._map_to_proto(session, domain_beneficiary))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetBeneficiary: {e}")
            import traceback
            traceback.print_exc()
        
        return response

    def GetBeneficiaryByUserEmail(self, request: GetBeneficiaryByUserEmailRequest, context):
        response = GetBeneficiaryByUserEmailResponse()
        response.has_beneficiary = False
        
        try:
            if not Validator.is_valid_email(request.user_email):
                response.errors.append(ErrorHandler.invalid_parameter('user_email'))
                return response
            
            with DatabaseManager.get_session() as session:
                db_beneficiary = session.query(Beneficiary).join(
                    BeneficiaryUser, Beneficiary.beneficiary_id == BeneficiaryUser.beneficiary_id
                ).join(
                    AppUser, BeneficiaryUser.app_user_id == AppUser.app_user_id
                ).filter(
                    func.lower(AppUser.email) == func.lower(request.user_email)
                ).first()
                
                if db_beneficiary:
                    response.has_beneficiary = True
                    domain_beneficiary = BeneficiaryConverter.to_domain(db_beneficiary)
                    # ✅ Use Helper
                    response.beneficiary.CopyFrom(self._map_to_proto(session, domain_beneficiary))
                    print(f"✅ Found beneficiary for user {request.user_email}")
                else:
                    print(f"ℹ️ No beneficiary found for user {request.user_email}")
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetBeneficiaryByUserEmail: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def CreateBeneficiary(self, request: CreateBeneficiaryRequest, context):
        response = CreateBeneficiaryResponse()
        
        try:
            # Validate
            errors = []
            if not Validator.is_not_empty(request.beneficiary_name):
                errors.append(ErrorHandler.invalid_parameter('beneficiary_name'))
            if not Validator.is_valid_email(request.email):
                errors.append(ErrorHandler.invalid_parameter('email'))
            if not Validator.is_not_empty(request.location_city):
                errors.append(ErrorHandler.invalid_parameter('location_city'))
            if not Validator.is_not_empty(request.location_state):
                errors.append(ErrorHandler.invalid_parameter('location_state'))
            if request.beneficiary_size and not Validator.is_valid_size(request.beneficiary_size):
                errors.append(ErrorHandler.invalid_parameter('beneficiary_size'))
            
            if errors:
                response.errors.extend(errors)
                return response
            
            with DatabaseManager.get_session() as session:
                # Check duplicates
                existing_email = session.query(Beneficiary).filter(
                    func.lower(Beneficiary.email) == func.lower(request.email)
                ).first()
                
                if existing_email:
                    response.errors.append(
                        ErrorHandler.already_exists('Beneficiary', 'email', request.email)
                    )
                    return response
                
                existing_name = session.query(Beneficiary).filter(
                    func.lower(Beneficiary.beneficiary_name) == func.lower(request.beneficiary_name)
                ).first()
                
                if existing_name:
                    response.errors.append(
                        ErrorHandler.already_exists('Beneficiary', 'name', request.beneficiary_name)
                    )
                    return response
                
                # Get beneficiary size
                size_code = BeneficiaryConverter.size_to_code(
                    request.beneficiary_size if request.beneficiary_size else 'SMALL'
                )
                beneficiary_size = session.query(BeneficiarySize).filter(
                    BeneficiarySize.code == size_code
                ).first()
                
                # Create beneficiary
                new_beneficiary = Beneficiary(
                    beneficiary_name=request.beneficiary_name,
                    email=request.email,
                    website_url=request.website_url or None,
                    phone_number=request.phone_number or None,
                    location_city=request.location_city,
                    location_state=request.location_state,
                    ein=request.ein or None,
                    beneficiary_description=request.beneficiary_description or '',
                    beneficiary_size_id=beneficiary_size.beneficiary_size_id
                )
                
                session.add(new_beneficiary)
                session.flush()

                # ✅ SAVE SHOP URL
                if request.shop_url:
                    new_shop = BeneficiaryShop(
                        beneficiary_id=new_beneficiary.beneficiary_id,
                        shop_url=request.shop_url
                    )
                    session.add(new_shop)
                    print(f"🛍️ Shop URL saved: {request.shop_url}")

                # ✅ SAVE SOCIAL MEDIA
                if request.social_media_links:
                    for link in request.social_media_links:
                        if link.strip():
                            new_social = BeneficiarySocialMedia(
                                beneficiary_id=new_beneficiary.beneficiary_id,
                                social_media_link=link.strip()
                            )
                            session.add(new_social)
                    print(f"📱 Saved {len(request.social_media_links)} social media links")
                
                # Link user if provided
                if request.user_email:
                    user = session.query(AppUser).filter(
                        func.lower(AppUser.email) == func.lower(request.user_email)
                    ).first()
                    
                    if user:
                        admin_role = session.query(BeneficiaryUserPermissionRole).filter(
                            BeneficiaryUserPermissionRole.code == 1
                        ).first()
                        
                        if admin_role:
                            beneficiary_user = BeneficiaryUser(
                                beneficiary_id=new_beneficiary.beneficiary_id,
                                app_user_id=user.app_user_id,
                                beneficiary_user_permission_role_id=admin_role.beneficiary_user_permission_role_id
                            )
                            session.add(beneficiary_user)
                
                # Create Cause Preferences
                if hasattr(request, 'cause_codes') and request.cause_codes:
                    print(f"📥 Received {len(request.cause_codes)} cause codes for beneficiary")
                    primary_rank = session.query(CausePreferenceRank).filter(CausePreferenceRank.code == 2).first()
                    
                    if primary_rank:
                        for enum_value in request.cause_codes:
                            db_cause_name = CauseMapper.enum_to_db_name(enum_value)
                            cause = session.query(Cause).filter(Cause.cause_name == db_cause_name).first()
                            
                            if cause:
                                cause_pref = BeneficiaryCausePreference(
                                    beneficiary_id=new_beneficiary.beneficiary_id,
                                    cause_id=cause.cause_id,
                                    cause_preference_rank_id=primary_rank.cause_preference_rank_id
                                )
                                session.add(cause_pref)
                
                # Convert to response using Helper
                domain_beneficiary = BeneficiaryConverter.to_domain(new_beneficiary)
                response.beneficiary.CopyFrom(self._map_to_proto(session, domain_beneficiary))
                
                print(f"✅ Beneficiary created successfully with ID: {new_beneficiary.beneficiary_id}")
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"❌ Error in CreateBeneficiary: {e}")
            import traceback
            traceback.print_exc()
        
        return response