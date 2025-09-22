/*
    psql script to create tables, separated by schema

    some table definitions also include indexes

    1. public tables
*/

\set QUIET on
SET client_min_messages TO WARNING;

/*

    PUBLIC SCHEMA TABLES

*/

-- Domain related tables

\i src/public/tables/user_type.sql
\i src/public/tables/app_user.sql
\i src/public/tables/registration_type.sql
\i src/public/tables/app_user_registration_type.sql
\i src/public/tables/cause_category.sql
\i src/public/tables/cause.sql
\i src/public/tables/cause_preference_rank.sql
\i src/public/tables/social_media_type.sql
\i src/public/tables/shop_type.sql

-- Business related tables

\i src/public/tables/business_size.sql
\i src/public/tables/business_user_permission_role.sql
\i src/public/tables/business_type.sql
\i src/public/tables/business.sql
\i src/public/tables/business_user.sql
\i src/public/tables/business_cause_preference.sql
\i src/public/tables/business_social_media.sql
\i src/public/tables/business_shop.sql
\i src/public/tables/business_impact_link.sql

-- Beneficiary related tables

\i src/public/tables/beneficiary_size.sql
\i src/public/tables/beneficiary_user_permission_role.sql
\i src/public/tables/beneficiary_type.sql
\i src/public/tables/beneficiary.sql
\i src/public/tables/beneficiary_user.sql
\i src/public/tables/beneficiary_cause_preference.sql
\i src/public/tables/beneficiary_social_media.sql
\i src/public/tables/beneficiary_shop.sql
