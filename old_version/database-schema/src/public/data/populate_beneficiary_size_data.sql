/*
    script creating definitions for beneficiary sizes
*/
DO 
LANGUAGE plpgsql
$$

DECLARE   small_beneficiary_size_code_key     CONSTANT   INT   := 1;
DECLARE   medium_beneficiary_size_code_key    CONSTANT   INT   := 2;
DECLARE   large_beneficiary_size_code_key     CONSTANT   INT   := 3;

BEGIN

    /*
        save beneficiary sizes
    */

    CALL    save_beneficiary_size(small_beneficiary_size_code_key,  'small');
    CALL    save_beneficiary_size(medium_beneficiary_size_code_key, 'medium');
    CALL    save_beneficiary_size(large_beneficiary_size_code_key,  'large');

END $$;
/*
---------
Queries

select * from beneficiary_size
*/