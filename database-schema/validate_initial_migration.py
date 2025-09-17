import os
import re
import argparse
from pathlib import Path
from collections import defaultdict

def extract_schema_objects_from_migration(migration_file, is_data_file=False):
    """
    Extract schema object references from a migration file.
    
    Args:
        migration_file (str): Path to the migration file
        is_data_file (bool): Whether the file is a data population file
        
    Returns:
        dict: Dictionary mapping object types to sets of (schema, object_name) tuples
    """
    object_references = defaultdict(set)
    
    # Determine the object type from the filename
    filename = os.path.basename(migration_file)
    
    if is_data_file:
        object_type = 'data'
    elif '03_create_type' in filename:
        object_type = 'types'
    elif '04_create_tables' in filename:
        object_type = 'tables'
    elif '05_create_views' in filename:
        object_type = 'views'
    elif '06_create_functions' in filename:
        object_type = 'functions'
    elif '07_create_procedures' in filename:
        object_type = 'procedures'
    elif '08_create_triggers' in filename:
        object_type = 'triggers'
    elif '09_populate_data' in filename:
        object_type = 'data'
    else:
        return object_references  # Unknown object type
    
    with open(migration_file, 'r') as f:
        content = f.read()
    
    # Look for references like: \i src/{schema_name}/{object_type}/{object_name}.sql
    pattern = r'\\i src/([^/]+)/([^/]+)/([^/]+)\.sql'
    matches = re.findall(pattern, content)
    
    for match in matches:
        schema_name, folder_type, object_name = match
        
        # For data files, we're looking for 'data' folder
        if is_data_file or object_type == 'data':
            if folder_type == 'data':
                object_references['data'].add((schema_name, object_name))
        else:
            # Validate that the folder_type matches expected object_type
            # Convert plural to singular if needed for comparison
            folder_singular = folder_type[:-1] if folder_type.endswith('s') else folder_type
            object_singular = object_type[:-1] if object_type.endswith('s') else object_type
            
            if folder_singular == object_singular:
                object_references[object_type].add((schema_name, object_name))
    
    return object_references

def find_actual_schema_objects(src_dir):
    """
    Find all actual schema objects in the src directory structure.
    
    Args:
        src_dir (str): Path to the src directory
        
    Returns:
        dict: Dictionary mapping object types to sets of (schema, object_name) tuples
    """
    actual_objects = defaultdict(set)
    
    # List of object types to check (based on existing folders mentioned)
    object_types = ['functions', 'procedures', 'tables', 'triggers', 'data']
    
    # List of schemas to check
    schemas = ['public']
    
    for schema in schemas:
        schema_dir = os.path.join(src_dir, schema)
        if not os.path.isdir(schema_dir):
            continue
            
        for object_type in object_types:
            object_dir = os.path.join(schema_dir, object_type)
            if not os.path.isdir(object_dir):
                continue
                
            for file in os.listdir(object_dir):
                if file.endswith('.sql'):
                    object_name = file[:-4]  # Remove .sql extension
                    actual_objects[object_type].add((schema, object_name))
    
    return actual_objects

def find_tables_missing_triggers(src_dir):
    """
    Find all tables that are missing update trigger or trigger function.
    
    Args:
        src_dir (str): Path to the src directory
        
    Returns:
        dict: Dictionary with missing trigger information
    """
    missing_triggers = {
        'missing_trigger_functions': [],
        'missing_triggers': []
    }
    
    # List of schemas to check
    schemas = ['public']
    
    # Find all tables first
    tables = {}
    for schema in schemas:
        schema_dir = os.path.join(src_dir, schema)
        if not os.path.isdir(schema_dir):
            continue
            
        tables_dir = os.path.join(schema_dir, 'tables')
        if not os.path.isdir(tables_dir):
            continue
            
        for file in os.listdir(tables_dir):
            if file.endswith('.sql'):
                table_name = file[:-4]  # Remove .sql extension
                tables[(schema, table_name)] = True
    
    # Check for corresponding trigger functions and triggers
    for (schema, table_name) in tables:
        # Check for update trigger function
        trigger_function_name = f"{table_name}_before_update_triggerfn"
        trigger_function_path = os.path.join(src_dir, schema, "functions", f"{trigger_function_name}.sql")
        
        if not os.path.exists(trigger_function_path):
            missing_triggers['missing_trigger_functions'].append((schema, table_name, trigger_function_name))
        
        # Check for update trigger
        trigger_name = f"{table_name}_before_update_trigger"
        trigger_path = os.path.join(src_dir, schema, "triggers", f"{trigger_name}.sql")
        
        if not os.path.exists(trigger_path):
            missing_triggers['missing_triggers'].append((schema, table_name, trigger_name))
    
    return missing_triggers

