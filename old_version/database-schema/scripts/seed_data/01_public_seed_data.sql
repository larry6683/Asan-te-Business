-- Public Schema Seed Data SQL Script
-- This script creates test data for database integration in the public schema
-- Script will insert data in the correct order to respect foreign key constraints

DO $$
DECLARE
    -- User type IDs
    business_user_type_id UUID;
    beneficiary_user_type_id UUID;
    consumer_user_type_id UUID;
    
    -- Business size IDs
    small_business_size_id UUID;
    medium_business_size_id UUID;
    large_business_size_id UUID;
    
    -- Business user permission role IDs
    admin_business_user_permission_role_id UUID;
    team_member_business_user_permission_role_id UUID;
    removed_business_user_permission_role_id UUID;
    
    -- Social media type IDs
    unspecified_social_media_type_id UUID;
    linkedin_social_media_type_id UUID;
    instagram_social_media_type_id UUID;
    facebook_social_media_type_id UUID;
    
    -- Cause IDs
    homelessness_cause_id UUID;
    disadvantaged_populations_cause_id UUID;
    education_cause_id UUID;
    social_innovation_cause_id UUID;
    drought_fire_management_cause_id UUID;
    climate_advocacy_cause_id UUID;
    
    -- Cause preference rank IDs
    unranked_cause_preference_rank_id UUID;
    primary_cause_preference_rank_id UUID;
    supporting_cause_preference_rank_id UUID;
    
    -- Shop type IDs
    shopify_shop_type_id UUID;
    
    -- Business IDs - Using fixed UUIDs to ensure consistency with wallet script
    business1_id UUID := 'b1111111-1111-1111-1111-111111111111';
    business2_id UUID := 'b2222222-2222-2222-2222-222222222222';
    business3_id UUID := 'b3333333-3333-3333-3333-333333333333';
    
    -- App user IDs for businesses - Using fixed UUIDs for consistency
    -- Business 1 Users
    business1_admin1_id UUID := '11111111-1111-1111-1111-111111111101';
    business1_admin2_id UUID := '11111111-1111-1111-1111-111111111102';
    business1_team1_id UUID := '11111111-1111-1111-1111-111111111103';
    business1_team2_id UUID := '11111111-1111-1111-1111-111111111104';
    
    -- Business 2 Users
    business2_admin1_id UUID := '22222222-2222-2222-2222-222222222201';
    business2_admin2_id UUID := '22222222-2222-2222-2222-222222222202';
    business2_team1_id UUID := '22222222-2222-2222-2222-222222222203';
    business2_team2_id UUID := '22222222-2222-2222-2222-222222222204';
    
    -- Business 3 Users
    business3_admin1_id UUID := '33333333-3333-3333-3333-333333333301';
    business3_admin2_id UUID := '33333333-3333-3333-3333-333333333302';
    business3_team1_id UUID := '33333333-3333-3333-3333-333333333303';
    business3_team2_id UUID := '33333333-3333-3333-3333-333333333304';
    
