import os
import re
import argparse
import importlib.util
from pathlib import Path
from collections import defaultdict

def find_sqlalchemy_models(tables_dir):
    """
    Find all SQLAlchemy model files in the tables directory.
    
    Args:
        tables_dir (str): Path to the tables directory
        
    Returns:
        dict: Dictionary mapping model names to file paths
    """
    models = {}
    
    if not os.path.isdir(tables_dir):
        return models
    
    for file in os.listdir(tables_dir):
        if file.endswith('.py') and file != '__init__.py':
            model_name = file[:-3]  # Remove .py extension
            models[model_name] = os.path.join(tables_dir, file)
    
    return models

def check_model_imports(tables_dir):
    """
    Check if __init__.py properly imports all models.
    
    Args:
        tables_dir (str): Path to the tables directory
        
    Returns:
        dict: Dictionary with import validation results
    """
    results = {
        'init_file_exists': False,
        'missing_imports': [],
        'extra_imports': [],
        'import_errors': []
    }
    
    init_file = os.path.join(tables_dir, '__init__.py')
    
    if not os.path.exists(init_file):
        results['init_file_exists'] = False
        return results
    
    results['init_file_exists'] = True
    
    # Find all model files
    models = find_sqlalchemy_models(tables_dir)
    
    # Read __init__.py to find imports
    try:
        with open(init_file, 'r') as f:
            init_content = f.read()
        
        # Look for imports from model files
        imported_models = set()
        
        # Pattern for: from .model_name import ModelName
        from_import_pattern = r'from\s+\.(\w+)\s+import\s+(\w+)'
        from_matches = re.findall(from_import_pattern, init_content)
        for file_name, class_name in from_matches:
            imported_models.add(file_name)
        
        # Pattern for: from .model_name import *
        star_import_pattern = r'from\s+\.(\w+)\s+import\s+\*'
        star_matches = re.findall(star_import_pattern, init_content)
        for file_name in star_matches:
            imported_models.add(file_name)
        
        # Check for missing imports
        for model_name in models.keys():
            if model_name not in imported_models:
                results['missing_imports'].append(model_name)
        
        # Check for extra imports (imports that don't have corresponding files)
        for imported_model in imported_models:
            if imported_model not in models:
                results['extra_imports'].append(imported_model)
                
    except Exception as e:
        results['import_errors'].append(f"Error reading __init__.py: {e}")
    
    return results

def check_populate_functions(populate_script):
    """
    Check if populate_data.py has all necessary populate functions.
    
    Args:
        populate_script (str): Path to populate_data.py
        
    Returns:
        dict: Dictionary with populate function validation results
    """
    results = {
        'script_exists': False,
        'populate_functions': [],
        'missing_functions': [],
        'main_function_exists': False,
        'errors': []
    }
    
    if not os.path.exists(populate_script):
        results['script_exists'] = False
        return results
    
    results['script_exists'] = True
    
    try:
        with open(populate_script, 'r') as f:
            content = f.read()
        
        # Look for populate functions
        populate_pattern = r'def\s+(populate_\w+)\s*\('
        populate_matches = re.findall(populate_pattern, content)
        results['populate_functions'] = populate_matches
        
        # Check for main setup function
        if 'def populate_all_reference_data(' in content:
            results['main_function_exists'] = True
        
        # Expected populate functions based on common reference tables
        expected_functions = [
            'populate_user_types',
            'populate_business_sizes',
            'populate_business_user_permission_roles',
            'populate_cause_categories_and_causes',
            'populate_cause_preference_ranks',
            'populate_social_media_types',
            'populate_shop_types'
        ]
        
        for expected in expected_functions:
            if expected not in populate_matches:
                results['missing_functions'].append(expected)
                
    except Exception as e:
        results['errors'].append(f"Error reading populate script: {e}")
    
    return results