def validate_schema_objects(src_dir, migration_dir):
    """
    Validate that all schema objects have corresponding entries in migration files.
    
    Args:
        src_dir (str): Path to the src directory
        migration_dir (str): Path to the migration directory
        
    Returns:
        dict: Dictionary with validation results
    """
    # Find all migration files in the 00_initial_schema subdirectory
    initial_schema_dir = os.path.join(migration_dir, '00_initial_schema')
    if not os.path.isdir(initial_schema_dir):
        print(f"Warning: Initial schema directory '{initial_schema_dir}' not found.")
        initial_schema_dir = migration_dir  # Fall back to migration_dir if subdirectory doesn't exist
    
    # Standard object migration files
    migration_files = [
        os.path.join(initial_schema_dir, f) for f in os.listdir(initial_schema_dir)
        if f.startswith(('03_', '04_', '05_', '06_', '07_', '08_')) and f.endswith('.sql')
    ]
    
    # Data population migration file
    data_migration_file = os.path.join(initial_schema_dir, '09_populate_data.sql')
    
    # Extract references from standard migration files
    migration_references = defaultdict(set)
    for file in migration_files:
        refs = extract_schema_objects_from_migration(file)
        for obj_type, obj_set in refs.items():
            migration_references[obj_type].update(obj_set)
    
    # Extract references from data population file if it exists
    if os.path.exists(data_migration_file):
        data_refs = extract_schema_objects_from_migration(data_migration_file, is_data_file=True)
        for obj_type, obj_set in data_refs.items():
            migration_references[obj_type].update(obj_set)
    else:
        print(f"Warning: Data population file '{data_migration_file}' not found.")
    
    # Find actual schema objects
    actual_objects = find_actual_schema_objects(src_dir)
    
    # Find tables missing triggers
    missing_triggers = find_tables_missing_triggers(src_dir)
    
    # Validate that all actual objects have migration references
    results = {
        'missing_in_migration': defaultdict(list),
        'extra_in_migration': defaultdict(list),
        'matched': defaultdict(list),
        'missing_trigger_functions': missing_triggers['missing_trigger_functions'],
        'missing_triggers': missing_triggers['missing_triggers']
    }
    
    for obj_type, obj_set in actual_objects.items():
        for schema, obj_name in obj_set:
            if (schema, obj_name) in migration_references[obj_type]:
                results['matched'][obj_type].append((schema, obj_name))
            else:
                results['missing_in_migration'][obj_type].append((schema, obj_name))
    
    # Check for extra references in migration files
    for obj_type, obj_set in migration_references.items():
        for schema, obj_name in obj_set:
            if obj_type in actual_objects and (schema, obj_name) not in actual_objects[obj_type]:
                results['extra_in_migration'][obj_type].append((schema, obj_name))
    
    return results

