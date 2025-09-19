/*
    Script to drop all database objects utilizing cascade if possible
    works with public schema only
*/
/*
-- Script to drop all tables, functions, triggers, and procedures in the public schema
-- NOTE: Run this with care! This will delete all data in the public schema

-- Disable notices to reduce output noise
SET client_min_messages TO warning;

-- Disable foreign key checks during the operation
SET session_replication_role = 'replica';

-- Drop all triggers
DO $$
DECLARE
    trigger_rec RECORD;
    table_rec RECORD;
BEGIN
    FOR table_rec IN 
        SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    LOOP
        FOR trigger_rec IN
            SELECT tgname FROM pg_trigger t
            JOIN pg_class c ON t.tgrelid = c.oid
            JOIN pg_namespace n ON c.relnamespace = n.oid
            WHERE n.nspname = 'public' AND c.relname = table_rec.tablename
            AND NOT t.tgisinternal  -- Skip internal triggers
        LOOP
            EXECUTE format('DROP TRIGGER IF EXISTS %I ON public.%I CASCADE', 
                           trigger_rec.tgname, table_rec.tablename);
        END LOOP;
    END LOOP;
END;
$$;

-- Drop all tables
DO $$
DECLARE
    tables_rec RECORD;
BEGIN
    FOR tables_rec IN 
        SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP TABLE IF EXISTS public.%I CASCADE', tables_rec.tablename);
    END LOOP;
END;
$$;

-- Drop all functions and procedures
DO $$
DECLARE
    func_rec RECORD;
BEGIN
    FOR func_rec IN 
        SELECT n.nspname, p.proname, pg_get_function_identity_arguments(p.oid) AS args
        FROM pg_proc p
        JOIN pg_namespace n ON p.pronamespace = n.oid
        WHERE n.nspname = 'public'
    LOOP
        -- Handle both functions and procedures
        BEGIN
            EXECUTE format('DROP FUNCTION IF EXISTS public.%I(%s) CASCADE', 
                          func_rec.proname, func_rec.args);
        EXCEPTION WHEN OTHERS THEN
            BEGIN
                EXECUTE format('DROP PROCEDURE IF EXISTS public.%I(%s) CASCADE', 
                              func_rec.proname, func_rec.args);
            EXCEPTION WHEN OTHERS THEN
                RAISE NOTICE 'Could not drop function or procedure: %', func_rec.proname;
            END;
        END;
    END LOOP;
END;
$$;

-- Drop all types
DO $$
DECLARE
    type_rec RECORD;
BEGIN
    FOR type_rec IN 
        SELECT typname FROM pg_type t
        JOIN pg_namespace n ON t.typnamespace = n.oid
        WHERE n.nspname = 'public'
        AND t.typtype = 'c'  -- Only composite types
        AND t.typname NOT LIKE 'pg_%'  -- Exclude system types
        AND t.typname NOT LIKE '_%'    -- Exclude system types
    LOOP
        EXECUTE format('DROP TYPE IF EXISTS public.%I CASCADE', type_rec.typname);
    END LOOP;
END;
$$;

-- Drop all views
DO $$
DECLARE
    view_rec RECORD;
BEGIN
    FOR view_rec IN 
        SELECT table_name FROM information_schema.views
        WHERE table_schema = 'public'
    LOOP
        EXECUTE format('DROP VIEW IF EXISTS public.%I CASCADE', view_rec.table_name);
    END LOOP;
END;
$$;

-- Report completion
DO $$
BEGIN
    RAISE NOTICE 'All tables, functions, procedures, triggers, types, and views in the public schema have been dropped.';
END;
$$;

-- Reset session settings
SET session_replication_role = 'origin';
SET client_min_messages TO notice;
*/