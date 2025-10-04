# Import config first to set up database path
from config.config import Config

from sqlalchemy import func
from src.public.tables import (
    Business, BusinessSize, AppUser, BusinessUser, BusinessUserPermissionRole
)
from database.db_manager import DatabaseManager
from converters.business_converter import BusinessConverter
from utils.error_handler import ErrorHandler
from utils.validator import Validator
from codegen.business.business_pb2 import (
    GetBusinessRequest, GetBusinessResponse,
    CreateBusinessRequest, CreateBusinessResponse,
    Business as ProtoBusiness
)
from codegen.business.business_pb2_grpc import BusinessServiceServicer

class BusinessService(BusinessServiceServicer):
    
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
                response.business.CopyFrom(ProtoBusiness(
                    id=domain_business.id,
                    business_name=domain_business.business_name,
                    email=domain_business.email,
                    website_url=domain_business.website_url,
                    phone_number=domain_business.phone_number,
                    location_city=domain_business.location_city,
                    location_state=domain_business.location_state,
                    ein=domain_business.ein,
                    business_description=domain_business.business_description,
                    business_size=BusinessConverter.size_to_string(domain_business.business_size)
                ))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in GetBusiness: {e}")
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
                
                # Link user if provided
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
                
                # Convert to response
                domain_business = BusinessConverter.to_domain(new_business)
                response.business.CopyFrom(ProtoBusiness(
                    id=domain_business.id,
                    business_name=domain_business.business_name,
                    email=domain_business.email,
                    website_url=domain_business.website_url,
                    phone_number=domain_business.phone_number,
                    location_city=domain_business.location_city,
                    location_state=domain_business.location_state,
                    ein=domain_business.ein,
                    business_description=domain_business.business_description,
                    business_size=BusinessConverter.size_to_string(domain_business.business_size)
                ))
                
        except Exception as e:
            response.errors.append(ErrorHandler.internal_error(str(e)))
            print(f"Error in CreateBusiness: {e}")
            import traceback
            traceback.print_exc()
        
        return response
