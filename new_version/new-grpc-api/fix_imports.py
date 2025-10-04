import os
import re

def fix_imports(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('_pb2.py') or file.endswith('_pb2_grpc.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Fix imports
                content = re.sub(
                    r'from error import error_pb2',
                    'from codegen.error import error_pb2',
                    content
                )
                content = re.sub(
                    r'from user import user_pb2',
                    'from codegen.user import user_pb2',
                    content
                )
                content = re.sub(
                    r'from business import business_pb2',
                    'from codegen.business import business_pb2',
                    content
                )
                content = re.sub(
                    r'from beneficiary import beneficiary_pb2',
                    'from codegen.beneficiary import beneficiary_pb2',
                    content
                )
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f'Fixed imports in: {filepath}')

if __name__ == '__main__':
    fix_imports('src/codegen')
    print('All imports fixed!')
