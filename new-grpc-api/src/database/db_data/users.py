from database.models.user import UserDbo, UserTypeCode

def get_user_by_email(email: str) -> UserDbo:
    """
    Simulating query selection from database.
    In real implementation, this would be replaced with actual database queries.
    """
    return next((
        user for user in users
        if user.email.lower() == email.lower()
    ), None)

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
