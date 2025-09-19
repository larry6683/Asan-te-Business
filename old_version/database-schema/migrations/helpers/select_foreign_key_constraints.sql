/*
    Statement to select foreign keys from database
    change schema as needed
    modify where statement to optionally:
        1. select all foreign keys from schema
        2. select foreign keys from specific table(s)
        3. select foreign keys using a specific table
    
    NOTES:
        This is great for testing migration scripts!
*/
SELECT
    tc.constraint_name, 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_schema AS foreign_table_schema,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
AND 
(
    -- select foreign keys from specific table
    (
        tc.table_schema='public' 
        AND tc.table_name like '%'
    )
    OR
    -- find all places a table is used as a foreign table
    (
        ccu.table_schema='public' 
        AND ccu.table_name like '%'
    )
)