/*
    Script creating definitions for beneficiary types
*/
DO 
LANGUAGE plpgsql
$$

DECLARE   non_profit_beneficiary_type_code    CONSTANT   INT   := 1;

BEGIN

    /*
        Save beneficiary types
    */

    CALL    save_beneficiary_type(non_profit_beneficiary_type_code, 'non-profit');

END $$;
/*
---------
Queries

SELECT * FROM beneficiary_type;
*/
