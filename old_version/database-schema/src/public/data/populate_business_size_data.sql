/*
    script creating definitions for business sizes
*/
DO 
LANGUAGE plpgsql
$$

DECLARE   small_business_size_code     CONSTANT   INT   := 1;
DECLARE   medium_business_size_code    CONSTANT   INT   := 2;
DECLARE   large_business_size_code     CONSTANT   INT   := 3;

BEGIN

    /*
        save business sizes
    */

    CALL    save_business_size(small_business_size_code,    'small');
    CALL    save_business_size(medium_business_size_code,   'medium');
    CALL    save_business_size(large_business_size_code,    'large');

END $$;
/*
---------
Queries

select * from business_size
*/