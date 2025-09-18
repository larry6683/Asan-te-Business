import uuid
from database.models.user import UserDbo, UserTypeCode, CreateUserDbo

def get_user_by_email(email: str) -> UserDbo:
    """
    Simulating query selection from database.
    In real implementation, this would be replaced with actual database queries.
    """
    return next((
        user for user in users
        if user.email.lower() == email.lower()
    ), None)

def create_user(create_user_data: CreateUserDbo) -> UserDbo:
    """
    Create a new user in the mock database.
    In real implementation, this would be replaced with actual database insert.
    """
    # Check if user already exists
    existing_user = get_user_by_email(create_user_data.email)
    if existing_user:
        return None  # User already exists
    
    # Create new user
    new_user = UserDbo(
        app_user_id=str(uuid.uuid4()),
        email=create_user_data.email,
        user_type_code=create_user_data.user_type_code
    )
    
    users.append(new_user)
    return new_user

# Mock data for testing
users = [
    UserDbo(
        app_user_id="2e779286-c1a4-462d-9897-3ffedbe4261f",
        email="admin@business1.com",
        user_type_code=UserTypeCode.BUSINESS
    ),
    UserDbo(
        app_user_id="f1a21dfc-5ea5-4e52-8f6f-2295dc5482fa",
        email="admin@business2.com",
        user_type_code=UserTypeCode.BUSINESS
    ),
    UserDbo(
        app_user_id="1d1575f0-9766-4eb3-a65b-9f99d2bd21c5",
        email="beneficiary@org1.com",
        user_type_code=UserTypeCode.BENEFICIARY
    ),
    UserDbo(
        app_user_id="consumer1@email.com",
        email="consumer1@email.com",
        user_type_code=UserTypeCode.CONSUMER
    ),
]
