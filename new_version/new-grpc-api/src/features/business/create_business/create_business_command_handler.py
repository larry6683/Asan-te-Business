# new_version/new-grpc-api/src/features/business/create_business/create_business_command_handler.py
import uuid
import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import func

# Import path fix
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, src_path)

from database_path_fix import import_sqlalchemy_models

# Try to import SQLAlchemy models
Business, BusinessSize, AppUser, BusinessUser, BusinessUserPermissionRole, SQLALCHEMY_AVAILABLE = import_sqlalchemy_models(['Business', 'BusinessSize', 'AppUser', 'BusinessUser', 'BusinessUserPermissionRole'])

from config.config import Config
from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils
from converters.business_converter import BusinessConverter
from domain.business import BusinessSize as DomainBusinessSize

# Keep old mock functionality
from database.db_data.businesses import get_business_by_email, add_business, business_email_exists, business_name_exists
from database.db_data.users import get_user_by_email
from database.models.business import BusinessDbo, BusinessSizeCode

from .create_business_command import CreateBusinessCommand, CreateBusinessCommandResult

class CreateBusinessCommandHandler(
    RequestHandler[CreateBusinessCommand, CreateBusinessCommandResult]
):
    def __init__(self):
        pass

    def handle(self, request: CreateBusinessCommand) -> CreateBusinessCommandResult:
        # Check if we should use database and if SQLAlchemy is available
        try:
            use_db = Config.use_db()
        except:
            use_db = False
            
        if not use_db or not SQLALCHEMY_AVAILABLE:
            print("Using mock database (SQLAlchemy not available or not configured)")
            return self.handle_mock(request)
        
        try:
            from database.db_connection import DatabaseConnection
            with DatabaseConnection.get_session() as session:
                return self.handle_with_sqlalchemy(session, request)
        except Exception as e:
            print(f"SQLAlchemy handler failed: {e}, falling back to mock")
            return self.handle_mock(request)
    
    def handle_with_sqlalchemy(self, session: Session, request: CreateBusinessCommand) -> CreateBusinessCommandResult:
        """SQLAlchemy implementation using the new database models"""
        try:
            # Check if business email already exists
            existing_business = (session.query(Business)
                               .filter(func.lower(Business.email) == func.lower(request.email))
                               .first())
            
            if existing_business:
                return CreateBusinessCommandResult(
                    errors=[ErrorUtils.create_error(10, f"Business email '{request.email}' already exists")]
                )
            
            # Check if business name already exists
            existing_name = (session.query(Business)
                           .filter(func.lower(Business.business_name) == func.lower(request.business_name))
                           .first())
            
            if existing_name:
                return CreateBusinessCommandResult(
                    errors=[ErrorUtils.create_error(11, f"Business name '{request.business_name}' already exists")]
                )
            
            # Validate business size
            domain_business_size = BusinessConverter.business_size_from_string(request.business_size)
            
            # Get business size code and find BusinessSize entity
            business_size_code = BusinessConverter.business_size_string_to_code(request.business_size)
            business_size_entity = (session.query(BusinessSize)
                                  .filter(BusinessSize.code == business_size_code)
                                  .first())
            
            if not business_size_entity:
                return CreateBusinessCommandResult(
                    errors=[ErrorUtils.create_parameter_error(f"Invalid business size: '{request.business_size}'")]
                )
            
            # Find the user if user_email is provided
            app_user = None
            if request.user_email:
                app_user = (session.query(AppUser)
                          .filter(func.lower(AppUser.email) == func.lower(request.user_email))
                          .first())
                
                if not app_user:
                    return CreateBusinessCommandResult(
                        errors=[ErrorUtils.create_user_not_found_error(request.user_email)]
                    )
            
            # Create new business
            new_business = Business(
                business_name=request.business_name,
                email=request.email,
                website_url=request.website_url,
                phone_number=request.phone_number,
                location_city=request.location_city,
                location_state=request.location_state,
                ein=request.ein,
                business_description=request.business_description or "",
                business_size_id=business_size_entity.business_size_id
            )
            
            session.add(new_business)
            session.flush()  # Flush to get the ID
            
            # Link user to business if user_email provided
            if app_user:
                # Get admin permission role (assuming code 1 is admin)
                admin_role = (session.query(BusinessUserPermissionRole)
                            .filter(BusinessUserPermissionRole.code == 1)
                            .first())
                
                if admin_role:
                    business_user = BusinessUser(
                        business_id=new_business.business_id,
                        app_user_id=app_user.app_user_id,
                        business_user_permission_role_id=admin_role.business_user_permission_role_id
                    )
                    session.add(business_user)
            
            # Convert to domain object
            business = BusinessConverter.to_domain(new_business)
            
            return CreateBusinessCommandResult(business=business)
            
        except Exception as e:
            session.rollback()
            return CreateBusinessCommandResult(
                errors=[ErrorUtils.create_operation_failed_error(self.handle_with_sqlalchemy, str(e), e)]
            )
        
    def handle_mock(self, request: CreateBusinessCommand) -> CreateBusinessCommandResult:
        """Keep existing mock functionality for development"""
        # Check if business email already exists
        if business_email_exists(request.email):
            return CreateBusinessCommandResult(
                errors=[ErrorUtils.create_error(10, f"Business email '{request.email}' already exists")]
            )
        
        # Check if business name already exists
        if business_name_exists(request.business_name):
            return CreateBusinessCommandResult(
                errors=[ErrorUtils.create_error(11, f"Business name '{request.business_name}' already exists")]
            )
        
        # Validate user exists if provided
        if request.user_email:
            user = get_user_by_email(request.user_email)
            if not user:
                return CreateBusinessCommandResult(
                    errors=[ErrorUtils.create_user_not_found_error(request.user_email)]
                )
        
        # Convert business size string to enum
        business_size = BusinessConverter.business_size_from_string(request.business_size)
        
        # Create new business with old DBO structure
        new_business_dbo = BusinessDbo(
            business_id=str(uuid.uuid4()),
            business_name=request.business_name,
            email=request.email,
            website_url=request.website_url,
            phone_number=request.phone_number,
            location_city=request.location_city,
            location_state=request.location_state,
            ein=request.ein,
            business_description=request.business_description or "",
            business_size_code=BusinessSizeCode.from_str(request.business_size)
        )
        
        # Add to mock database
        add_business(new_business_dbo)
        
        # Convert old DBO to domain object
        business_size_map = {
            BusinessSizeCode.SMALL: DomainBusinessSize.SMALL,
            BusinessSizeCode.MEDIUM: DomainBusinessSize.MEDIUM,
            BusinessSizeCode.LARGE: DomainBusinessSize.LARGE
        }
        
        from domain.business import Business
        business = Business(
            id=new_business_dbo.business_id,
            business_name=new_business_dbo.business_name,
            email=new_business_dbo.email,
            website_url=new_business_dbo.website_url,
            phone_number=new_business_dbo.phone_number,
            location_city=new_business_dbo.location_city,
            location_state=new_business_dbo.location_state,
            ein=new_business_dbo.ein,
            business_description=new_business_dbo.business_description,
            business_size=business_size_map[new_business_dbo.business_size_code]
        )
        
        return CreateBusinessCommandResult(business=business)
