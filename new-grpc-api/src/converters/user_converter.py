from src.public.tables import AppUser, UserType
from domain.user import User, UserType as DomainUserType

class UserConverter:
    
    USER_TYPE_MAP = {
        1: DomainUserType.BUSINESS,
        2: DomainUserType.BENEFICIARY,
        3: DomainUserType.CONSUMER
    }
    
    USER_TYPE_REVERSE_MAP = {
        'BUSINESS': 1,
        'BENEFICIARY': 2,
        'CONSUMER': 3
    }
    
    @staticmethod
    def to_domain(db_user: AppUser) -> User:
        user_type = UserConverter.USER_TYPE_MAP.get(
            db_user.user_type.code, 
            DomainUserType.CONSUMER
        )
        
        return User(
            id=str(db_user.app_user_id),
            email=db_user.email,
            user_type=user_type,
            mailing_list_signup=db_user.mailing_list_signup
        )
    
    @staticmethod
    def user_type_to_code(user_type_str: str) -> int:
        return UserConverter.USER_TYPE_REVERSE_MAP.get(user_type_str.upper(), 1)
    
    @staticmethod
    def user_type_to_string(user_type: DomainUserType) -> str:
        return user_type.value
