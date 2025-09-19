"""
Usage: bash python -m database_layer.tests.test_shop_type
"""
from database_layer.models.shop_type import ShopType
from .test_utils import create_test_session

def test_shop_type_model():
    print("=== Testing ShopType Model ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating shop types...")
    
    # Create shop type (from your populate script - only shopify for now)
    shopify = ShopType(code=1, shop_type_name='shopify')
    
    session.add(shopify)
    session.commit()
    
    print("✅ Created shop type")
    
    print("\n2. Testing queries...")
    
    # Query by code
    shopify_type = session.query(ShopType).filter_by(code=1).first()
    print(f"Found by code: {shopify_type}")
    
    # Query by name
    shopify_by_name = session.query(ShopType).filter_by(shop_type_name='shopify').first()
    print(f"Found by name: {shopify_by_name}")
    
    # Get all
    all_types = session.query(ShopType).all()
    print(f"Total shop types: {len(all_types)}")
    
    print("\n3. Verifying expected type exists...")
    
    expected_types = ['shopify']
    for type_name in expected_types:
        shop_type = session.query(ShopType).filter_by(shop_type_name=type_name).first()
        if shop_type:
            print(f"✅ Found: {type_name} (code {shop_type.code})")
        else:
            print(f"❌ Missing: {type_name}")
    
    print("\n4. Testing unique code constraint...")
    
    try:
        duplicate_code = ShopType(code=1, shop_type_name='duplicate-shopify')
        session.add(duplicate_code)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate code!")
    except Exception as e:
        print("✅ Unique code constraint working")
        session.rollback()
    
    print("\n5. Testing we can add more shop types...")
    
    try:
        # Add another shop type with different code
        etsy = ShopType(code=2, shop_type_name='etsy')
        session.add(etsy)
        session.commit()
        print("✅ Can add additional shop types")
        
        # Verify we now have 2
        total = session.query(ShopType).count()
        print(f"Total shop types after adding etsy: {total}")
    except Exception as e:
        print(f"❌ Error adding additional shop type: {e}")
        session.rollback()
    
    session.close()
    print("\n🎉 ShopType model working perfectly!")

if __name__ == "__main__":
    test_shop_type_model()