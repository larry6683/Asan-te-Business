/*
    statement to select all constraints on a table
    useful for testing migrations
    useful for dropping constraints during migration
*/
SELECT conname
FROM pg_catalog.pg_constraint con
INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid
INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace
WHERE rel.relname = 'business';

/*
DO
LANGUAGE plpgsql
$$
DECLARE r RECORD;
BEGIN
    -- stuff

    RAISE NOTICE 'drop constraints from {table_name}';
    FOR r IN (
        SELECT conname
        FROM pg_catalog.pg_constraint con
        INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid
        INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace
        WHERE rel.relname = '')
    LOOP
        EXECUTE format('ALTER TABLE {table_name} DROP CONSTRAINT %s', i.conname);
    END LOOP;

    -- stuff
End;
$$;
*/