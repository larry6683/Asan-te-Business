/*
    psql script to execute data population, separated by schema

    1. public data population
    
*/

\set QUIET on
SET client_min_messages TO WARNING;

/*

    PUBLIC DATA POPULATION

*/

\i src/public/data/populate_beneficiary_size_data.sql
\i src/public/data/populate_beneficiary_type_data.sql
\i src/public/data/populate_beneficiary_user_permission_role_data.sql
\i src/public/data/populate_business_size_data.sql
\i src/public/data/populate_business_type_data.sql
\i src/public/data/populate_business_user_permission_role_data.sql

\i src/public/data/populate_cause_and_cause_category_data.sql
\i src/public/data/populate_cause_preference_rank_data.sql
\i src/public/data/populate_registration_type_data.sql
\i src/public/data/populate_shop_type_data.sql
\i src/public/data/populate_social_media_type_data.sql
\i src/public/data/populate_user_type_data.sql
