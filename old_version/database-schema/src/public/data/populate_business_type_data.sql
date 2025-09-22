/*
    Script creating definitions for business types
*/
DO 
LANGUAGE plpgsql
$$

DECLARE   business_type_code    CONSTANT   INT   := 1;

BEGIN

    /*
        Save business types
    */

    CALL    save_business_type(business_type_code, 'business');

END $$;
/*
---------
Queries

SELECT * FROM business_type;
*/
