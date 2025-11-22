from config.config import Config
from sqlalchemy import func
from src.public.tables import (
    Business, BusinessSize, AppUser, BusinessUser, BusinessUserPermissionRole,
    Cause, BusinessCausePreference, CausePreferenceRank,
    BusinessShop, BusinessSocialMedia  # ✅ ADDED TABLES
)
from database.db_manager import DatabaseManager
from converters.business_converter import BusinessConverter
from utils.error_handler import ErrorHandler
from utils.validator import Validator
from utils.cause_mapper import CauseMapper
from codegen.business.business_pb2 import (
    GetBusinessRequest, GetBusinessResponse,
    GetBusinessByUserEmailRequest, GetBusinessByUserEmailResponse,
    CreateBusinessRequest, CreateBusinessResponse,
    Business as ProtoBusiness, Cause as ProtoCause # ✅ ADDED Cause Alias
)
from codegen.business.business_pb2_grpc import BusinessServiceServicer

class BusinessService(BusinessServiceServicer):
    
    # ✅ HELPER: Map Database Object -> Proto Message (Including new fields)
    def _map_to_proto(self, session, domain_business):
        # 1. Get Shop URL
        shop = session.query(BusinessShop).filter(
            BusinessShop.business_id == domain_business.id
        ).first()
        shop_url = shop.shop_url if shop else ""

        # 2. Get Social Media Links
        socials = session.query(BusinessSocialMedia).filter(
            BusinessSocialMedia.business_id == domain_business.id
        ).all()
        social_links = [s.social_media_link for s in socials] if socials else []

        # 3. Get Causes with Ranks
        cause_prefs = session.query(BusinessCausePreference).filter(
            BusinessCausePreference.business_id == domain_business.id
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

        return ProtoBusiness(
            id=domain_business.id,
            business_name=domain_business.business_name,
            email=domain_business.email,
            website_url=domain_business.website_url,
            phone_number=domain_business.phone_number,
            location_city=domain_business.location_city,
            location_state=domain_business.location_state,
            ein=domain_business.ein,
            business_description=domain_business.business_description,
            business_size=BusinessConverter.size_to_string(domain_business.business_size),
            shop_url=shop_url,              # ✅ New Field
            social_media_links=social_links, # ✅ New Field
            causes=proto_causes             # ✅ New Field
        )

    def GetBusiness(self, request: GetBusinessRequest, context):
        response = GetBusinessResponse()
        
        try:
            if not Validator.is_not_empty(request.business_id):
                response.errors.append(ErrorHandler.invalid_parameter('business_id'))
                return response
            
            with DatabaseManager.get_session() as session:
                db_business = session.query(Business).filter(
                    Business.business_id == request.business_id
                ).first()
                
                if not db_business:
                    response.errors.append(
                        ErrorHandler.not_found('Business', request.business_id)
                    )
                    return response
                
                domain_business = BusinessConverter.to_domain(db_business)
                # ✅ Use Helper
                response.business.CopyFrom(self._map_to_proto(session, domain_business))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetBusiness: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def GetBusinessByUserEmail(self, request: GetBusinessByUserEmailRequest, context):
        response = GetBusinessByUserEmailResponse()
        response.has_business = False
        
        try:
            if not Validator.is_valid_email(request.user_email):
                response.errors.append(ErrorHandler.invalid_parameter('user_email'))
                return response
            
            with DatabaseManager.get_session() as session:
                db_business = session.query(Business).join(
                    BusinessUser, Business.business_id == BusinessUser.business_id
                ).join(
                    AppUser, BusinessUser.app_user_id == AppUser.app_user_id
                ).filter(
                    func.lower(AppUser.email) == func.lower(request.user_email)
                ).first()
                
                if db_business:
                    response.has_business = True
                    domain_business = BusinessConverter.to_domain(db_business)
                    # ✅ Use Helper
                    response.business.CopyFrom(self._map_to_proto(session, domain_business))
                    print(f"✅ Found business for user {request.user_email}: {db_business.business_name}")
                else:
                    response.has_business = False
                    print(f"ℹ️ No business found for user {request.user_email}")
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"❌ Error in GetBusinessByUserEmail: {e}")
            import traceback
            traceback.print_exc()
        
        return response
    
    def CreateBusiness(self, request: CreateBusinessRequest, context):
        response = CreateBusinessResponse()
        
        try:
            # Validate
            errors = []
            if not Validator.is_not_empty(request.business_name):
                errors.append(ErrorHandler.invalid_parameter('business_name'))
            if not Validator.is_valid_email(request.email):
                errors.append(ErrorHandler.invalid_parameter('email'))
            if not Validator.is_not_empty(request.location_city):
                errors.append(ErrorHandler.invalid_parameter('location_city'))
            if not Validator.is_not_empty(request.location_state):
                errors.append(ErrorHandler.invalid_parameter('location_state'))
            if request.business_size and not Validator.is_valid_size(request.business_size):
                errors.append(ErrorHandler.invalid_parameter('business_size'))
            
            if errors:
                response.errors.extend(errors)
                return response
            
            with DatabaseManager.get_session() as session:
                # Check duplicates
                existing_email = session.query(Business).filter(
                    func.lower(Business.email) == func.lower(request.email)
                ).first()
                
                if existing_email:
                    response.errors.append(
                        ErrorHandler.already_exists('Business', 'email', request.email)
                    )
                    return response
                
                existing_name = session.query(Business).filter(
                    func.lower(Business.business_name) == func.lower(request.business_name)
                ).first()
                
                if existing_name:
                    response.errors.append(
                        ErrorHandler.already_exists('Business', 'name', request.business_name)
                    )
                    return response
                
                # Get business size
                size_code = BusinessConverter.size_to_code(
                    request.business_size if request.business_size else 'SMALL'
                )
                business_size = session.query(BusinessSize).filter(
                    BusinessSize.code == size_code
                ).first()
                
                # Create business
                new_business = Business(
                    business_name=request.business_name,
                    email=request.email,
                    website_url=request.website_url or None,
                    phone_number=request.phone_number or None,
                    location_city=request.location_city,
                    location_state=request.location_state,
                    ein=request.ein or None,
                    business_description=request.business_description or '',
                    business_size_id=business_size.business_size_id
                )
                
                session.add(new_business)
                session.flush()

                print(f"✅ Business Record Created: {new_business.business_id}")

                # ✅ SAVE SHOP URL
                if request.shop_url:
                    new_shop = BusinessShop(
                        business_id=new_business.business_id,
                        shop_url=request.shop_url
                    )
                    session.add(new_shop)
                    print(f"🛍️ Shop URL saved: {request.shop_url}")

                # ✅ SAVE SOCIAL MEDIA
                if request.social_media_links:
                    for link in request.social_media_links:
                        if link.strip():
                            new_social = BusinessSocialMedia(
                                business_id=new_business.business_id,
                                social_media_link=link.strip()
                            )
                            session.add(new_social)
                    print(f"📱 Saved {len(request.social_media_links)} social media links")

                # Link user
                if request.user_email:
                    user = session.query(AppUser).filter(
                        func.lower(AppUser.email) == func.lower(request.user_email)
                    ).first()
                    
                    if user:
                        admin_role = session.query(BusinessUserPermissionRole).filter(
                            BusinessUserPermissionRole.code == 1
                        ).first()
                        
                        if admin_role:
                            business_user = BusinessUser(
                                business_id=new_business.business_id,
                                app_user_id=user.app_user_id,
                                business_user_permission_role_id=admin_role.business_user_permission_role_id
                            )
                            session.add(business_user)
                
                # Create Cause Preferences
                if hasattr(request, 'cause_codes') and request.cause_codes:
                    print(f"📥 Received {len(request.cause_codes)} cause codes")
                    default_rank = session.query(CausePreferenceRank).filter(CausePreferenceRank.code == 1).first()
                    
                    if default_rank:
                        for enum_value in request.cause_codes:
                            db_cause_name = CauseMapper.enum_to_db_name(enum_value)
                            cause = session.query(Cause).filter(Cause.cause_name == db_cause_name).first()
                            
                            if cause:
                                cause_pref = BusinessCausePreference(
                                    business_id=new_business.business_id,
                                    cause_id=cause.cause_id,
                                    cause_preference_rank_id=default_rank.cause_preference_rank_id
                                )
                                session.add(cause_pref)
                
                # Convert to response using Helper
                domain_business = BusinessConverter.to_domain(new_business)
                response.business.CopyFrom(self._map_to_proto(session, domain_business))
                
                print(f"✅ Business created successfully with ID: {new_business.business_id}")
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"❌ Error in CreateBusiness: {e}")
            import traceback
            traceback.print_exc()
        
        return response