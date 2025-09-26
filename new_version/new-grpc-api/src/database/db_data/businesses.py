from database.models.business import BusinessDbo, BusinessSizeCode

def get_business_by_id(business_id: str) -> BusinessDbo:
    """
    Simulating query selection from database.
    In real implementation, this would be replaced with actual database queries.
    """
    return next((
        business for business in businesses
        if business.business_id == business_id
    ), None)

def get_business_by_email(email: str) -> BusinessDbo:
    """Get business by email"""
    return next((
        business for business in businesses
        if business.email.lower() == email.lower()
    ), None)

def add_business(business: BusinessDbo) -> None:
    """Add a new business to the mock database"""
    businesses.append(business)

def business_email_exists(email: str) -> bool:
    """Check if business email already exists"""
    return get_business_by_email(email) is not None

def business_name_exists(name: str) -> bool:
    """Check if business name already exists"""
    return next((
        business for business in businesses
        if business.business_name.lower() == name.lower()
    ), None) is not None

# Mock data for testing
businesses = [
    BusinessDbo(
        business_id="b1234567-1234-1234-1234-123456789012",
        business_name="Tech Solutions Inc",
        email="admin@techsolutions.com",
        website_url="https://techsolutions.com",
        phone_number="555-0123",
        location_city="San Francisco",
        location_state="CA",
        ein="12-3456789",
        business_description="Leading technology solutions provider",
        business_size_code=BusinessSizeCode.MEDIUM
    ),
    BusinessDbo(
        business_id="b2345678-2345-2345-2345-234567890123",
        business_name="Local Coffee Shop",
        email="owner@localcoffee.com",
        website_url="https://localcoffee.com",
        phone_number="555-0456",
        location_city="Denver",
        location_state="CO",
        business_description="Artisanal coffee and community gathering place",
        business_size_code=BusinessSizeCode.SMALL
    ),
]
