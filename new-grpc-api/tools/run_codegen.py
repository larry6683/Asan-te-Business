import subprocess
import sys
import os
from pathlib import Path

def run_codegen():
    proto_path = "./src/protos"
    output_path = "./src/codegen"
    
    print("Running codegen tool...")
    print(f"protopath={proto_path} outputpath={output_path}")
    
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Find all proto files
    proto_files = []
    for proto_file in Path(proto_path).rglob("*.proto"):
        proto_files.append(str(proto_file))
    
    print("\nExecuting protoc for message types...")
    
    # Generate Python message classes
    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"--proto_path={proto_path}",
        f"--python_out={output_path}",
        f"--pyi_out={output_path}"
    ] + proto_files
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error generating message types: {result.stderr}")
        return False
    
    # Generate gRPC service classes
    service_files = []
    for proto_file in Path(proto_path).rglob("*service.proto"):
        service_files.append(str(proto_file))
    
    if service_files:
        print("Executing protoc for service types...")
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"--proto_path={proto_path}",
            f"--grpc_python_out={output_path}"
        ] + service_files
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error generating service types: {result.stderr}")
            return False
    
    print("Protoc completed successfully...")
    
    # Fix imports
    print("\nFixing codegen imports...")
    try:
        exec(open("./tools/fix_codegen_imports.py").read())
        print("Import fixes completed...")
    except Exception as e:
        print(f"Warning: Could not fix imports: {e}")
    
    print("\nCodegen completed successfully!")
    return True

if __name__ == "__main__":
    success = run_codegen()
    if not success:
        sys.exit(1)
