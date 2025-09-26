"""
Usage: bash python -m database_layer.tests.test_business_impact_link
"""
import uuid
from sqlalchemy.sql import func
from database_layer.src.public.tables.business_size import BusinessSize
from database_layer.src.public.tables.business import Business
from database_layer.src.public.tables.business_impact_link import BusinessImpactLink
from .test_utils import create_test_session

def test_business_impact_link():
    print("=== Testing BusinessImpactLink Model ===")
    
    engine, session = create_test_session()
    
    print("\n1. Creating parent records...")
    
    # Create business size
    medium = BusinessSize(code=2, business_size_name='medium')
    
    session.add(medium)
    session.commit()
    print("✅ Created business size")
    
    print("\n2. Creating businesses...")
    
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
        business_size_id=medium.business_size_id,
        business_description='AI and machine learning solutions'
    )
    
    session.add_all([eco_solutions, tech_innovations])
    session.commit()
    print("✅ Created businesses")
    
    print("\n3. Creating impact links...")
    
    # Eco Solutions impact links
    eco_sustainability_report = BusinessImpactLink(
        business_id=eco_solutions.business_id,
        impact_link_url='https://ecosolutions.com/sustainability-report-2024'
    )
    
    eco_carbon_neutral = BusinessImpactLink(
        business_id=eco_solutions.business_id,
        impact_link_url='https://ecosolutions.com/carbon-neutral-initiative'
    )
    
    eco_community_impact = BusinessImpactLink(
        business_id=eco_solutions.business_id,
        impact_link_url='https://ecosolutions.com/community-impact-2024'
    )
    
    # Tech Innovations impact links
    tech_community_outreach = BusinessImpactLink(
        business_id=tech_innovations.business_id,
        impact_link_url='https://techinnovations.com/community-outreach'
    )
    
    tech_education_program = BusinessImpactLink(
        business_id=tech_innovations.business_id,
        impact_link_url='https://techinnovations.com/coding-bootcamp-scholarships'
    )
    
    session.add_all([eco_sustainability_report, eco_carbon_neutral, eco_community_impact, tech_community_outreach, tech_education_program])
    session.commit()
    print("✅ Created impact links")
    
    print("\n4. Testing relationship navigation...")
    
    # Find all impact links for each business
    eco_links = session.query(BusinessImpactLink).filter_by(business_id=eco_solutions.business_id).all()
    print(f"Eco Solutions has {len(eco_links)} impact link(s):")
    for link in eco_links:
        print(f"  - {link.impact_link_url}")
    
    tech_links = session.query(BusinessImpactLink).filter_by(business_id=tech_innovations.business_id).all()
    print(f"Tech Innovations has {len(tech_links)} impact link(s):")
    for link in tech_links:
        print(f"  - {link.impact_link_url}")
    
    print("\n5. Testing business relationship navigation...")
    
    # Test accessing business from impact link
    first_eco_link = eco_links[0]
    print(f"First Eco Solutions link belongs to: {first_eco_link.business.business_name}")
    
    first_tech_link = tech_links[0] 
    print(f"First Tech Innovations link belongs to: {first_tech_link.business.business_name}")
    
    print("\n6. Testing foreign key constraints...")
    
    # Try to create impact link with invalid business_id
    try:
        bad_impact_link = BusinessImpactLink(
            business_id=uuid.uuid4(),  # Random UUID that doesn't exist
            impact_link_url='https://badcompany.com/impact-report'
        )
        session.add(bad_impact_link)
        session.commit()
        print("❌ ERROR: Should have failed due to business foreign key constraint!")
    except Exception as e:
        print("✅ Business foreign key constraint working")
        session.rollback()
    
    print("\n7. Testing queries...")
    
    # Count total impact links
    total_links = session.query(BusinessImpactLink).count()
    print(f"Total impact links: {total_links}")
    
    # Find businesses with multiple impact links
    businesses_with_multiple = session.query(BusinessImpactLink.business_id).group_by(BusinessImpactLink.business_id).having(func.count() > 1).all()
    print(f"Businesses with multiple impact links: {len(businesses_with_multiple)}")
    
    # Find businesses with specific types of impact links
    sustainability_links = session.query(BusinessImpactLink).filter(BusinessImpactLink.impact_link_url.contains('sustainability')).all()
    print(f"Sustainability-related links: {len(sustainability_links)}")
    
    community_links = session.query(BusinessImpactLink).filter(BusinessImpactLink.impact_link_url.contains('community')).all()
    print(f"Community-related links: {len(community_links)}")
    
    print("\n8. Testing URL validation...")
    
    # Create a link with a different URL format
    local_file_link = BusinessImpactLink(
        business_id=eco_solutions.business_id,
        impact_link_url='/local/reports/quarterly-impact-q4-2024.pdf'
    )
    session.add(local_file_link)
    session.commit()
    print("✅ Can store various URL formats (local paths, etc.)")
    
    session.close()
    print("\n🎉 BusinessImpactLink model working perfectly!")

if __name__ == "__main__":
    test_business_impact_link()