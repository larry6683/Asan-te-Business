/*
    script populating definitions for social media link types
*/
DO
LANGUAGE plpgsql
$$
DECLARE
    unspecified_social_media_type_code           CONSTANT       INT     := 0;
    linkedin_social_media_type_code              CONSTANT       INT     := 1;
    instagram_social_media_type_code             CONSTANT       INT     := 2;
    facebook_social_media_type_code              CONSTANT       INT     := 3;
BEGIN

    /*
        save social media types
    */

    CALL    save_social_media_type(unspecified_social_media_type_code, 'unspecified');
    CALL    save_social_media_type(linkedin_social_media_type_code,    'linkedin');
    CALL    save_social_media_type(instagram_social_media_type_code,   'instagram');
    CALL    save_social_media_type(facebook_social_media_type_code,    'facebook');

END 
$$;

/*
QUERIES
select * from social_media_type
*/