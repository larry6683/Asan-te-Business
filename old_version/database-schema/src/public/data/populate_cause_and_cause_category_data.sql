/*
    script creating definitions for cause categories
*/

DO 
LANGUAGE plpgsql
$$
/*
    cause categories
*/
DECLARE community_cause_category_code           CONSTANT    INT     := 1;
DECLARE social_cause_category_code              CONSTANT    INT     := 2;
DECLARE innovation_cause_category_code          CONSTANT    INT     := 3;
DECLARE environment_cause_category_code         CONSTANT    INT     := 4;
DECLARE emergency_reflief_cause_category_code   CONSTANT    INT     := 5;

--
-- causes
--

-- Community Causes
DECLARE homelessness_cause_code                 CONSTANT    INT     := 1;
DECLARE events_advocacy_cause_code              CONSTANT    INT     := 2;
DECLARE first_responders_cause_code             CONSTANT    INT     := 3;
DECLARE disadvantaged_populations_cause_code    CONSTANT    INT     := 4;
DECLARE schools_techers_cause_code              CONSTANT    INT     := 5;

-- Social Causes
DECLARE sports_cause_code                       CONSTANT    INT     := 6;
DECLARE arts_cause_code                         CONSTANT    INT     := 7;
DECLARE education_cause_code                    CONSTANT    INT     := 8;
DECLARE social_justice_cause_code               CONSTANT    INT     := 9;
DECLARE mental_health_and_wellbeing_cause_code  CONSTANT    INT     := 10;


-- Innovation Causes
DECLARE youth_empowerment_cause_code            CONSTANT    INT     := 11;
DECLARE social_innovation_cause_code            CONSTANT    INT     := 12;
DECLARE sustainable_innovation_cause_code       CONSTANT    INT     := 13;
DECLARE social_entrepreneurship_cause_code      CONSTANT    INT     := 14;


-- Environment Causes
DECLARE drought_and_fire_management_cause_code  CONSTANT    INT     := 15;
DECLARE climate_advocacy_cause_code             CONSTANT    INT     := 16;
DECLARE climate_refugees_cause_code             CONSTANT    INT     := 17;
DECLARE water_sustainability_cause_code         CONSTANT    INT     := 18;


-- First Responder Causes
DECLARE emergency_relief_cause_code             CONSTANT    INT     := 19;

BEGIN

    /*
        save cause categories
    */

    CALL save_cause_category(community_cause_category_code,         'Community');
    CALL save_cause_category(social_cause_category_code,            'Social');
    CALL save_cause_category(innovation_cause_category_code,        'Innovation');
    CALL save_cause_category(environment_cause_category_code,       'Environment');
    CALL save_cause_category(emergency_reflief_cause_category_code, 'Emergency Relief');

    /*
        save causes
    */

    -- Community Causes
    CALL save_cause(homelessness_cause_code,                'Homelessness',                 community_cause_category_code);
    CALL save_cause(events_advocacy_cause_code,             'Events & Advocacy',            community_cause_category_code);
    CALL save_cause(first_responders_cause_code,            'First Responders',             community_cause_category_code);
    CALL save_cause(disadvantaged_populations_cause_code,   'Disadvantaged Populations',    community_cause_category_code);
    CALL save_cause(schools_techers_cause_code,             'Schools & Teachers',           community_cause_category_code);

    -- Social Causes
    CALL save_cause(sports_cause_code,                      'Sports',                       social_cause_category_code);
    CALL save_cause(arts_cause_code,                        'Arts',                         social_cause_category_code);
    CALL save_cause(education_cause_code,                   'Education',                    social_cause_category_code);
    CALL save_cause(social_justice_cause_code,              'Social Justice',               social_cause_category_code);
    CALL save_cause(mental_health_and_wellbeing_cause_code, 'Mental Health & Wellbeing',    social_cause_category_code);


    -- Innovation Causes
    CALL save_cause(youth_empowerment_cause_code,           'Youth Empowerment',            innovation_cause_category_code);
    CALL save_cause(social_innovation_cause_code,           'Social Innovation',            innovation_cause_category_code);
    CALL save_cause(sustainable_innovation_cause_code,      'Sustainable Innovation',       innovation_cause_category_code);
    CALL save_cause(social_entrepreneurship_cause_code,     'Social Entrepreneurship',      innovation_cause_category_code);


    -- Environment Causes
    CALL save_cause(drought_and_fire_management_cause_code, 'Drought & Fire Management',    environment_cause_category_code);
    CALL save_cause(climate_advocacy_cause_code,            'Climate Advocacy',             environment_cause_category_code);
    CALL save_cause(climate_refugees_cause_code,            'Climate Refugees',             environment_cause_category_code);
    CALL save_cause(water_sustainability_cause_code,        'Water Sustainability',         environment_cause_category_code);


    -- First Responder Causes
    CALL save_cause(emergency_relief_cause_code,             'Emergency Relief', emergency_reflief_cause_category_code);

END;
$$;

/*
---------
Queries

select * from cause_category

select * from cause

SELECT  c.code AS cause_code,
        cause_name,
        cc.code AS cause_category_code,
        cc.cause_category_name
FROM    cause AS c
JOIN    cause_category AS cc on cc.cause_category_id = c.cause_category_id
--------------
Commands
delete from cause;
delete from cause_category;

CALL save_cause(17,    'Water Sustainability',     10);
*/