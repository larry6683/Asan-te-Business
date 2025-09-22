import glob, fileinput, sys, os
from pathlib import Path
from itertools import chain

"""
Fix imports in generated protobuf files for proper module resolution.
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
    
    if line.startswith('from'):
        if is_sub_module:
            # Handle submodule imports
            mods = ["auth", "error", "user"]
            if any(mod not in file_path and f"from {mod}" in line for mod in mods):
                line = line.replace("from ", "from ..")
            else:
                split = line.split('import')
                line = f'import{split[1]}'
        else:
            line = line.replace('from ', 'from .')
    
    return line

def fix_codegen_file(file_path: Path):
    if 'google' in str(file_path):
        return

    # print_fix_message(file_path)

    is_sub_module = not str(file_path.parent).endswith("codegen")

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
