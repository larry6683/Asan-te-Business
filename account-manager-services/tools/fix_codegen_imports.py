import glob, fileinput, sys, os
from pathlib import Path
from itertools import chain

"""
    There is an issue when generating the grpc files
    when the output directory is a subfolder
    there is an issue with the imports... 
    a "module not found" error will occur from one of the generated files
    this fixes that by forcing relative imports.

    Inpired by protoletariat python package
    which is incompatible with our version of protobuf
    https://github.com/cpcloud/protoletariat

    NOTE
    THIS WILL ONLY FIX FILES DIRECTLY UNDER THE 'codegen' FOLDER
    THIS HAS NOT BEEN CONFIGURED TO WORK WITH ANY ADDITIONAL NESTED FILES/FOLDERS

    NOTE
    I realize there are 'better' ways of matching strings
    and that all these functions could be reduced to very simple replaces
    but I wanted to be extra thorough with tests and such
    also - it makes me feel safe :) - TJ

    NOTE 
    writing to stderror is done for messaging because writing to standard output updates the opened file.

    example fixes
    Fix 1 (generic import):
        Before:
            import campaign_ids_pb2 as campaign__ids__pb2
        After:
            from . import campaign_ids_pb2 as campaign__ids__pb2

    Fix 2 (specific imports): 
        Before:
            from campaign_ids_pb2 import *
        After:
            from .campaign_ids_pb2 import *

    Fix 3 (module imports, only supporting 1 level of submodules for now):
        Before:
            from auth import entity_type_pb2 as auth_dot_entity__type__pb2
        After:
            from ..auth import entity_type_pb2 as auth_dot_entity__type__pb2
"""

def print_fix_message(file_path: str):
    sys.stderr.write(f'fixing file: {file_path}\n')

def fix_py_line(line: str, is_sub_module: bool) -> str:
    if line.startswith('import'):
        line = ''.join(('from . ', line))
    elif line.startswith('from'):
        # check for grpc module imports
        line = line.replace('from ', 'from ..' if is_sub_module else 'from .')
    return line

def fix_pyi_line(line: str, is_sub_module: bool, file_path: str = None) -> str:
    if 'google' in line or line.startswith('import'):
        return line
    
    # this can probably be the else condition but just to be sure...
    if line.startswith('from'):
        if is_sub_module:
            # a progromatic solution requires "searching" for dependencies
            # hardcoding is used in lieu of more complicated logic
            mods = ["auth", "error", "payment_method"]
            if (any(mod not in file_path and f"from {mod}" in line for mod in mods)
                    # this condition can be removed if te_credit_transaction_history lives in te_credit_account
                    or "te_credit_account_status" in line):
                # from auth import x => from ..auth import x
                line = line.replace("from ", "from ..")
            
            else:
                # from x import y => import y
                split = line.split('import')
                line = f'import{split[1]}'
        else:
            line = line.replace('from ', 'from .')
    
    return line

def fix_codegen_file(file_path: Path):
    if 'google' in str(file_path):
        pass

    # uncomment for messaging
    # print_fix_message(file_path)

    is_sub_module = not str(file_path.parent).endswith("codegen") # only supports one level of submodules

    with fileinput.FileInput(files=file_path, inplace=True) as input:
        for line in input:
            if '_pb2' in line:
                if file_path.suffix == '.py':
                    line = fix_py_line(line, is_sub_module)
                else:
                    line = fix_pyi_line(line, is_sub_module, str(file_path))
            print(line, end='')

codegen_dir = 'src/codegen/'

codegen_py_path_glob = Path(codegen_dir).glob(f'**/*.py')
codegen_pyi_path_glob = Path(codegen_dir).glob(f'**/*.pyi')

for path in chain(codegen_py_path_glob, codegen_pyi_path_glob):
    fix_codegen_file(path)
