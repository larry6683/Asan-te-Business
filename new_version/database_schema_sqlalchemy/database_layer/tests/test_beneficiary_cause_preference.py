"""
Usage: bash python -m database_layer.tests.test_beneficiary_cause_preference
"""
import uuid
from sqlalchemy.sql import func
from database_layer.models.beneficiary_size import BeneficiarySize
from database_layer.models.beneficiary import Beneficiary
from database_layer.models.cause_category import CauseCategory
from database_layer.models.cause import Cause
from database_layer.models.cause_preference_rank import CausePreferenceRank
from database_layer.models.beneficiary_cause_preference import BeneficiaryCausePreference
from .test_utils import create_test_session

def test_beneficiary_cause_preference_junction():
    print("=== Testing BeneficiaryCausePreference Junction Table ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create beneficiary sizes
    medium = BeneficiarySize(code=2, beneficiary_size_name='medium')
    small = BeneficiarySize(code=1, beneficiary_size_name='small')
    
    # Create cause categories
    community = CauseCategory(code=1, cause_category_name='Community')
    social = CauseCategory(code=2, cause_category_name='Social')
    environment = CauseCategory(code=4, cause_category_name='Environment')
    
    # Create cause preference ranks
    unranked = CausePreferenceRank(code=1, cause_preference_rank_name='unranked')
    primary = CausePreferenceRank(code=2, cause_preference_rank_name='primary')
    supporting = CausePreferenceRank(code=3, cause_preference_rank_name='supporting')
    
    session.add_all([medium, small, community, social, environment, unranked, primary, supporting])
    session.commit()
    print("✅ Created basic parent records")
    
    print("\n2. Creating causes...")
    
    # Create causes
    homelessness = Cause(
        code=1,
        cause_name='Homelessness',
        cause_category_id=community.cause_category_id
    )
    
    education = Cause(
        code=8,
        cause_name='Education',
        cause_category_id=social.cause_category_id
    )
    
    mental_health = Cause(
        code=10,
        cause_name='Mental Health & Wellbeing',
        cause_category_id=social.cause_category_id
    )
    
    climate_advocacy = Cause(
        code=16,
        cause_name='Climate Advocacy',
        cause_category_id=environment.cause_category_id
    )
    
    session.add_all([homelessness, education, mental_health, climate_advocacy])
    session.commit()
    print("✅ Created causes")
    
    print("\n3. Creating beneficiaries...")
    
    # Create beneficiaries
    homeless_shelter = Beneficiary(
        beneficiary_name='Downtown Homeless Shelter',
        email='info@downtownshelter.org',
        location_city='Denver',
        location_state='CO',
        beneficiary_size_id=medium.beneficiary_size_id,
        beneficiary_description='Emergency shelter and support services'
    )
    
    community_center = Beneficiary(
        beneficiary_name='Community Learning Center',
        email='contact@communitylearning.org',
        location_city='Boulder',
        location_state='CO',
        beneficiary_size_id=small.beneficiary_size_id,
        beneficiary_description='Educational programs for all ages'
    )
    
    session.add_all([homeless_shelter, community_center])
    session.commit()
    print("✅ Created beneficiaries")
    
    print("\n4. Creating beneficiary cause preferences...")
    
    # Homeless Shelter preferences (community and social focus)
    shelter_primary_homelessness = BeneficiaryCausePreference(
        beneficiary_id=homeless_shelter.beneficiary_id,
        cause_id=homelessness.cause_id,
        cause_preference_rank_id=primary.cause_preference_rank_id
    )
    
    shelter_supporting_mental_health = BeneficiaryCausePreference(
        beneficiary_id=homeless_shelter.beneficiary_id,
        cause_id=mental_health.cause_id,
        cause_preference_rank_id=supporting.cause_preference_rank_id
    )
    
    # Community Center preferences (education focus)
    center_primary_education = BeneficiaryCausePreference(
        beneficiary_id=community_center.beneficiary_id,
        cause_id=education.cause_id,
        cause_preference_rank_id=primary.cause_preference_rank_id
    )
    
    center_supporting_mental_health = BeneficiaryCausePreference(
        beneficiary_id=community_center.beneficiary_id,
        cause_id=mental_health.cause_id,
        cause_preference_rank_id=supporting.cause_preference_rank_id
    )
    
    center_unranked_climate = BeneficiaryCausePreference(
        beneficiary_id=community_center.beneficiary_id,
        cause_id=climate_advocacy.cause_id,
        cause_preference_rank_id=unranked.cause_preference_rank_id
    )
    
    session.add_all([shelter_primary_homelessness, shelter_supporting_mental_health, center_primary_education, center_supporting_mental_health, center_unranked_climate])
    session.commit()
    print("✅ Created beneficiary cause preferences")
    
    print("\n5. Testing relationship navigation...")
    
    # Find all cause preferences for each beneficiary
    shelter_preferences = session.query(BeneficiaryCausePreference).filter_by(beneficiary_id=homeless_shelter.beneficiary_id).all()
    print(f"Homeless Shelter has {len(shelter_preferences)} cause preference(s):")
    for pref in shelter_preferences:
        print(f"  - {pref.cause.cause_name} ({pref.preference_rank.cause_preference_rank_name})")
    
    center_preferences = session.query(BeneficiaryCausePreference).filter_by(beneficiary_id=community_center.beneficiary_id).all()
    print(f"Community Center has {len(center_preferences)} cause preference(s):")
    for pref in center_preferences:
        print(f"  - {pref.cause.cause_name} ({pref.preference_rank.cause_preference_rank_name})")
    
    print("\n6. Testing reverse navigation (causes -> beneficiaries)...")
    
    # Find all beneficiaries working on each cause
    mental_health_supporters = session.query(BeneficiaryCausePreference).filter_by(cause_id=mental_health.cause_id).all()
    print(f"Mental Health & Wellbeing is supported by {len(mental_health_supporters)} beneficiary/ies:")
    for supporter in mental_health_supporters:
        print(f"  - {supporter.beneficiary.beneficiary_name} ({supporter.preference_rank.cause_preference_rank_name})")
    
    education_supporters = session.query(BeneficiaryCausePreference).filter_by(cause_id=education.cause_id).all()
    print(f"Education is supported by {len(education_supporters)} beneficiary/ies:")
    for supporter in education_supporters:
        print(f"  - {supporter.beneficiary.beneficiary_name} ({supporter.preference_rank.cause_preference_rank_name})")
    
    print("\n7. Testing preference rank queries...")
    
    # Find all primary preferences
    primary_preferences = session.query(BeneficiaryCausePreference).filter_by(cause_preference_rank_id=primary.cause_preference_rank_id).all()
    print(f"Primary cause preferences ({len(primary_preferences)}):")
    for pref in primary_preferences:
        print(f"  - {pref.beneficiary.beneficiary_name} → {pref.cause.cause_name}")
    
    # Find all supporting preferences
    supporting_preferences = session.query(BeneficiaryCausePreference).filter_by(cause_preference_rank_id=supporting.cause_preference_rank_id).all()
    print(f"Supporting cause preferences ({len(supporting_preferences)}):")
    for pref in supporting_preferences:
        print(f"  - {pref.beneficiary.beneficiary_name} → {pref.cause.cause_name}")
    
    print("\n8. Testing foreign key constraints...")
    
    # Try to create preference with invalid beneficiary_id
    try:
        bad_beneficiary_pref = BeneficiaryCausePreference(
            beneficiary_id=uuid.uuid4(),  # Random UUID that doesn't exist
            cause_id=education.cause_id,
            cause_preference_rank_id=primary.cause_preference_rank_id
        )
        session.add(bad_beneficiary_pref)
        session.commit()
        print("❌ ERROR: Should have failed due to beneficiary foreign key constraint!")
    except Exception as e:
        print("✅ Beneficiary foreign key constraint working")
        session.rollback()
    
    # Try to create preference with invalid cause_id
    try:
        bad_cause_pref = BeneficiaryCausePreference(
            beneficiary_id=homeless_shelter.beneficiary_id,
            cause_id=uuid.uuid4(),  # Random UUID that doesn't exist
            cause_preference_rank_id=primary.cause_preference_rank_id
        )
        session.add(bad_cause_pref)
        session.commit()
        print("❌ ERROR: Should have failed due to cause foreign key constraint!")
    except Exception as e:
        print("✅ Cause foreign key constraint working")
        session.rollback()
    
    # Try to create preference with invalid preference rank
    try:
        bad_rank_pref = BeneficiaryCausePreference(
            beneficiary_id=homeless_shelter.beneficiary_id,
            cause_id=education.cause_id,
            cause_preference_rank_id=uuid.uuid4()  # Random UUID that doesn't exist
        )
        session.add(bad_rank_pref)
        session.commit()
        print("❌ ERROR: Should have failed due to preference rank foreign key constraint!")
    except Exception as e:
        print("✅ Preference rank foreign key constraint working")
        session.rollback()
    
    print("\n9. Testing advanced queries...")
    
    # Count total preferences by rank
    for rank in [primary, supporting, unranked]:
        count = session.query(BeneficiaryCausePreference).filter_by(cause_preference_rank_id=rank.cause_preference_rank_id).count()
        print(f"{rank.cause_preference_rank_name.title()} preferences: {count}")
    
    # Find beneficiaries with multiple preferences
    beneficiaries_with_multiple = session.query(BeneficiaryCausePreference.beneficiary_id).group_by(BeneficiaryCausePreference.beneficiary_id).having(func.count() > 1).all()
    print(f"Beneficiaries with multiple cause preferences: {len(beneficiaries_with_multiple)}")
    
    session.close()
    print("\n🎉 BeneficiaryCausePreference junction table working perfectly!")

if __name__ == "__main__":
    test_beneficiary_cause_preference_junction()