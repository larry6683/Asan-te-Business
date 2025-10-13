/*
    psql script to create triggers, separated by schema

    1. public triggers

*/

\set QUIET on
SET client_min_messages TO WARNING;

/*

    PUBLIC TRIGGERS

*/

-- Domain trigger triggers

\i src/public/triggers/user_type_before_update_trigger.sql
\i src/public/triggers/app_user_before_insert_trigger.sql
\i src/public/triggers/app_user_before_update_trigger.sql
\i src/public/triggers/cause_category_before_update_trigger.sql
\i src/public/triggers/cause_before_update_trigger.sql
\i src/public/triggers/cause_preference_rank_before_update_trigger.sql
\i src/public/triggers/social_media_type_before_update_trigger.sql
\i src/public/triggers/shop_type_before_update_trigger.sql
\i src/public/triggers/registration_type_before_update_trigger.sql
\i src/public/triggers/app_user_registration_type_before_update_trigger.sql

-- Business trigger triggers

\i src/public/triggers/business_size_before_update_trigger.sql
\i src/public/triggers/business_user_permission_role_before_update_trigger.sql
\i src/public/triggers/business_type_before_update_trigger.sql
\i src/public/triggers/business_before_insert_trigger.sql
\i src/public/triggers/business_before_update_trigger.sql
\i src/public/triggers/business_user_before_update_trigger.sql
\i src/public/triggers/business_cause_preference_before_update_trigger.sql
\i src/public/triggers/business_social_media_before_update_trigger.sql
\i src/public/triggers/business_shop_before_update_trigger.sql
\i src/public/triggers/business_impact_link_before_update_trigger.sql

-- Beneficiary trigger triggers

\i src/public/triggers/beneficiary_size_before_update_trigger.sql
\i src/public/triggers/beneficiary_user_permission_role_before_update_trigger.sql
\i src/public/triggers/beneficiary_type_before_update_trigger.sql
\i src/public/triggers/beneficiary_before_insert_trigger.sql
\i src/public/triggers/beneficiary_before_update_trigger.sql
\i src/public/triggers/beneficiary_user_before_update_trigger.sql
\i src/public/triggers/beneficiary_cause_preference_before_update_trigger.sql
\i src/public/triggers/beneficiary_social_media_before_update_trigger.sql
\i src/public/triggers/beneficiary_shop_before_update_trigger.sql
