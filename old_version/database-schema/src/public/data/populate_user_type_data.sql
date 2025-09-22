/*
    script creating definitions for user type
*/
DO 
LANGUAGE plpgsql
$$

DECLARE     business_user_type_code         CONSTANT    INT     := 1;
DECLARE     beneficiary_user_type_code      CONSTANT    INT     := 2;
DECLARE     consumer_user_type_code         CONSTANT    INT     := 3;

BEGIN

    /*
        save user types
    */
    
    CALL    save_user_type(business_user_type_code,     'business user');
    CALL    save_user_type(beneficiary_user_type_code,  'beneficiary user');
    CALL    save_user_type(consumer_user_type_code,     'consumer user');

END $$;
/*
---------
Queries

select * from user_type
*/