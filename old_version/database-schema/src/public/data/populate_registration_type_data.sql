/*
    Script creating definitions for registration types
*/
DO 
LANGUAGE plpgsql
$$

DECLARE   business_registration_type_code   CONSTANT   INT   := 1;
DECLARE   non_profit_registration_type_code CONSTANT   INT   := 2;
DECLARE   consumer_registration_type_code   CONSTANT   INT   := 3;

BEGIN

    /*
        Save registration types
    */

    CALL    save_registration_type(business_registration_type_code, 'business');
    CALL    save_registration_type(non_profit_registration_type_code, 'non-profit');
    CALL    save_registration_type(consumer_registration_type_code, 'consumer');

END $$;
/*
---------
Queries

SELECT * FROM registration_type;
*/
