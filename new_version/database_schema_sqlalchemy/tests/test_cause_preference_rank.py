"""
Usage: bash python -m database_layer.tests.test_cause_preference_rank
"""
from database_layer.src.public.tables.cause_preference_rank import CausePreferenceRank
from .test_utils import create_test_session

def test_cause_preference_rank_model():
    print("=== Testing CausePreferenceRank Model ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating cause preference ranks...")
    
    # Create the 3 standard preference ranks (from your populate script)
    unranked = CausePreferenceRank(code=1, cause_preference_rank_name='unranked')
    primary = CausePreferenceRank(code=2, cause_preference_rank_name='primary')
    supporting = CausePreferenceRank(code=3, cause_preference_rank_name='supporting')
    
    session.add_all([unranked, primary, supporting])
    session.commit()
    
    print("✅ Created all 3 preference ranks")
    
    print("\n2. Testing queries...")
    
    # Query by code
    primary_rank = session.query(CausePreferenceRank).filter_by(code=2).first()
    print(f"Found by code: {primary_rank}")
    
    # Query by name
    unranked_rank = session.query(CausePreferenceRank).filter_by(cause_preference_rank_name='unranked').first()
    print(f"Found by name: {unranked_rank}")
    
    # Get all
    all_ranks = session.query(CausePreferenceRank).all()
    print(f"Total preference ranks: {len(all_ranks)}")
    
    print("\n3. Verifying all expected ranks exist...")
    
    expected_ranks = ['unranked', 'primary', 'supporting']
    for rank_name in expected_ranks:
        rank = session.query(CausePreferenceRank).filter_by(cause_preference_rank_name=rank_name).first()
        if rank:
            print(f"✅ Found: {rank_name} (code {rank.code})")
        else:
            print(f"❌ Missing: {rank_name}")
    
    print("\n4. Testing unique code constraint...")
    
    try:
        duplicate_code = CausePreferenceRank(code=1, cause_preference_rank_name='duplicate-unranked')
        session.add(duplicate_code)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate code!")
    except Exception as e:
        print("✅ Unique code constraint working")
        session.rollback()
    
    print("\n5. Testing unique name constraint...")
    
    try:
        duplicate_name = CausePreferenceRank(code=99, cause_preference_rank_name='primary')
        session.add(duplicate_name)
        session.commit()
        print("❌ ERROR: Should have failed due to duplicate name!")
    except Exception as e:
        print("✅ Unique name constraint working")
        session.rollback()
    
    session.close()
    print("\n🎉 CausePreferenceRank model working perfectly!")

if __name__ == "__main__":
    test_cause_preference_rank_model()