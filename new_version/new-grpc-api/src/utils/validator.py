import re

class Validator:
    
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(Validator.EMAIL_PATTERN, email))
    
    @staticmethod
    def is_not_empty(value: str) -> bool:
        return bool(value and value.strip())
    
    @staticmethod
    def is_valid_user_type(user_type: str) -> bool:
        valid_types = ['BUSINESS', 'BENEFICIARY', 'CONSUMER']
        return user_type.upper() in valid_types
    
    @staticmethod
    def is_valid_size(size: str) -> bool:
        valid_sizes = ['SMALL', 'MEDIUM', 'LARGE']
        return size.upper() in valid_sizes
