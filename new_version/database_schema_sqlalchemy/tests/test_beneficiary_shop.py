"""
Usage: bash python -m database_layer.tests.test_beneficiary_shop
"""
import uuid
from sqlalchemy.sql import func
from database_layer.src.public.tables.beneficiary_size import BeneficiarySize
from database_layer.src.public.tables.beneficiary import Beneficiary
from database_layer.src.public.tables.shop_type import ShopType
from database_layer.src.public.tables.beneficiary_shop import BeneficiaryShop
from .test_utils import create_test_session

def test_beneficiary_shop_junction():
    print("=== Testing BeneficiaryShop Junction Table ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create beneficiary size
    medium = BeneficiarySize(code=2, beneficiary_size_name='medium')
    
    # Create shop types
    shopify = ShopType(code=1, shop_type_name='shopify')
    etsy = ShopType(code=2, shop_type_name='etsy')
    
    session.add_all([medium, shopify, etsy])
    session.commit()
    print("✅ Created parent records")
    
    print("\n2. Creating beneficiaries...")
    
    # Create beneficiaries
    homeless_shelter = Beneficiary(
        beneficiary_name='Downtown Homeless Shelter',
        email='info@downtownshelter.org',
        location_city='Denver',
        location_state='CO',
        beneficiary_size_id=medium.beneficiary_size_id
    )
    
    food_bank = Beneficiary(
        beneficiary_name='Community Food Bank',
        email='contact@communityfoodbank.org',
        location_city='Boulder',
        location_state='CO',
        beneficiary_size_id=medium.beneficiary_size_id
    )
    
    session.add_all([homeless_shelter, food_bank])
    session.commit()
    print("✅ Created beneficiaries")
    
    print("\n3. Creating beneficiary shops...")
    
    # Homeless Shelter shops
    shelter_shopify = BeneficiaryShop(
        beneficiary_id=homeless_shelter.beneficiary_id,
        shop_type_id=shopify.shop_type_id,
        shop_url='https://downtownshelter.myshopify.com'
    )
    
    # Food Bank shops
    foodbank_shopify = BeneficiaryShop(
        beneficiary_id=food_bank.beneficiary_id,
        shop_type_id=shopify.shop_type_id,
        shop_url='https://communityfoodbank.myshopify.com'
    )
    
    foodbank_etsy = BeneficiaryShop(
        beneficiary_id=food_bank.beneficiary_id,
        shop_type_id=etsy.shop_type_id,
        shop_url='https://etsy.com/shop/CommunityFoodBank'
    )
    
    session.add_all([shelter_shopify, foodbank_shopify, foodbank_etsy])
    session.commit()
    print("✅ Created beneficiary shops")
    
    print("\n4. Testing relationship navigation...")
    
    # Find all shops for each beneficiary
    shelter_shops = session.query(BeneficiaryShop).filter_by(beneficiary_id=homeless_shelter.beneficiary_id).all()
    print(f"Homeless Shelter has {len(shelter_shops)} shop(s):")
    for shop in shelter_shops:
        print(f"  - {shop.shop_type.shop_type_name}: {shop.shop_url}")
    
    foodbank_shops = session.query(BeneficiaryShop).filter_by(beneficiary_id=food_bank.beneficiary_id).all()
    print(f"Food Bank has {len(foodbank_shops)} shop(s):")
    for shop in foodbank_shops:
        print(f"  - {shop.shop_type.shop_type_name}: {shop.shop_url}")
    
    print("\n5. Testing reverse navigation...")
    
    # Find all beneficiaries on each platform
    shopify_beneficiaries = session.query(BeneficiaryShop).filter_by(shop_type_id=shopify.shop_type_id).all()
    print(f"Shopify has {len(shopify_beneficiaries)} beneficiary/ies:")
    for ben_shop in shopify_beneficiaries:
        print(f"  - {ben_shop.beneficiary.beneficiary_name}: {ben_shop.shop_url}")
    
    etsy_beneficiaries = session.query(BeneficiaryShop).filter_by(shop_type_id=etsy.shop_type_id).all()
    print(f"Etsy has {len(etsy_beneficiaries)} beneficiary/ies:")
    for ben_shop in etsy_beneficiaries:
        print(f"  - {ben_shop.beneficiary.beneficiary_name}: {ben_shop.shop_url}")
    
    print("\n6. Testing foreign key constraints...")
    
    # Try to create shop with invalid beneficiary_id
    try:
        bad_beneficiary_shop = BeneficiaryShop(
            beneficiary_id=uuid.uuid4(),  # Random UUID that doesn't exist
            shop_type_id=shopify.shop_type_id,
            shop_url='https://bad.myshopify.com'
        )
        session.add(bad_beneficiary_shop)
        session.commit()
        print("❌ ERROR: Should have failed due to beneficiary foreign key constraint!")
    except Exception as e:
        print("✅ Beneficiary foreign key constraint working")
        session.rollback()
    
    # Try to create shop with invalid shop_type_id
    try:
        bad_type_shop = BeneficiaryShop(
            beneficiary_id=homeless_shelter.beneficiary_id,
            shop_type_id=uuid.uuid4(),  # Random UUID that doesn't exist
            shop_url='https://badplatform.com/shelter'
        )
        session.add(bad_type_shop)
        session.commit()
        print("❌ ERROR: Should have failed due to shop type foreign key constraint!")
    except Exception as e:
        print("✅ Shop type foreign key constraint working")
        session.rollback()
    
    print("\n7. Testing queries...")
    
    # Count shops by platform
    for platform in [shopify, etsy]:
        count = session.query(BeneficiaryShop).filter_by(shop_type_id=platform.shop_type_id).count()
        print(f"{platform.shop_type_name.title()} beneficiary shops: {count}")
    
    # Find beneficiaries with multiple shops
    beneficiaries_with_multiple = session.query(BeneficiaryShop.beneficiary_id).group_by(BeneficiaryShop.beneficiary_id).having(func.count() > 1).all()
    print(f"Beneficiaries with multiple shops: {len(beneficiaries_with_multiple)}")
    
    session.close()
    print("\n🎉 BeneficiaryShop junction table working perfectly!")

if __name__ == "__main__":
    test_beneficiary_shop_junction()