BEGIN
    -- Get IDs by code from reference tables
    
    -- User types
    SELECT user_type_id INTO business_user_type_id FROM user_type WHERE code = 1;
    SELECT user_type_id INTO beneficiary_user_type_id FROM user_type WHERE code = 2;
    SELECT user_type_id INTO consumer_user_type_id FROM user_type WHERE code = 3;
    
    -- Business sizes
    SELECT business_size_id INTO small_business_size_id FROM business_size WHERE code = 1;
    SELECT business_size_id INTO medium_business_size_id FROM business_size WHERE code = 2;
    SELECT business_size_id INTO large_business_size_id FROM business_size WHERE code = 3;
    
    -- Business user permission roles
    SELECT business_user_permission_role_id INTO admin_business_user_permission_role_id 
    FROM business_user_permission_role WHERE code = 1;
    
    SELECT business_user_permission_role_id INTO team_member_business_user_permission_role_id 
    FROM business_user_permission_role WHERE code = 2;
    
    SELECT business_user_permission_role_id INTO removed_business_user_permission_role_id 
    FROM business_user_permission_role WHERE code = 3;
    
    -- Social media types
    SELECT social_media_type_id INTO unspecified_social_media_type_id FROM social_media_type WHERE code = 0;
    SELECT social_media_type_id INTO linkedin_social_media_type_id FROM social_media_type WHERE code = 1;
    SELECT social_media_type_id INTO instagram_social_media_type_id FROM social_media_type WHERE code = 2;
    SELECT social_media_type_id INTO facebook_social_media_type_id FROM social_media_type WHERE code = 3;
    
    -- Causes
    SELECT cause_id INTO homelessness_cause_id FROM cause WHERE code = 1;
    SELECT cause_id INTO disadvantaged_populations_cause_id FROM cause WHERE code = 4;
    SELECT cause_id INTO education_cause_id FROM cause WHERE code = 8;
    SELECT cause_id INTO social_innovation_cause_id FROM cause WHERE code = 12;
    SELECT cause_id INTO drought_fire_management_cause_id FROM cause WHERE code = 15;
    SELECT cause_id INTO climate_advocacy_cause_id FROM cause WHERE code = 16;
    
    -- Cause preference ranks
    SELECT cause_preference_rank_id INTO unranked_cause_preference_rank_id FROM cause_preference_rank WHERE code = 1;
    SELECT cause_preference_rank_id INTO primary_cause_preference_rank_id FROM cause_preference_rank WHERE code = 2;
    SELECT cause_preference_rank_id INTO supporting_cause_preference_rank_id FROM cause_preference_rank WHERE code = 3;
    
    -- Shop types
    SELECT shop_type_id INTO shopify_shop_type_id FROM shop_type WHERE code = 1;
    
    -- 1. First, create the app users (need these before business users)
    INSERT INTO app_user (app_user_id, user_type_id, email, mailing_list_signup)
    VALUES
        -- Business 1 Users
        (business1_admin1_id, business_user_type_id, 'admin1@business1.com', TRUE),
        (business1_admin2_id, business_user_type_id, 'admin2@business1.com', FALSE),
        (business1_team1_id, business_user_type_id, 'team1@business1.com', TRUE),
        (business1_team2_id, business_user_type_id, 'team2@business1.com', FALSE),
        
        -- Business 2 Users
        (business2_admin1_id, business_user_type_id, 'admin1@business2.com', TRUE),
        (business2_admin2_id, business_user_type_id, 'admin2@business2.com', FALSE),
        (business2_team1_id, business_user_type_id, 'team1@business2.com', TRUE),
        (business2_team2_id, business_user_type_id, 'team2@business2.com', FALSE),
        
        -- Business 3 Users
        (business3_admin1_id, business_user_type_id, 'admin1@business3.com', TRUE),
        (business3_admin2_id, business_user_type_id, 'admin2@business3.com', FALSE),
        (business3_team1_id, business_user_type_id, 'team1@business3.com', TRUE),
        (business3_team2_id, business_user_type_id, 'team2@business3.com', FALSE);

    -- 2. Create the three businesses
    INSERT INTO business (business_id, business_name, email, website_url, phone_number, location_city, location_state, business_size_id, business_description)
    VALUES
        (business1_id, 'Eco Solutions Inc.', 'contact@ecosolutions.com', 'https://ecosolutions.com', '555-123-4567', 'Seattle', 'WA', 
        medium_business_size_id, 'Sustainable product manufacturer focused on reducing environmental impact'),
        
        (business2_id, 'Tech Innovations Ltd', 'info@techinnovations.com', 'https://techinnovations.com', '555-234-5678', 'San Francisco', 'CA', 
        large_business_size_id, 'Technology company specializing in AI and machine learning solutions'),
        
        (business3_id, 'Local Harvest Co-op', 'hello@localharvest.org', 'https://localharvest.org', '555-345-6789', 'Portland', 'OR', 
        small_business_size_id, 'Community-owned grocery focusing on local, sustainable food production');

    -- 3. Create business users (linking businesses to app users)
    INSERT INTO business_user (business_id, app_user_id, business_user_permission_role_id)
    VALUES
        -- Business 1 Users
        (business1_id, business1_admin1_id, admin_business_user_permission_role_id),
        (business1_id, business1_admin2_id, admin_business_user_permission_role_id),
        (business1_id, business1_team1_id, team_member_business_user_permission_role_id),
        (business1_id, business1_team2_id, team_member_business_user_permission_role_id),
        
        -- Business 2 Users
        (business2_id, business2_admin1_id, admin_business_user_permission_role_id),
        (business2_id, business2_admin2_id, admin_business_user_permission_role_id),
        (business2_id, business2_team1_id, team_member_business_user_permission_role_id),
        (business2_id, business2_team2_id, team_member_business_user_permission_role_id),
        
        -- Business 3 Users
        (business3_id, business3_admin1_id, admin_business_user_permission_role_id),
        (business3_id, business3_admin2_id, admin_business_user_permission_role_id),
        (business3_id, business3_team1_id, team_member_business_user_permission_role_id),
        (business3_id, business3_team2_id, team_member_business_user_permission_role_id);

    -- 4. Add business social media
    INSERT INTO business_social_media (business_id, social_media_type_id, social_media_url)
    VALUES
        (business1_id, linkedin_social_media_type_id, 'https://linkedin.com/company/ecosolutions'),
        (business1_id, instagram_social_media_type_id, 'https://instagram.com/ecosolutions'),
        (business2_id, linkedin_social_media_type_id, 'https://linkedin.com/company/techinnovations'),
        (business3_id, facebook_social_media_type_id, 'https://facebook.com/localharvest');

    -- 5. Add business cause preferences
    INSERT INTO business_cause_preference (business_id, cause_id, cause_preference_rank_id)
    VALUES
        -- Business 1 Causes
        (business1_id, drought_fire_management_cause_id, primary_cause_preference_rank_id),
        (business1_id, climate_advocacy_cause_id, supporting_cause_preference_rank_id),
        
        -- Business 2 Causes
        (business2_id, education_cause_id, primary_cause_preference_rank_id),
        (business2_id, social_innovation_cause_id, supporting_cause_preference_rank_id),
        
        -- Business 3 Causes
        (business3_id, homelessness_cause_id, primary_cause_preference_rank_id),
        (business3_id, disadvantaged_populations_cause_id, supporting_cause_preference_rank_id);

    -- 6. Add business shops
    INSERT INTO business_shop (business_id, shop_type_id, shop_url)
    VALUES
        (business1_id, shopify_shop_type_id, 'https://ecosolutions.myshopify.com'),
        (business2_id, shopify_shop_type_id, 'https://techinnovations.myshopify.com'),
        (business3_id, shopify_shop_type_id, 'https://localharvest.myshopify.com');

    -- 7. Add impact links for businesses
    INSERT INTO business_impact_link (business_id, impact_link_url)
    VALUES
        (business1_id, 'https://ecosolutions.com/sustainability-report-2024'),
        (business1_id, 'https://ecosolutions.com/carbon-neutral-initiative'),
        (business2_id, 'https://techinnovations.com/community-outreach'),
        (business3_id, 'https://localharvest.org/food-security-program');

