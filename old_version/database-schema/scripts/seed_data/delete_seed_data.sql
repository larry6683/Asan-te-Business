-- Corrected Cleanup Script
-- This script removes all inserted test data in the correct order to prevent foreign key constraint violations
-- NOTE: this may have not been updated in a minute, feel free to modify if it is not as comprehensive as needed

BEGIN;

-- 3. Delete business impact links
DELETE FROM business_impact_link
WHERE business_id IN (
    'b1111111-1111-1111-1111-111111111111',
    'b2222222-2222-2222-2222-222222222222',
    'b3333333-3333-3333-3333-333333333333'
);

-- 4. Delete business shops
DELETE FROM business_shop
WHERE business_id IN (
    'b1111111-1111-1111-1111-111111111111',
    'b2222222-2222-2222-2222-222222222222',
    'b3333333-3333-3333-3333-333333333333'
);

-- 5. Delete business cause preferences
DELETE FROM business_cause_preference
WHERE business_id IN (
    'b1111111-1111-1111-1111-111111111111',
    'b2222222-2222-2222-2222-222222222222',
    'b3333333-3333-3333-3333-333333333333'
);

-- 6. Delete business social media
DELETE FROM business_social_media
WHERE business_id IN (
    'b1111111-1111-1111-1111-111111111111',
    'b2222222-2222-2222-2222-222222222222',
    'b3333333-3333-3333-3333-333333333333'
);

-- 7. Delete business users
DELETE FROM business_user
WHERE business_id IN (
    'b1111111-1111-1111-1111-111111111111',
    'b2222222-2222-2222-2222-222222222222',
    'b3333333-3333-3333-3333-333333333333'
);

-- 8. Delete businesses
DELETE FROM business
WHERE business_id IN (
    'b1111111-1111-1111-1111-111111111111',
    'b2222222-2222-2222-2222-222222222222',
    'b3333333-3333-3333-3333-333333333333'
);

-- 9. Finally, delete app users
DELETE FROM app_user
WHERE app_user_id IN (
    '11111111-1111-1111-1111-111111111101',
    '11111111-1111-1111-1111-111111111102',
    '11111111-1111-1111-1111-111111111103',
    '11111111-1111-1111-1111-111111111104',
    '22222222-2222-2222-2222-222222222201',
    '22222222-2222-2222-2222-222222222202',
    '22222222-2222-2222-2222-222222222203',
    '22222222-2222-2222-2222-222222222204',
    '33333333-3333-3333-3333-333333333301',
    '33333333-3333-3333-3333-333333333302',
    '33333333-3333-3333-3333-333333333303',
    '33333333-3333-3333-3333-333333333304'
);

COMMIT;
/*
DELETE FROM business_impact_link;
DELETE FROM business_shop;
DELETE FROM business_cause_preference;
DELETE FROM business_social_media;
DELETE FROM business_user;
DELETE FROM business;
DELETE FROM app_user;
*/

/*
DROP TABLE IF EXISTS business_impact_link;
DROP TABLE IF EXISTS business_shop;
DROP TABLE IF EXISTS business_cause_preference;
DROP TABLE IF EXISTS business_social_media;
DROP TABLE IF EXISTS business_user;
DROP TABLE IF EXISTS beneficiary_user;
DROP TABLE IF EXISTS business;
DROP TABLE IF EXISTS app_user_registration_type;
DROP TABLE IF EXISTS app_user;
*/