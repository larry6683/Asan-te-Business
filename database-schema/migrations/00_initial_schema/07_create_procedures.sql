/*
    psql script to create stored procedures, separated by schema

    1. public procedures
    
*/

\set QUIET on
SET client_min_messages TO WARNING;

/*

    PUBLIC PROCEDURES

*/

\i src/public/procedures/save_beneficiary_size.sql
\i src/public/procedures/save_beneficiary_type.sql
\i src/public/procedures/save_beneficiary_user_permission_role.sql
\i src/public/procedures/save_business_size.sql
\i src/public/procedures/save_business_type.sql
\i src/public/procedures/save_business_user_permission_role.sql
\i src/public/procedures/save_cause_category.sql
\i src/public/procedures/save_cause_preference_rank.sql
\i src/public/procedures/save_cause.sql
\i src/public/procedures/save_registration_type.sql
\i src/public/procedures/save_shop_type.sql
\i src/public/procedures/save_social_media_type.sql
\i src/public/procedures/save_user_type.sql
