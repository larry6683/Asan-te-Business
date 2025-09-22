/*
    script creating definitions for business permission role
*/
DO 
LANGUAGE plpgsql
$$

DECLARE   admin_business_user_permission_role_code         CONSTANT   INT       := 1;
DECLARE   team_member_business_user_permission_role_code   CONSTANT   INT       := 2;
DECLARE   removed_business_user_permission_role_code      CONSTANT    INT       := 3;


BEGIN

    /*
        save business permission role
    */

    CALL save_business_user_permission_role(admin_business_user_permission_role_code,        'Admin');
    CALL save_business_user_permission_role(team_member_business_user_permission_role_code,  'Team Member');
    CALL save_business_user_permission_role(removed_business_user_permission_role_code,      'Removed');


END $$;
/*
---------
Queries

select * from business_user_permission_role
*/