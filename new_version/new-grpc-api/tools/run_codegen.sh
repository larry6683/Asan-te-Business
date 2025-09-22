#!/bin/bash

proto_path="./src/protos"
output_path="./src/codegen"

echo "Running codegen tool..." 
echo "protopath=${proto_path} outputpath=${output_path}"

echo
echo "Executing protoc"
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

echo "Completed..."

echo
echo "Fixing codegen imports"
python ./tools/fix_codegen_imports.py
echo "Completed..."

echo
echo "Codegen completed"

sleep 10
