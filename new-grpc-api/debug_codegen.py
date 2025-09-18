import subprocess
import sys
import os

# Check protobuf version
try:
    import google.protobuf
    print(f"Protobuf version: {google.protobuf.__version__}")
except ImportError:
    print("Protobuf not installed")

# Check grpcio version  
try:
    import grpc
    print(f"gRPC version: {grpc.__version__}")
except ImportError:
    print("gRPC not installed")

# Check Python version
print(f"Python version: {sys.version}")

# Check if codegen files exist
codegen_path = "src/codegen"
if os.path.exists(codegen_path):
    for root, dirs, files in os.walk(codegen_path):
        for file in files:
            if file.endswith('.py'):
                print(f"Found: {os.path.join(root, file)}")
else:
    print("Codegen directory doesn't exist")