def check_hash_events(tables_dir):
    """
    Check if tables that need hash generation have SQLAlchemy events.
    
    Args:
        tables_dir (str): Path to the tables directory
        
    Returns:
        dict: Dictionary with hash event validation results
    """
    results = {
        'tables_needing_hash': ['app_user', 'business', 'beneficiary'],
        'tables_with_events': [],
        'missing_events': [],
        'errors': []
    }
    
    # Tables that should have hash generation based on original SQL triggers
    hash_tables = {
        'app_user': ['email_hash'],
        'business': ['email_hash', 'business_name_hash'],
        'beneficiary': ['email_hash', 'beneficiary_name_hash']
    }
    
    for table_name, expected_hashes in hash_tables.items():
        model_file = os.path.join(tables_dir, f'{table_name}.py')
        
        if not os.path.exists(model_file):
            results['missing_events'].append(f"{table_name}.py file not found")
            continue
        
        try:
            with open(model_file, 'r') as f:
                content = f.read()
            
            # Look for SQLAlchemy event decorators
            has_events = False
            
            # Check for @event.listens_for patterns
            event_pattern = r'@event\.listens_for\s*\(\s*\w+\s*,\s*[\'"]before_(insert|update)[\'"]\s*\)'
            if re.search(event_pattern, content):
                has_events = True
                results['tables_with_events'].append(table_name)
            
            if not has_events:
                results['missing_events'].append(f"{table_name} - missing hash generation events")
                
        except Exception as e:
            results['errors'].append(f"Error reading {table_name}.py: {e}")
    
    return results

def check_seed_data_scripts(scripts_dir):
    """
    Check if seed data scripts exist and are properly organized.
    
    Args:
        scripts_dir (str): Path to the scripts directory
        
    Returns:
        dict: Dictionary with seed data validation results
    """
    results = {
        'seed_data_dir_exists': False,
        'expected_scripts': ['public_seed_data.py', 'clear_db_data.py', 'delete_seed_data.py'],
        'existing_scripts': [],
        'missing_scripts': [],
        'script_errors': []
    }
    
    seed_data_dir = os.path.join(scripts_dir, 'seed_data')
    
    if not os.path.isdir(seed_data_dir):
        results['seed_data_dir_exists'] = False
        return results
    
    results['seed_data_dir_exists'] = True
    
    for script in results['expected_scripts']:
        script_path = os.path.join(seed_data_dir, script)
        if os.path.exists(script_path):
            results['existing_scripts'].append(script)
        else:
            results['missing_scripts'].append(script)
    
    return results

def validate_sqlalchemy_migration(project_root):
    """
    Validate that the SQLAlchemy migration is complete and properly organized.
    
    Args:
        project_root (str): Path to the project root directory
        
    Returns:
        dict: Dictionary with validation results
    """
    tables_dir = os.path.join(project_root, 'src', 'public', 'tables')
    migrations_dir = os.path.join(project_root, 'migrations', 'initial_schema')
    scripts_dir = os.path.join(project_root, 'scripts')
    populate_script = os.path.join(migrations_dir, 'populate_data.py')
    
    results = {
        'models': check_model_imports(tables_dir),
        'populate_functions': check_populate_functions(populate_script),
        'hash_events': check_hash_events(tables_dir),
        'seed_scripts': check_seed_data_scripts(scripts_dir),
        'directory_structure': {}
    }
    
    # Check basic directory structure
    results['directory_structure'] = {
        'tables_dir_exists': os.path.isdir(tables_dir),
        'migrations_dir_exists': os.path.isdir(migrations_dir),
        'scripts_dir_exists': os.path.isdir(scripts_dir),
        'populate_script_exists': os.path.exists(populate_script)
    }
    
    return results

