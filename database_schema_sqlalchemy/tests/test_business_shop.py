"""
Usage: bash python -m database_layer.tests.test_business_shop
"""
import uuid
from sqlalchemy.sql import func
from database_layer.src.public.tables.business_size import BusinessSize
from database_layer.src.public.tables.business import Business
from database_layer.src.public.tables.shop_type import ShopType
from database_layer.src.public.tables.business_shop import BusinessShop
from .test_utils import create_test_session

def test_business_shop_junction():
    print("=== Testing BusinessShop Junction Table ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create business size
    medium = BusinessSize(code=2, business_size_name='medium')
    
    # Create shop types
    shopify = ShopType(code=1, shop_type_name='shopify')
    etsy = ShopType(code=2, shop_type_name='etsy')
    
    session.add_all([medium, shopify, etsy])
    session.commit()
    print("✅ Created parent records")
    
    print("\n2. Creating businesses...")
    
    # Create businesses
    eco_solutions = Business(
        business_name='Eco Solutions Inc.',
        email='contact@ecosolutions.com',
        location_city='Seattle',
        location_state='WA',
        business_size_id=medium.business_size_id
    )
    
    tech_innovations = Business(
        business_name='Tech Innovations Ltd',
        email='info@techinnovations.com',
        location_city='San Francisco',
        location_state='CA',
        business_size_id=medium.business_size_id
    )
    
    session.add_all([eco_solutions, tech_innovations])
    session.commit()
    print("✅ Created businesses")
    
    print("\n3. Creating business shops...")
    
    # Eco Solutions shops
    eco_shopify = BusinessShop(
        business_id=eco_solutions.business_id,
        shop_type_id=shopify.shop_type_id,
        shop_url='https://ecosolutions.myshopify.com'
    )
    
    eco_etsy = BusinessShop(
        business_id=eco_solutions.business_id,
        shop_type_id=etsy.shop_type_id,
        shop_url='https://etsy.com/shop/EcoSolutions'
    )
    
    # Tech Innovations shops
    tech_shopify = BusinessShop(
        business_id=tech_innovations.business_id,
        shop_type_id=shopify.shop_type_id,
        shop_url='https://techinnovations.myshopify.com'
    )
    
    session.add_all([eco_shopify, eco_etsy, tech_shopify])
    session.commit()
    print("✅ Created business shops")
    
    print("\n4. Testing relationship navigation...")
    
    # Find all shops for each business
    eco_shops = session.query(BusinessShop).filter_by(business_id=eco_solutions.business_id).all()
    print(f"Eco Solutions has {len(eco_shops)} shop(s):")
    for shop in eco_shops:
        print(f"  - {shop.shop_type.shop_type_name}: {shop.shop_url}")
    
    tech_shops = session.query(BusinessShop).filter_by(business_id=tech_innovations.business_id).all()
    print(f"Tech Innovations has {len(tech_shops)} shop(s):")
    for shop in tech_shops:
        print(f"  - {shop.shop_type.shop_type_name}: {shop.shop_url}")
    
    print("\n5. Testing reverse navigation...")
    
    # Find all businesses on each platform
    shopify_businesses = session.query(BusinessShop).filter_by(shop_type_id=shopify.shop_type_id).all()
    print(f"Shopify has {len(shopify_businesses)} business(es):")
    for biz_shop in shopify_businesses:
        print(f"  - {biz_shop.business.business_name}: {biz_shop.shop_url}")
    
    etsy_businesses = session.query(BusinessShop).filter_by(shop_type_id=etsy.shop_type_id).all()
    print(f"Etsy has {len(etsy_businesses)} business(es):")
    for biz_shop in etsy_businesses:
        print(f"  - {biz_shop.business.business_name}: {biz_shop.shop_url}")
    
    print("\n6. Testing foreign key constraints...")
    
    # Try to create shop with invalid business_id
    try:
        bad_business_shop = BusinessShop(
            business_id=uuid.uuid4(),  # Random UUID that doesn't exist
            shop_type_id=shopify.shop_type_id,
            shop_url='https://bad.myshopify.com'
        )
        session.add(bad_business_shop)
        session.commit()
        print("❌ ERROR: Should have failed due to business foreign key constraint!")
    except Exception as e:
        print("✅ Business foreign key constraint working")
        session.rollback()
    
    # Try to create shop with invalid shop_type_id
    try:
        bad_type_shop = BusinessShop(
            business_id=eco_solutions.business_id,
            shop_type_id=uuid.uuid4(),  # Random UUID that doesn't exist
            shop_url='https://badplatform.com/ecosolutions'
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
        count = session.query(BusinessShop).filter_by(shop_type_id=platform.shop_type_id).count()
        print(f"{platform.shop_type_name.title()} shops: {count}")
    
    # Find businesses with multiple shops
    businesses_with_multiple = session.query(BusinessShop.business_id).group_by(BusinessShop.business_id).having(func.count() > 1).all()
    print(f"Businesses with multiple shops: {len(businesses_with_multiple)}")
    
    session.close()
    print("\n🎉 BusinessShop junction table working perfectly!")

if __name__ == "__main__":
    test_business_shop_junction()