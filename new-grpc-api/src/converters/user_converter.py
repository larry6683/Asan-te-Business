from domain.user import User, UserType, CreateUserData
from database.models.user import UserDbo, UserTypeCode, CreateUserDbo

class UserConverter:
    @staticmethod
    def to_domain(user_dbo: UserDbo) -> User:
        """Convert database object to domain object"""
        user_type_map = {
            UserTypeCode.BUSINESS: UserType.BUSINESS,
            UserTypeCode.BENEFICIARY: UserType.BENEFICIARY,
            UserTypeCode.CONSUMER: UserType.CONSUMER
        }
        
        return User(
            id=user_dbo.app_user_id,
            email=user_dbo.email,
            user_type=user_type_map[user_dbo.user_type_code]
        )
    
    @staticmethod
    def user_type_to_string(user_type: UserType) -> str:
        """Convert UserType enum to string"""
        return user_type.name
    
    @staticmethod
    def user_type_from_string(user_type_str: str) -> UserType:
        """Convert string to UserType enum"""
        user_type_map = {
            "BUSINESS": UserType.BUSINESS,
            "BENEFICIARY": UserType.BENEFICIARY,
            "CONSUMER": UserType.CONSUMER
        }
        return user_type_map.get(user_type_str.upper())
    
    @staticmethod
    def to_create_user_dbo(create_user_data: CreateUserData) -> CreateUserDbo:
        """Convert domain create user data to database object"""
        user_type_map = {
            UserType.BUSINESS: UserTypeCode.BUSINESS,
            UserType.BENEFICIARY: UserTypeCode.BENEFICIARY,
            UserType.CONSUMER: UserTypeCode.CONSUMER
        }
        
        return CreateUserDbo(
            email=create_user_data.email,
            user_type_code=user_type_map[create_user_data.user_type],
            mailing_list_signup=create_user_data.mailing_list_signup
        )
