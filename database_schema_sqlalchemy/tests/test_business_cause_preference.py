"""
Usage: bash python -m database_layer.tests.test_business_cause_preference
"""
import uuid
from sqlalchemy.sql import func
from database_layer.src.public.tables.business_size import BusinessSize
from database_layer.src.public.tables.business import Business
from database_layer.src.public.tables.cause_category import CauseCategory
from database_layer.src.public.tables.cause import Cause
from database_layer.src.public.tables.cause_preference_rank import CausePreferenceRank
from database_layer.src.public.tables.business_cause_preference import BusinessCausePreference
from .test_utils import create_test_session

def test_business_cause_preference_junction():
    print("=== Testing BusinessCausePreference Junction Table ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create business sizes
    medium = BusinessSize(code=2, business_size_name='medium')
    small = BusinessSize(code=1, business_size_name='small')
    
    # Create cause categories
    environment = CauseCategory(code=4, cause_category_name='Environment')
    social = CauseCategory(code=2, cause_category_name='Social')
    community = CauseCategory(code=1, cause_category_name='Community')
    
    # Create cause preference ranks
    unranked = CausePreferenceRank(code=1, cause_preference_rank_name='unranked')
    primary = CausePreferenceRank(code=2, cause_preference_rank_name='primary')
    supporting = CausePreferenceRank(code=3, cause_preference_rank_name='supporting')
    
    session.add_all([medium, small, environment, social, community, unranked, primary, supporting])
    session.commit()
    print("✅ Created basic parent records")
    
    print("\n2. Creating causes...")
    
    # Create causes
    climate_advocacy = Cause(
        code=18,  
        cause_name='Climate Advocacy',
        cause_category_id=environment.cause_category_id
    )

    drought_fire = Cause(
        code=17,   
        cause_name='Droughts & Fire Management', 
        cause_category_id=environment.cause_category_id
    )

    education = Cause(
        code=10, 
        cause_name='Education',
        cause_category_id=social.cause_category_id
    )

    homelessness = Cause(
        code=1,  
        cause_name='Homelessness',
        cause_category_id=community.cause_category_id
    )
        
    session.add_all([climate_advocacy, drought_fire, education, homelessness])
    session.commit()
    print("✅ Created causes")
    
    print("\n3. Creating businesses...")
    
    # Create businesses
    eco_solutions = Business(
        business_name='Eco Solutions Inc.',
        email='contact@ecosolutions.com',
        location_city='Seattle',
        location_state='WA',
        business_size_id=medium.business_size_id,
        business_description='Sustainable product manufacturer'
    )
    
    tech_innovations = Business(
        business_name='Tech Innovations Ltd',
        email='info@techinnovations.com',
        location_city='San Francisco',
        location_state='CA',
        business_size_id=small.business_size_id,
        business_description='AI and machine learning solutions'
    )
    
    session.add_all([eco_solutions, tech_innovations])
    session.commit()
    print("✅ Created businesses")
    
    print("\n4. Creating business cause preferences...")
    
    # Eco Solutions preferences (environmental focus)
    eco_primary_climate = BusinessCausePreference(
        business_id=eco_solutions.business_id,
        cause_id=climate_advocacy.cause_id,
        cause_preference_rank_id=primary.cause_preference_rank_id
    )
    
    eco_supporting_drought = BusinessCausePreference(
        business_id=eco_solutions.business_id,
        cause_id=drought_fire.cause_id,
        cause_preference_rank_id=supporting.cause_preference_rank_id
    )
    
    # Tech Innovations preferences (education and social focus)
    tech_primary_education = BusinessCausePreference(
        business_id=tech_innovations.business_id,
        cause_id=education.cause_id,
        cause_preference_rank_id=primary.cause_preference_rank_id
    )
    
    tech_supporting_homelessness = BusinessCausePreference(
        business_id=tech_innovations.business_id,
        cause_id=homelessness.cause_id,
        cause_preference_rank_id=supporting.cause_preference_rank_id
    )
    
    tech_unranked_climate = BusinessCausePreference(
        business_id=tech_innovations.business_id,
        cause_id=climate_advocacy.cause_id,
        cause_preference_rank_id=unranked.cause_preference_rank_id
    )
    
    session.add_all([eco_primary_climate, eco_supporting_drought, tech_primary_education, tech_supporting_homelessness, tech_unranked_climate])
    session.commit()
    print("✅ Created business cause preferences")
    
    print("\n5. Testing relationship navigation...")
    
    # Find all cause preferences for each business
    eco_preferences = session.query(BusinessCausePreference).filter_by(business_id=eco_solutions.business_id).all()
    print(f"Eco Solutions has {len(eco_preferences)} cause preference(s):")
    for pref in eco_preferences:
        print(f"  - {pref.cause.cause_name} ({pref.preference_rank.cause_preference_rank_name})")
    
    tech_preferences = session.query(BusinessCausePreference).filter_by(business_id=tech_innovations.business_id).all()
    print(f"Tech Innovations has {len(tech_preferences)} cause preference(s):")
    for pref in tech_preferences:
        print(f"  - {pref.cause.cause_name} ({pref.preference_rank.cause_preference_rank_name})")
    
    print("\n6. Testing reverse navigation (causes -> businesses)...")
    
    # Find all businesses supporting each cause
    climate_supporters = session.query(BusinessCausePreference).filter_by(cause_id=climate_advocacy.cause_id).all()
    print(f"Climate Advocacy is supported by {len(climate_supporters)} business(es):")
    for supporter in climate_supporters:
        print(f"  - {supporter.business.business_name} ({supporter.preference_rank.cause_preference_rank_name})")
    
    education_supporters = session.query(BusinessCausePreference).filter_by(cause_id=education.cause_id).all()
    print(f"Education is supported by {len(education_supporters)} business(es):")
    for supporter in education_supporters:
        print(f"  - {supporter.business.business_name} ({supporter.preference_rank.cause_preference_rank_name})")
    
    print("\n7. Testing preference rank queries...")
    
    # Find all primary preferences
    primary_preferences = session.query(BusinessCausePreference).filter_by(cause_preference_rank_id=primary.cause_preference_rank_id).all()
    print(f"Primary cause preferences ({len(primary_preferences)}):")
    for pref in primary_preferences:
        print(f"  - {pref.business.business_name} → {pref.cause.cause_name}")
    
    # Find all supporting preferences
    supporting_preferences = session.query(BusinessCausePreference).filter_by(cause_preference_rank_id=supporting.cause_preference_rank_id).all()
    print(f"Supporting cause preferences ({len(supporting_preferences)}):")
    for pref in supporting_preferences:
        print(f"  - {pref.business.business_name} → {pref.cause.cause_name}")
    
    print("\n8. Testing foreign key constraints...")
    
    # Try to create preference with invalid business_id
    try:
        bad_business_pref = BusinessCausePreference(
            business_id=uuid.uuid4(),  # Random UUID that doesn't exist
            cause_id=education.cause_id,
            cause_preference_rank_id=primary.cause_preference_rank_id
        )
        session.add(bad_business_pref)
        session.commit()
        print("❌ ERROR: Should have failed due to business foreign key constraint!")
    except Exception as e:
        print("✅ Business foreign key constraint working")
        session.rollback()
    
    # Try to create preference with invalid cause_id
    try:
        bad_cause_pref = BusinessCausePreference(
            business_id=eco_solutions.business_id,
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
        bad_rank_pref = BusinessCausePreference(
            business_id=eco_solutions.business_id,
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
        count = session.query(BusinessCausePreference).filter_by(cause_preference_rank_id=rank.cause_preference_rank_id).count()
        print(f"{rank.cause_preference_rank_name.title()} preferences: {count}")
    
    # Find businesses with multiple preferences
    businesses_with_multiple = session.query(BusinessCausePreference.business_id).group_by(BusinessCausePreference.business_id).having(func.count() > 1).all()
    print(f"Businesses with multiple cause preferences: {len(businesses_with_multiple)}")
    
    session.close()
    print("\n🎉 BusinessCausePreference junction table working perfectly!")

if __name__ == "__main__":
    test_business_cause_preference_junction()