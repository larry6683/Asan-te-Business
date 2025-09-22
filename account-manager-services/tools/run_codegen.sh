#!/bin/bash

proto_path="./src/protos"
output_path="./src/codegen"

echo running codegen tool... 
echo protopath=${proto_path} outputpath=${output_path}

# echo
# echo executing import google types
# python ./tools/import_google_types.py
# echo completed...

echo
echo executing protoc
shopt -s globstar

python -m grpc_tools.protoc \
    --proto_path=${proto_path} \
    --python_out=${output_path} \
    --pyi_out=${output_path} \
    ${proto_path}/**/*.proto

python -m grpc_tools.protoc \
    --proto_path=${proto_path} \
    --grpc_python_out=${output_path} \
    ${proto_path}/**/*service.proto

echo completed...

echo
echo fixing codegen imports
python ./tools/fix_codegen_imports.py
echo completed...

echo
echo codegen completed

sleep 10