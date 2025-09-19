"""
Create test/seed data for development and testing.
This replaces the 01_public_seed_data.sql script.
"""

import sys
import os
import uuid

# Add the project root to Python path to import database_layer
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_layer.models import (
    Base, UserType, BusinessSize, Business, AppUser, BusinessUser,
    BusinessUserPermissionRole, SocialMediaType, BusinessSocialMedia,
    Cause, CausePreferenceRank, BusinessCausePreference, ShopType,
    BusinessShop, BusinessImpactLink
)

def create_session(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """Create database session"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session()

def create_seed_data(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """
    Create test data for development - equivalent to 01_public_seed_data.sql
    """
    print("Creating seed data...")
    
    try:
        engine, session = create_session(database_url)
        
        # Get reference data IDs
        business_user_type = session.query(UserType).filter_by(code=1).first()
        medium_business_size = session.query(BusinessSize).filter_by(code=2).first()
        large_business_size = session.query(BusinessSize).filter_by(code=3).first()
        small_business_size = session.query(BusinessSize).filter_by(code=1).first()
        
        admin_role = session.query(BusinessUserPermissionRole).filter_by(code=1).first()
        team_role = session.query(BusinessUserPermissionRole).filter_by(code=2).first()
        
        linkedin_type = session.query(SocialMediaType).filter_by(code=1).first()
        instagram_type = session.query(SocialMediaType).filter_by(code=2).first()
        facebook_type = session.query(SocialMediaType).filter_by(code=3).first()
        
        # Get causes
        homelessness_cause = session.query(Cause).filter_by(code=1).first()
        disadvantaged_cause = session.query(Cause).filter_by(code=4).first()
        education_cause = session.query(Cause).filter_by(code=8).first()
        social_innovation_cause = session.query(Cause).filter_by(code=12).first()
        drought_cause = session.query(Cause).filter_by(code=15).first()
        climate_cause = session.query(Cause).filter_by(code=16).first()
        
        primary_rank = session.query(CausePreferenceRank).filter_by(code=2).first()
        supporting_rank = session.query(CausePreferenceRank).filter_by(code=3).first()
        
        shopify_type = session.query(ShopType).filter_by(code=1).first()
        
        # Pre-defined UUIDs for consistency (matching the original SQL)
        business1_id = uuid.UUID('b1111111-1111-1111-1111-111111111111')
        business2_id = uuid.UUID('b2222222-2222-2222-2222-222222222222') 
        business3_id = uuid.UUID('b3333333-3333-3333-3333-333333333333')
        
        # Business 1 User IDs
        business1_admin1_id = uuid.UUID('11111111-1111-1111-1111-111111111101')
        business1_admin2_id = uuid.UUID('11111111-1111-1111-1111-111111111102')
        business1_team1_id = uuid.UUID('11111111-1111-1111-1111-111111111103')
        business1_team2_id = uuid.UUID('11111111-1111-1111-1111-111111111104')
        
        # Business 2 User IDs  
        business2_admin1_id = uuid.UUID('22222222-2222-2222-2222-222222222201')
        business2_admin2_id = uuid.UUID('22222222-2222-2222-2222-222222222202')
        business2_team1_id = uuid.UUID('22222222-2222-2222-2222-222222222203')
        business2_team2_id = uuid.UUID('22222222-2222-2222-2222-222222222204')
        
        # Business 3 User IDs
        business3_admin1_id = uuid.UUID('33333333-3333-3333-3333-333333333301')
        business3_admin2_id = uuid.UUID('33333333-3333-3333-3333-333333333302')
        business3_team1_id = uuid.UUID('33333333-3333-3333-3333-333333333303')
        business3_team2_id = uuid.UUID('33333333-3333-3333-3333-333333333304')
        
        print("Creating app users...")
        # Create app users first
        app_users = [
            # Business 1 Users
            AppUser(app_user_id=business1_admin1_id, user_type_id=business_user_type.user_type_id, 
                   email='admin1@business1.com', mailing_list_signup=True),
            AppUser(app_user_id=business1_admin2_id, user_type_id=business_user_type.user_type_id,
                   email='admin2@business1.com', mailing_list_signup=False),
            AppUser(app_user_id=business1_team1_id, user_type_id=business_user_type.user_type_id,
                   email='team1@business1.com', mailing_list_signup=True),
            AppUser(app_user_id=business1_team2_id, user_type_id=business_user_type.user_type_id,
                   email='team2@business1.com', mailing_list_signup=False),
            
            # Business 2 Users
            AppUser(app_user_id=business2_admin1_id, user_type_id=business_user_type.user_type_id,
                   email='admin1@business2.com', mailing_list_signup=True),
            AppUser(app_user_id=business2_admin2_id, user_type_id=business_user_type.user_type_id,
                   email='admin2@business2.com', mailing_list_signup=False),
            AppUser(app_user_id=business2_team1_id, user_type_id=business_user_type.user_type_id,
                   email='team1@business2.com', mailing_list_signup=True),
            AppUser(app_user_id=business2_team2_id, user_type_id=business_user_type.user_type_id,
                   email='team2@business2.com', mailing_list_signup=False),
            
            # Business 3 Users
            AppUser(app_user_id=business3_admin1_id, user_type_id=business_user_type.user_type_id,
                   email='admin1@business3.com', mailing_list_signup=True),
            AppUser(app_user_id=business3_admin2_id, user_type_id=business_user_type.user_type_id,
                   email='admin2@business3.com', mailing_list_signup=False),
            AppUser(app_user_id=business3_team1_id, user_type_id=business_user_type.user_type_id,
                   email='team1@business3.com', mailing_list_signup=True),
            AppUser(app_user_id=business3_team2_id, user_type_id=business_user_type.user_type_id,
                   email='team2@business3.com', mailing_list_signup=False)
        ]
        
        session.add_all(app_users)
        session.commit()
        print("App users created")
        
        print("Creating businesses...")
        # Create businesses
        businesses = [
            Business(
                business_id=business1_id,
                business_name='Eco Solutions Inc.',
                email='contact@ecosolutions.com',
                website_url='https://ecosolutions.com',
                phone_number='555-123-4567',
                location_city='Seattle',
                location_state='WA',
                business_size_id=medium_business_size.business_size_id,
                business_description='Sustainable product manufacturer focused on reducing environmental impact'
            ),
            Business(
                business_id=business2_id,
                business_name='Tech Innovations Ltd',
                email='info@techinnovations.com',
                website_url='https://techinnovations.com',
                phone_number='555-234-5678',
                location_city='San Francisco',
                location_state='CA',
                business_size_id=large_business_size.business_size_id,
                business_description='Technology company specializing in AI and machine learning solutions'
            ),
            Business(
                business_id=business3_id,
                business_name='Local Harvest Co-op',
                email='hello@localharvest.org',
                website_url='https://localharvest.org',
                phone_number='555-345-6789',
                location_city='Portland',
                location_state='OR',
                business_size_id=small_business_size.business_size_id,
                business_description='Community-owned grocery focusing on local, sustainable food production'
            )
        ]
        
        session.add_all(businesses)
        session.commit()
        print("Businesses created")
        
        print("Creating business users...")
        # Create business users (linking users to businesses)
        business_users = [
            # Business 1 Users
            BusinessUser(business_id=business1_id, app_user_id=business1_admin1_id, 
                        business_user_permission_role_id=admin_role.business_user_permission_role_id),
            BusinessUser(business_id=business1_id, app_user_id=business1_admin2_id,
                        business_user_permission_role_id=admin_role.business_user_permission_role_id),
            BusinessUser(business_id=business1_id, app_user_id=business1_team1_id,
                        business_user_permission_role_id=team_role.business_user_permission_role_id),
            BusinessUser(business_id=business1_id, app_user_id=business1_team2_id,
                        business_user_permission_role_id=team_role.business_user_permission_role_id),
            
            # Business 2 Users
            BusinessUser(business_id=business2_id, app_user_id=business2_admin1_id,
                        business_user_permission_role_id=admin_role.business_user_permission_role_id),
            BusinessUser(business_id=business2_id, app_user_id=business2_admin2_id,
                        business_user_permission_role_id=admin_role.business_user_permission_role_id),
            BusinessUser(business_id=business2_id, app_user_id=business2_team1_id,
                        business_user_permission_role_id=team_role.business_user_permission_role_id),
            BusinessUser(business_id=business2_id, app_user_id=business2_team2_id,
                        business_user_permission_role_id=team_role.business_user_permission_role_id),
            
            # Business 3 Users
            BusinessUser(business_id=business3_id, app_user_id=business3_admin1_id,
                        business_user_permission_role_id=admin_role.business_user_permission_role_id),
            BusinessUser(business_id=business3_id, app_user_id=business3_admin2_id,
                        business_user_permission_role_id=admin_role.business_user_permission_role_id),
            BusinessUser(business_id=business3_id, app_user_id=business3_team1_id,
                        business_user_permission_role_id=team_role.business_user_permission_role_id),
            BusinessUser(business_id=business3_id, app_user_id=business3_team2_id,
                        business_user_permission_role_id=team_role.business_user_permission_role_id)
        ]
        
        session.add_all(business_users)
        session.commit()
        print("Business users created")
        
        print("Creating business social media...")
        # Add business social media
        social_media = [
            BusinessSocialMedia(business_id=business1_id, social_media_type_id=linkedin_type.social_media_type_id,
                               social_media_url='https://linkedin.com/company/ecosolutions'),
            BusinessSocialMedia(business_id=business1_id, social_media_type_id=instagram_type.social_media_type_id,
                               social_media_url='https://instagram.com/ecosolutions'),
            BusinessSocialMedia(business_id=business2_id, social_media_type_id=linkedin_type.social_media_type_id,
                               social_media_url='https://linkedin.com/company/techinnovations'),
            BusinessSocialMedia(business_id=business3_id, social_media_type_id=facebook_type.social_media_type_id,
                               social_media_url='https://facebook.com/localharvest')
        ]
        
        session.add_all(social_media)
        session.commit()
        print(" Business social media created")
        
        print("Creating business cause preferences...")
        # Add business cause preferences
        cause_preferences = [
            # Business 1 Causes
            BusinessCausePreference(business_id=business1_id, cause_id=drought_cause.cause_id,
                                   cause_preference_rank_id=primary_rank.cause_preference_rank_id),
            BusinessCausePreference(business_id=business1_id, cause_id=climate_cause.cause_id,
                                   cause_preference_rank_id=supporting_rank.cause_preference_rank_id),
            
            # Business 2 Causes  
            BusinessCausePreference(business_id=business2_id, cause_id=education_cause.cause_id,
                                   cause_preference_rank_id=primary_rank.cause_preference_rank_id),
            BusinessCausePreference(business_id=business2_id, cause_id=social_innovation_cause.cause_id,
                                   cause_preference_rank_id=supporting_rank.cause_preference_rank_id),
            
            # Business 3 Causes
            BusinessCausePreference(business_id=business3_id, cause_id=homelessness_cause.cause_id,
                                   cause_preference_rank_id=primary_rank.cause_preference_rank_id),
            BusinessCausePreference(business_id=business3_id, cause_id=disadvantaged_cause.cause_id,
                                   cause_preference_rank_id=supporting_rank.cause_preference_rank_id)
        ]
        
        session.add_all(cause_preferences)
        session.commit()
        print("Business cause preferences created")
        
        print("Creating business shops...")
        # Add business shops
        shops = [
            BusinessShop(business_id=business1_id, shop_type_id=shopify_type.shop_type_id,
                        shop_url='https://ecosolutions.myshopify.com'),
            BusinessShop(business_id=business2_id, shop_type_id=shopify_type.shop_type_id,
                        shop_url='https://techinnovations.myshopify.com'),
            BusinessShop(business_id=business3_id, shop_type_id=shopify_type.shop_type_id,
                        shop_url='https://localharvest.myshopify.com')
        ]
        
        session.add_all(shops)
        session.commit()
        print("Business shops created")
        
        print("Creating business impact links...")
        # Add impact links for businesses
        impact_links = [
            BusinessImpactLink(business_id=business1_id, 
                              impact_link_url='https://ecosolutions.com/sustainability-report-2024'),
            BusinessImpactLink(business_id=business1_id,
                              impact_link_url='https://ecosolutions.com/carbon-neutral-initiative'),
            BusinessImpactLink(business_id=business2_id,
                              impact_link_url='https://techinnovations.com/community-outreach'),
            BusinessImpactLink(business_id=business3_id,
                              impact_link_url='https://localharvest.org/food-security-program')
        ]
        
        session.add_all(impact_links)
        session.commit()
        print("Business impact links created")
        
        session.close()
        print("\nAll seed data created successfully!")
        print("\nCreated:")
        print("- 12 app users (4 per business)")
        print("- 3 businesses (Eco Solutions, Tech Innovations, Local Harvest)")
        print("- 12 business user relationships")
        print("- 4 social media profiles")
        print("- 6 cause preferences") 
        print("- 3 business shops")
        print("- 4 impact links")
        
    except Exception as e:
        print(f"Error creating seed data: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        raise

if __name__ == "__main__":
    create_seed_data()