def print_validation_results(results):
    """
    Print the validation results in a formatted way.
    
    Args:
        results (dict): Validation results dictionary
    """
    print("\n=== Schema Objects Validation Results ===\n")
    
    # Print matched objects
    # print("Matched Objects (found in both directories and migration files):")
    matched_count = 0
    for obj_type, objects in results['matched'].items():
        if objects:
            # print(f"  {obj_type.capitalize()}:")
            # for schema, obj_name in sorted(objects):
            #     print(f"    - {schema}.{obj_name}")
            matched_count += len(objects)

    print(f"  Total matched: {matched_count}\n")
    
    # Print missing objects
    print("Missing Objects (found in directories but missing in migration files):")
    missing_count = 0
    for obj_type, objects in results['missing_in_migration'].items():
        if objects:
            print(f"  {obj_type.capitalize()}:")
            for schema, obj_name in sorted(objects):
                print(f"    - {schema}.{obj_name}")
            missing_count += len(objects)
    
    if missing_count == 0:
        print("  No missing objects found.")
    else:
        print(f"  Total missing: {missing_count}")
    print()
    
    # Print extra objects
    print("Extra Objects (found in migration files but missing in directories):")
    extra_count = 0
    for obj_type, objects in results['extra_in_migration'].items():
        if objects:
            print(f"  {obj_type.capitalize()}:")
            for schema, obj_name in sorted(objects):
                print(f"    - {schema}.{obj_name}")
            extra_count += len(objects)
    
    if extra_count == 0:
        print("  No extra objects found.")
    else:
        print(f"  Total extra: {extra_count}")
    
    # Print tables missing trigger functions
    print("\nTables Missing Update Trigger Functions:")
    missing_trigger_fn_count = len(results['missing_trigger_functions'])
    if missing_trigger_fn_count == 0:
        print("  No tables missing update trigger functions.")
    else:
        for schema, table_name, trigger_fn_name in sorted(results['missing_trigger_functions']):
            print(f"  - {schema}.{table_name} (missing {trigger_fn_name}.sql)")
        print(f"  Total missing trigger functions: {missing_trigger_fn_count}")
    
    # Print tables missing triggers
    print("\nTables Missing Update Triggers:")
    missing_trigger_count = len(results['missing_triggers'])
    if missing_trigger_count == 0:
        print("  No tables missing update triggers.")
    else:
        for schema, table_name, trigger_name in sorted(results['missing_triggers']):
            print(f"  - {schema}.{table_name} (missing {trigger_name}.sql)")
        print(f"  Total missing triggers: {missing_trigger_count}")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total matched objects: {matched_count}")
    print(f"Total missing objects: {missing_count}")
    print(f"Total extra objects: {extra_count}")
    print(f"Total tables missing update trigger functions: {missing_trigger_fn_count}")
    print(f"Total tables missing update triggers: {missing_trigger_count}")
    
    if missing_count == 0 and extra_count == 0 and missing_trigger_fn_count == 0 and missing_trigger_count == 0:
        print("\nAll schema objects are properly referenced in migration files and all tables have required triggers!")
    else:
        print("\nDiscrepancies found. Please review the results.")

def main():
    parser = argparse.ArgumentParser(description='Validate schema objects against migration files')
    parser.add_argument('--src-dir', default='src', 
                        help='Path to the src directory (default: src)')
    parser.add_argument('--migration-dir', default='migrations', 
                        help='Path to the migration directory (default: migrations)')
    
    args = parser.parse_args()
    
    src_dir = args.src_dir
    migration_dir = args.migration_dir
    
    if not os.path.isdir(src_dir):
        print(f"Error: Source directory '{src_dir}' does not exist.")
        return 1
    
    if not os.path.isdir(migration_dir):
        print(f"Error: Migration directory '{migration_dir}' does not exist.")
        return 1
    
    results = validate_schema_objects(src_dir, migration_dir)
    print_validation_results(results)
    
    # Return exit code based on validation results
    if (results['missing_in_migration'] or results['extra_in_migration'] or 
        results['missing_trigger_functions'] or results['missing_triggers']):
        return 1
    return 0

if __name__ == "__main__":
    print("Schema Objects Validation Script")
    print("--------------------------------")
    print("Checking for schema objects in src/ against migration files in migrations/00_initial_schema/")
    print("This includes data population scripts in src/{schema}/data/ against references in migrations/00_initial_schema/09_populate_data.sql")
    print("Running from project root directory...")
    exit(main())