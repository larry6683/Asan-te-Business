# Import config first to set up database path
from config.config import Config

from sqlalchemy import func
from src.public.tables import (
    Beneficiary, BeneficiarySize, AppUser, BeneficiaryUser, BeneficiaryUserPermissionRole
)
from database.db_manager import DatabaseManager
from converters.beneficiary_converter import BeneficiaryConverter
from utils.error_handler import ErrorHandler
from utils.validator import Validator
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
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in CreateBeneficiary: {e}")
            import traceback
            traceback.print_exc()
        
        return response