def print_validation_results(results):
    """
    Print the validation results in a formatted way.
    
    Args:
        results (dict): Validation results dictionary
    """
    print("\n=== SQLAlchemy Migration Validation Results ===\n")
    
    # Directory structure
    print("Directory Structure:")
    structure = results['directory_structure']
    for check, status in structure.items():
        status_text = "✓" if status else "✗"
        print(f"  {status_text} {check.replace('_', ' ').title()}")
    print()
    
    # Model imports
    print("Model Imports (__init__.py):")
    models = results['models']
    if models['init_file_exists']:
        if not models['missing_imports'] and not models['extra_imports']:
            print("  ✓ All models properly imported")
        else:
            if models['missing_imports']:
                print(f"  ✗ Missing imports: {', '.join(models['missing_imports'])}")
            if models['extra_imports']:
                print(f"  ✗ Extra imports: {', '.join(models['extra_imports'])}")
    else:
        print("  ✗ __init__.py file missing")
    
    if models['import_errors']:
        for error in models['import_errors']:
            print(f"  ✗ {error}")
    print()
    
    # Populate functions
    print("Populate Functions:")
    populate = results['populate_functions']
    if populate['script_exists']:
        if populate['main_function_exists']:
            print("  ✓ Main populate function exists")
        else:
            print("  ✗ Main populate function missing")
        
        if not populate['missing_functions']:
            print("  ✓ All expected populate functions found")
        else:
            print(f"  ✗ Missing functions: {', '.join(populate['missing_functions'])}")
        
        print(f"  Found {len(populate['populate_functions'])} populate functions")
    else:
        print("  ✗ populate_data.py not found")
    
    if populate['errors']:
        for error in populate['errors']:
            print(f"  ✗ {error}")
    print()
    
    # Hash events
    print("Hash Generation Events:")
    hash_events = results['hash_events']
    if not hash_events['missing_events']:
        print("  ✓ All tables have proper hash events")
    else:
        for missing in hash_events['missing_events']:
            print(f"  ✗ {missing}")
    
    if hash_events['tables_with_events']:
        print(f"  ✓ Tables with events: {', '.join(hash_events['tables_with_events'])}")
    
    if hash_events['errors']:
        for error in hash_events['errors']:
            print(f"  ✗ {error}")
    print()
    
    # Seed data scripts
    print("Seed Data Scripts:")
    seed = results['seed_scripts']
    if seed['seed_data_dir_exists']:
        if not seed['missing_scripts']:
            print("  ✓ All seed data scripts found")
        else:
            print(f"  ✗ Missing scripts: {', '.join(seed['missing_scripts'])}")
        
        if seed['existing_scripts']:
            print(f"  ✓ Existing scripts: {', '.join(seed['existing_scripts'])}")
    else:
        print("  ✗ seed_data directory not found")
    print()
    
    # Summary
    print("=== Summary ===")
    issues = []
    
    if not results['directory_structure']['tables_dir_exists']:
        issues.append("Missing tables directory")
    if not results['models']['init_file_exists']:
        issues.append("Missing __init__.py")
    if results['models']['missing_imports']:
        issues.append("Missing model imports")
    if not results['populate_functions']['script_exists']:
        issues.append("Missing populate_data.py")
    if results['populate_functions']['missing_functions']:
        issues.append("Missing populate functions")
    if results['hash_events']['missing_events']:
        issues.append("Missing hash events")
    if results['seed_scripts']['missing_scripts']:
        issues.append("Missing seed scripts")
    
    if not issues:
        print("✓ SQLAlchemy migration appears complete and properly organized!")
    else:
        print("✗ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nPlease review and fix the issues above.")

def main():
    parser = argparse.ArgumentParser(description='Validate SQLAlchemy migration completeness')
    parser.add_argument('--project-root', default='.', 
                        help='Path to the project root directory (default: current directory)')
    
    args = parser.parse_args()
    
    project_root = args.project_root
    
    if not os.path.isdir(project_root):
        print(f"Error: Project root directory '{project_root}' does not exist.")
        return 1
    
    results = validate_sqlalchemy_migration(project_root)
    print_validation_results(results)
    
    # Return exit code based on validation results
    issues_found = (
        not results['directory_structure']['tables_dir_exists'] or
        not results['models']['init_file_exists'] or
        results['models']['missing_imports'] or
        not results['populate_functions']['script_exists'] or
        results['populate_functions']['missing_functions'] or
        results['hash_events']['missing_events'] or
        results['seed_scripts']['missing_scripts']
    )
    
    return 1 if issues_found else 0

if __name__ == "__main__":
    print("SQLAlchemy Migration Validation Script")
    print("-------------------------------------")
    print("Checking that SQLAlchemy migration is complete and properly organized")
    print("This validates models, populate functions, hash events, and seed data scripts")
    print("Running from project root directory...")
    exit(main())