END $$;

/*
 * Use these commands to check that data was inserted correctly
 * Uncomment the query you want to run
 *
 * Basic entity verification
 SELECT * FROM app_user ORDER BY created_at DESC LIMIT 20;
 SELECT * FROM business ORDER BY created_at DESC LIMIT 10;
 SELECT * FROM business_user ORDER BY created_at DESC LIMIT 20;

 * Check business social media entries
 SELECT bs.*, smt.social_media_type_name 
 FROM business_social_media bs
 JOIN social_media_type smt ON bs.social_media_type_id = smt.social_media_type_id
 ORDER BY bs.created_at DESC;

 * Check business cause preferences
 SELECT bcp.*, c.cause_name, cpr.cause_preference_rank_name, cc.cause_category_name
 FROM business_cause_preference bcp
 JOIN cause c ON bcp.cause_id = c.cause_id
 JOIN cause_preference_rank cpr ON bcp.cause_preference_rank_id = cpr.cause_preference_rank_id
 JOIN cause_category cc ON c.cause_category_id = cc.cause_category_id
 ORDER BY bcp.created_at DESC;

 * Check business shops
 SELECT bs.*, st.shop_type_name, b.business_name
 FROM business_shop bs
 JOIN shop_type st ON bs.shop_type_id = st.shop_type_id
 JOIN business b ON bs.business_id = b.business_id
 ORDER BY bs.created_at DESC;

 * Check business impact links
 SELECT bil.*, b.business_name
 FROM business_impact_link bil
 JOIN business b ON bil.business_id = b.business_id
 ORDER BY bil.created_at DESC;

 * Business users with permission roles
 SELECT bu.*, bupr.business_user_permission_role_name, b.business_name, au.email
 FROM business_user bu
 JOIN business_user_permission_role bupr ON bu.business_user_permission_role_id = bupr.business_user_permission_role_id
 JOIN business b ON bu.business_id = b.business_id
 JOIN app_user au ON bu.app_user_id = au.app_user_id
 ORDER BY bu.created_at DESC;
*/