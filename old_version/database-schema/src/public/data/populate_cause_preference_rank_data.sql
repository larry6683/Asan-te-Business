/*
    Script creating definitions for cause preference rank
*/
DO 
LANGUAGE plpgsql
$$

DECLARE   unranked_cause_preference_rank_code     INT := 1;
DECLARE   primary_cause_preference_rank_code      INT := 2;
DECLARE   supporting_cause_preference_rank_code   INT := 3;

BEGIN

    /*
        Save cause preference rank
    */

    CALL    save_cause_preference_rank(unranked_cause_preference_rank_code,     'unranked');
    CALL    save_cause_preference_rank(primary_cause_preference_rank_code,      'primary');
    CALL    save_cause_preference_rank(supporting_cause_preference_rank_code,   'supporting');

END $$;

/*
---------
Queries

SELECT * FROM cause_preference_rank;
*/
