import os
import re

def fix_imports(directory):
    """
    Fix imports in gRPC generated files and test scripts.
    Adjusts all import paths to use the codegen.* namespace consistently.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Only patch relevant Python files
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content  # keep for comparison

                # --- Fix gRPC generated file imports ---
                content = re.sub(
                    r'from codegen.error import error_pb2',
                    'from codegen.error import error_pb2',
                    content
                )
                content = re.sub(
                    r'from codegen.user import user_pb2',
                    'from codegen.user import user_pb2',
                    content
                )
                content = re.sub(
                    r'from codegen.business import business_pb2',
                    'from codegen.business import business_pb2',
                    content
                )
                content = re.sub(
                    r'from codegen.beneficiary import beneficiary_pb2',
                    'from codegen.beneficiary import beneficiary_pb2',
                    content
                )

                # --- Fix for test files (like test_cause_mapping.py) ---
                # Ensure imports always reference codegen.*
                content = re.sub(
                    r'from (\w+)\s+import (\w+_pb2(?:_grpc)?)',
                    r'from codegen.\\1 import \\2',
                    content
                )

                # Fix possible relative path imports (e.g. src.public.tables)
                content = re.sub(
                    r'from\s+database_schema_sqlalchemy\.src\.public\.tables',
                    'from src.public.tables',
                    content
                )

                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'✅ Fixed imports in: {filepath}')

    print('\n🎉 All imports fixed successfully!')


if __name__ == '__main__':
    # Adjust these directories as needed for your repo layout
    fix_imports('src/codegen')
    fix_imports('.')  # also fix test files in current directory (like new-grpc-api)
