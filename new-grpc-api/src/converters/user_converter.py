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
            user_type=user_type_map[user_dbo.user_type_code]
        )
    
    @staticmethod
    def user_type_to_string(user_type: UserType) -> str:
        """Convert UserType enum to string"""
        return user_type.name
