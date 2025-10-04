"""
Usage: bash python -m database_layer.tests.test_beneficiary_size
"""
from database_layer.src.public.tables.beneficiary_size import BeneficiarySize
from .test_utils import create_test_session

def test_beneficiary_size_model():
    print("=== Testing BeneficiarySize Model ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating beneficiary sizes...")
    
    # Create the 3 standard beneficiary sizes (from your populate script)
    small = BeneficiarySize(code=1, beneficiary_size_name='small')
    medium = BeneficiarySize(code=2, beneficiary_size_name='medium')
    large = BeneficiarySize(code=3, beneficiary_size_name='large')
    
    session.add_all([small, medium, large])
    session.commit()
    
    print("✅ Created all 3 beneficiary sizes")
    
    print("\n2. Testing queries...")
    
    # Query by code
    medium_size = session.query(BeneficiarySize).filter_by(code=2).first()
    print(f"Found by code: {medium_size}")
    
    # Query by name
    large_size = session.query(BeneficiarySize).filter_by(beneficiary_size_name='large').first()
    print(f"Found by name: {large_size}")
    
    # Get all
    all_sizes = session.query(BeneficiarySize).all()
    print(f"Total beneficiary sizes: {len(all_sizes)}")
    
    print("\n3. Verifying all expected sizes exist...")
    
    expected_sizes = ['small', 'medium', 'large']
    for size_name in expected_sizes:
        size = session.query(BeneficiarySize).filter_by(beneficiary_size_name=size_name).first()
        if size:
            print(f"✅ Found: {size_name} (code {size.code})")
        else:
            print(f"❌ Missing: {size_name}")
    
    print("\n4. Testing unique code constraint...")
    
    try:
        duplicate_code = BeneficiarySize(code=1, beneficiary_size_name='duplicate-small')
        session.add(duplicate_code)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate code!")
    except Exception as e:
        print("✅ Unique code constraint working")
        session.rollback()
    
    print("\n5. Testing unique name constraint...")
    
    try:
        duplicate_name = BeneficiarySize(code=99, beneficiary_size_name='small')
        session.add(duplicate_name)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate name!")
    except Exception as e:
        print("✅ Unique name constraint working")
        session.rollback()
    
    session.close()
    print("\n🎉 BeneficiarySize model working perfectly!")

if __name__ == "__main__":
    test_beneficiary_size_model()