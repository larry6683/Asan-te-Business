/*
    psql script to create functions, separated by schema

    1. public functions

*/

\set QUIET on
SET client_min_messages TO WARNING;

/*

    PUBLIC FUNCTIONS

*/

-- Domain trigger functions

\i src/public/functions/user_type_before_update_triggerfn.sql
\i src/public/functions/app_user_before_insert_triggerfn.sql
\i src/public/functions/app_user_before_update_triggerfn.sql
\i src/public/functions/cause_category_before_update_triggerfn.sql
\i src/public/functions/cause_before_update_triggerfn.sql
\i src/public/functions/cause_preference_rank_before_update_triggerfn.sql
\i src/public/functions/social_media_type_before_update_triggerfn.sql
\i src/public/functions/shop_type_before_update_triggerfn.sql
\i src/public/functions/registration_type_before_update_triggerfn.sql
\i src/public/functions/app_user_registration_type_before_update_triggerfn.sql

-- Business trigger functions

\i src/public/functions/business_size_before_update_triggerfn.sql
\i src/public/functions/business_user_permission_role_before_update_triggerfn.sql
\i src/public/functions/business_before_insert_triggerfn.sql
\i src/public/functions/business_before_update_triggerfn.sql
\i src/public/functions/business_type_before_update_triggerfn.sql
\i src/public/functions/business_user_before_update_triggerfn.sql
\i src/public/functions/business_cause_preference_before_update_triggerfn.sql
\i src/public/functions/business_social_media_before_update_triggerfn.sql
\i src/public/functions/business_shop_before_update_triggerfn.sql
\i src/public/functions/business_impact_link_before_update_triggerfn.sql

-- Beneficiary trigger functions

\i src/public/functions/beneficiary_size_before_update_triggerfn.sql
\i src/public/functions/beneficiary_user_permission_role_before_update_triggerfn.sql
\i src/public/functions/beneficiary_before_insert_triggerfn.sql
\i src/public/functions/beneficiary_before_update_triggerfn.sql
\i src/public/functions/beneficiary_type_before_update_triggerfn.sql
\i src/public/functions/beneficiary_user_before_update_triggerfn.sql
\i src/public/functions/beneficiary_cause_preference_before_update_triggerfn.sql
\i src/public/functions/beneficiary_social_media_before_update_triggerfn.sql
\i src/public/functions/beneficiary_shop_before_update_triggerfn.sql
