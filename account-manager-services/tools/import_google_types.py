import glob;
import shutil

proto_dir = './src/protos'
google_types_to_import = (
    "decimal.proto",
)

# python package "googleapis-common-protos"
# must be installed within a venv (or something similar)
# execute from root directory
google_type_protos_glob = glob.iglob(
    pathname='./**/site-packages/google/type/*.proto', 
    recursive=True, 
    include_hidden=True
)

for proto in google_type_protos_glob:
    if proto.endswith(google_types_to_import):
        shutil.copy(proto, f'{proto_dir}/google/type/')