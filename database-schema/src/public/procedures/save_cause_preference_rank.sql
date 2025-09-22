CREATE OR REPLACE PROCEDURE save_cause_preference_rank(
    code INT,
    cause_preference_rank_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO cause_preference_rank (code, cause_preference_rank_name)
    VALUES (code, cause_preference_rank_name)
    ON CONFLICT ON CONSTRAINT cause_preference_rank_code_key
    DO UPDATE
        SET cause_preference_rank_name = EXCLUDED.cause_preference_rank_name;
END
$$;

/*
CALL save_cause_preference_rank(1, 'boop-cause-preference-rank');

SELECT  *
FROM    cause_preference_rank;
*/