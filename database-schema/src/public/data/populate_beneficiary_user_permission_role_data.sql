/*
    script creating definitions for beneficiary permission role
*/
DO 
LANGUAGE plpgsql
$$

DECLARE   admin_beneficiary_user_permission_role_code        CONSTANT   INT   := 1;
DECLARE   team_member_beneficiary_user_permission_role_code  CONSTANT   INT   := 2;
DECLARE   removed_beneficiary_user_permission_role_code      CONSTANT   INT   := 3;


BEGIN

    /*
        save beneficiary permission role
    */

    CALL    save_beneficiary_user_permission_role(admin_beneficiary_user_permission_role_code,        'Admin');
    CALL    save_beneficiary_user_permission_role(team_member_beneficiary_user_permission_role_code,  'Team Member');
    CALL save_beneficiary_user_permission_role(removed_beneficiary_user_permission_role_code,         'Removed');


END $$;
/*
---------
Queries

select * from beneficiary_user_permission_role
*/