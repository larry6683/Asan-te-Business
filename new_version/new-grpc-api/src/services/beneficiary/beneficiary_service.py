# new-grpc-api/src/services/beneficiary/beneficiary_service.py
# UPDATED VERSION - Replace the CreateBeneficiary method

from config.config import Config
from sqlalchemy import func
from src.public.tables import (
    Beneficiary, BeneficiarySize, AppUser, BeneficiaryUser, BeneficiaryUserPermissionRole,
    Cause, BeneficiaryCausePreference, CausePreferenceRank  # 🆕 ADD THESE
)
from database.db_manager import DatabaseManager
from converters.beneficiary_converter import BeneficiaryConverter
from utils.error_handler import ErrorHandler
from utils.validator import Validator
from utils.cause_mapper import CauseMapper  # 🆕 ADD THIS IMPORT
from codegen.beneficiary.beneficiary_pb2 import (
    GetBeneficiaryRequest, GetBeneficiaryResponse,
    CreateBeneficiaryRequest, CreateBeneficiaryResponse,
    Beneficiary as ProtoBeneficiary
)
from codegen.beneficiary.beneficiary_pb2_grpc import BeneficiaryServiceServicer

class BeneficiaryService(BeneficiaryServiceServicer):
    
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
                response.beneficiary.CopyFrom(ProtoBeneficiary(
                    id=domain_beneficiary.id,
                    beneficiary_name=domain_beneficiary.beneficiary_name,
                    email=domain_beneficiary.email,
                    website_url=domain_beneficiary.website_url,
                    phone_number=domain_beneficiary.phone_number,
                    location_city=domain_beneficiary.location_city,
                    location_state=domain_beneficiary.location_state,
                    ein=domain_beneficiary.ein,
                    beneficiary_description=domain_beneficiary.beneficiary_description,
                    beneficiary_size=BeneficiaryConverter.size_to_string(domain_beneficiary.beneficiary_size)
                ))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetBeneficiary: {e}")
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
                
                # 🆕 CREATE CAUSE PREFERENCES FOR BENEFICIARY
                # Note: Beneficiaries can have PRIMARY, SUPPORTING causes
                # The cause_codes should come from frontend with rank information
                # For now, we'll treat all as primary mission-aligned causes
                if hasattr(request, 'cause_codes') and request.cause_codes:
                    print(f"📥 Received {len(request.cause_codes)} cause codes for beneficiary")
                    
                    # Get primary rank for beneficiaries
                    primary_rank = session.query(CausePreferenceRank).filter(
                        CausePreferenceRank.code == 2  # PRIMARY rank
                    ).first()
                    
                    if not primary_rank:
                        print("❌ ERROR: No primary cause preference rank found")
                        response.errors.append(
                            ErrorHandler.internal_error("No primary cause preference rank found")
                        )
                        session.rollback()
                        return response
                    
                    print(f"✅ Using rank: {primary_rank.cause_preference_rank_name} (code={primary_rank.code})")
                    
                    # Process each cause code
                    causes_saved = 0
                    causes_failed = []
                    
                    for enum_value in request.cause_codes:
                        # Convert enum to database name
                        db_cause_name = CauseMapper.enum_to_db_name(enum_value)
                        print(f"🔄 Mapping: '{enum_value}' → '{db_cause_name}'")
                        
                        # Look up cause
                        cause = session.query(Cause).filter(
                            Cause.cause_name == db_cause_name
                        ).first()
                        
                        if cause:
                            print(f"✅ Found cause: '{cause.cause_name}' (ID={cause.cause_id})")
                            
                            # Create preference
                            cause_pref = BeneficiaryCausePreference(
                                beneficiary_id=new_beneficiary.beneficiary_id,
                                cause_id=cause.cause_id,
                                cause_preference_rank_id=primary_rank.cause_preference_rank_id
                            )
                            session.add(cause_pref)
                            causes_saved += 1
                        else:
                            print(f"⚠️ Cause not found: '{db_cause_name}'")
                            causes_failed.append(db_cause_name)
                    
                    print(f"📊 Summary: {causes_saved} causes saved, {len(causes_failed)} failed")
                
                # Convert to response
                domain_beneficiary = BeneficiaryConverter.to_domain(new_beneficiary)
                response.beneficiary.CopyFrom(ProtoBeneficiary(
                    id=domain_beneficiary.id,
                    beneficiary_name=domain_beneficiary.beneficiary_name,
                    email=domain_beneficiary.email,
                    website_url=domain_beneficiary.website_url,
                    phone_number=domain_beneficiary.phone_number,
                    location_city=domain_beneficiary.location_city,
                    location_state=domain_beneficiary.location_state,
                    ein=domain_beneficiary.ein,
                    beneficiary_description=domain_beneficiary.beneficiary_description,
                    beneficiary_size=BeneficiaryConverter.size_to_string(domain_beneficiary.beneficiary_size)
                ))
                
                print(f"✅ Beneficiary created successfully with ID: {new_beneficiary.beneficiary_id}")
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"❌ Error in CreateBeneficiary: {e}")
            import traceback
            traceback.print_exc()
        
        return response