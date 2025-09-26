"""
Drop all database objects in the public schema.
This replaces drop_database_objects.sql script.
WARNING: This will completely reset your database - use with extreme caution!
"""

import sys
import os
import argparse

# Add the project root to Python path to import database_layer
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from database_layer.src.public.tables import Base

def create_session(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """Create database session"""
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return engine, Session()

def drop_all_database_objects(database_url="postgresql://asante_dev:password@localhost:5432/postgres", confirm=False):
    """
    Drop ALL database objects in the public schema - equivalent to drop_database_objects.sql
    This is the nuclear option that completely resets your database.
    
    Args:
        database_url: Database connection URL
        confirm: Must be True to actually execute (safety mechanism)
    """
    if not confirm:
        print("⚠️  WARNING: This will DROP ALL database objects in the public schema!")
        print("This includes:")
        print("- All tables and their data")
        print("- All functions and procedures") 
        print("- All triggers")
        print("- All views")
        print("- All sequences")
        print("- All custom types")
        print("\nTo proceed, you must explicitly confirm by setting confirm=True")
        print("Or use the --confirm flag if running from command line")
        return False
    
    print("🚨 DROPPING ALL DATABASE OBJECTS - THIS CANNOT BE UNDONE!")
    
    try:
        engine, session = create_session(database_url)
        
        # Disable foreign key checks and notices to reduce output noise
        session.execute(text("SET session_replication_role = 'replica'"))
        session.execute(text("SET client_min_messages TO warning"))
        
        print("Dropping all triggers...")
        # Drop all triggers first
        trigger_drop_sql = """
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
        """
        session.execute(text(trigger_drop_sql))
        
        print("Dropping all tables...")
        # Drop all tables with CASCADE
        table_drop_sql = """
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
        """
        session.execute(text(table_drop_sql))
        
        print("Dropping all functions and procedures...")
        # Drop all functions and procedures
        function_drop_sql = """
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
                -- Try as function first, then as procedure
                BEGIN
                    EXECUTE format('DROP FUNCTION IF EXISTS public.%I(%s) CASCADE', 
                                  func_rec.proname, func_rec.args);
                EXCEPTION WHEN OTHERS THEN
                    BEGIN
                        EXECUTE format('DROP PROCEDURE IF EXISTS public.%I(%s) CASCADE', 
                                      func_rec.proname, func_rec.args);
                    EXCEPTION WHEN OTHERS THEN
                        -- Ignore if neither works
                        NULL;
                    END;
                END;
            END LOOP;
        END;
        $$;
        """
        session.execute(text(function_drop_sql))
        
        print("Dropping all sequences...")
        # Drop all sequences
        sequence_drop_sql = """
        DO $$
        DECLARE
            seq_rec RECORD;
        BEGIN
            FOR seq_rec IN 
                SELECT sequencename FROM pg_sequences WHERE schemaname = 'public'
            LOOP
                EXECUTE format('DROP SEQUENCE IF EXISTS public.%I CASCADE', seq_rec.sequencename);
            END LOOP;
        END;
        $$;
        """
        session.execute(text(sequence_drop_sql))
        
        print("Dropping all views...")
        # Drop all views
        view_drop_sql = """
        DO $$
        DECLARE
            view_rec RECORD;
        BEGIN
            FOR view_rec IN 
                SELECT viewname FROM pg_views WHERE schemaname = 'public'
            LOOP
                EXECUTE format('DROP VIEW IF EXISTS public.%I CASCADE', view_rec.viewname);
            END LOOP;
        END;
        $$;
        """
        session.execute(text(view_drop_sql))
        
        print("Dropping all custom types...")
        # Drop all custom types (enums, composite types, etc.)
        type_drop_sql = """
        DO $$
        DECLARE
            type_rec RECORD;
        BEGIN
            FOR type_rec IN 
                SELECT typname FROM pg_type t
                JOIN pg_namespace n ON t.typnamespace = n.oid
                WHERE n.nspname = 'public' 
                AND t.typtype IN ('e', 'c')  -- enums and composite types
            LOOP
                EXECUTE format('DROP TYPE IF EXISTS public.%I CASCADE', type_rec.typname);
            END LOOP;
        END;
        $$;
        """
        session.execute(text(type_drop_sql))
        
        # Commit all changes
        session.commit()
        
        # Re-enable foreign key checks
        session.execute(text("SET session_replication_role = 'origin'"))
        session.commit()
        
        session.close()
        
        print("\n✅ ALL DATABASE OBJECTS DROPPED SUCCESSFULLY!")
        print("\nThe public schema is now completely empty.")
        print("You can now run populate_database.py to recreate everything from scratch.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error dropping database objects: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        raise

def verify_empty_schema(database_url="postgresql://asante_dev:password@localhost:5432/postgres"):
    """
    Verify that the public schema is empty after dropping objects
    """
    print("\n🔍 Verifying empty schema...")
    
    try:
        engine, session = create_session(database_url)
        
        # Check for remaining objects
        checks = [
            ("Tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"),
            ("Functions", "SELECT COUNT(*) FROM information_schema.routines WHERE routine_schema = 'public'"),
            ("Sequences", "SELECT COUNT(*) FROM information_schema.sequences WHERE sequence_schema = 'public'"),
            ("Views", "SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public'"),
            ("Types", "SELECT COUNT(*) FROM pg_type t JOIN pg_namespace n ON t.typnamespace = n.oid WHERE n.nspname = 'public' AND t.typtype IN ('e', 'c')")
        ]
        
        all_empty = True
        for name, query in checks:
            result = session.execute(text(query)).fetchone()[0]
            if result > 0:
                print(f"⚠️  {name}: {result} remaining")
                all_empty = False
            else:
                print(f"✅ {name}: 0 (empty)")
        
        session.close()
        
        if all_empty:
            print("\n🎉 Schema successfully emptied - ready for fresh setup!")
        else:
            print("\n⚠️  Some objects may remain - manual cleanup might be needed")
        
        return all_empty
        
    except Exception as e:
        print(f"❌ Error verifying schema: {e}")
        return False

def main():
    """
    Command-line interface for dropping database objects
    """
    parser = argparse.ArgumentParser(
        description='Drop all database objects in public schema (DANGEROUS!)',
        epilog="""
WARNING: This completely destroys your database!
Only use this when you want to start completely fresh.

Examples:
  python drop_database_objects.py --confirm     # Drop everything
  python drop_database_objects.py --verify     # Just verify current state
        """
    )
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', default='5432', help='Database port')
    parser.add_argument('--user', default='asante_dev', help='Database user')
    parser.add_argument('--password', default='password', help='Database password')
    parser.add_argument('--database', default='postgres', help='Database name')
    parser.add_argument('--confirm', action='store_true', 
                       help='Required flag to actually drop objects (safety mechanism)')
    parser.add_argument('--verify', action='store_true', 
                       help='Only verify current schema state without dropping anything')
    
    args = parser.parse_args()
    
    database_url = f"postgresql://{args.user}:{args.password}@{args.host}:{args.port}/{args.database}"
    
    if args.verify:
        verify_empty_schema(database_url)
    else:
        success = drop_all_database_objects(database_url, confirm=args.confirm)
        if success:
            verify_empty_schema(database_url)

if __name__ == "__main__":
    main()