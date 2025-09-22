from domain.user import User, UserType
from database.models.user import UserDbo, UserTypeCode

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
            user_type=user_type_map[user_dbo.user_type_code],
            mailing_list_signup=user_dbo.mailing_list_signup
        )
    
    @staticmethod
    def to_database(user: User) -> UserDbo:
        """Convert domain object to database object"""
        user_type_map = {
            UserType.BUSINESS: UserTypeCode.BUSINESS,
            UserType.BENEFICIARY: UserTypeCode.BENEFICIARY,
            UserType.CONSUMER: UserTypeCode.CONSUMER
        }
        
        return UserDbo(
            app_user_id=user.id,
            email=user.email,
            user_type_code=user_type_map[user.user_type],
            mailing_list_signup=user.mailing_list_signup
        )
    
    @staticmethod
    def user_type_to_string(user_type: UserType) -> str:
        """Convert UserType enum to string"""
        return user_type.name
        
    @staticmethod
    def user_type_from_string(user_type_str: str) -> UserType:
        """Convert string to UserType enum"""
        user_type_map = {
            'BUSINESS': UserType.BUSINESS,
            'BENEFICIARY': UserType.BENEFICIARY,
            'CONSUMER': UserType.CONSUMER
        }
        return user_type_map.get(user_type_str.upper())
