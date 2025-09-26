#!/bin/bash

# Script to generate gRPC code and run CreateBusiness service
# Usage: ./tools/run/create_business.sh [generate|run|both]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SRC_DIR="$PROJECT_ROOT/src"

echo -e "${BLUE}CreateBusiness Service Management Script${NC}"
echo -e "${BLUE}======================================${NC}"

# Function to fix import paths in generated files
fix_import_paths() {
    echo -e "${YELLOW}Fixing import paths in generated files...${NC}"
    
    cd "$SRC_DIR/codegen"
    
    # Fix ALL business related files
    for file in business/*.py; do
        if [ -f "$file" ]; then
            echo "Fixing imports in: $file"
            
            # Fix business imports
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' 's/from business import/from codegen.business import/g' "$file"
                sed -i '' 's/from error import/from codegen.error import/g' "$file"
            else
                # Linux/Windows with sed
                sed -i 's/from business import/from codegen.business import/g' "$file"
                sed -i 's/from error import/from codegen.error import/g' "$file"
            fi
        fi
    done
    
    echo -e "${GREEN}✓ Fixed all import paths${NC}"
}

# Function to generate gRPC code
generate_grpc_code() {
    echo -e "${YELLOW}Generating gRPC code from proto files...${NC}"
    
    cd "$SRC_DIR"
    
    # Create codegen directory if it doesn't exist
    mkdir -p codegen/business
    
    # Generate CreateBusiness proto
    echo "Generating create_business.proto..."
    python -m grpc_tools.protoc \
        --python_out=codegen \
        --grpc_python_out=codegen \
        --proto_path=protos \
        business/create_business.proto
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ create_business.proto generated successfully${NC}"
    else
        echo -e "${RED}✗ Failed to generate create_business.proto${NC}"
        exit 1
    fi
    
    # Generate CreateBusiness service proto
    echo "Generating create_business_service.proto..."
    python -m grpc_tools.protoc \
        --python_out=codegen \
        --grpc_python_out=codegen \
        --proto_path=protos \
        business/create_business_service.proto
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ create_business_service.proto generated successfully${NC}"
    else
        echo -e "${RED}✗ Failed to generate create_business_service.proto${NC}"
        exit 1
    fi
    
    # Generate GetBusiness proto
    echo "Generating get_business.proto..."
    python -m grpc_tools.protoc \
        --python_out=codegen \
        --grpc_python_out=codegen \
        --proto_path=protos \
        business/get_business.proto
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ get_business.proto generated successfully${NC}"
    else
        echo -e "${RED}✗ Failed to generate get_business.proto${NC}"
        exit 1
    fi
    
    # Generate GetBusiness service proto
    echo "Generating get_business_service.proto..."
    python -m grpc_tools.protoc \
        --python_out=codegen \
        --grpc_python_out=codegen \
        --proto_path=protos \
        business/get_business_service.proto
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ get_business_service.proto generated successfully${NC}"
    else
        echo -e "${RED}✗ Failed to generate get_business_service.proto${NC}"
        exit 1
    fi
    
    # Fix import paths
    fix_import_paths
    
    echo -e "${GREEN}All gRPC code generated successfully!${NC}"
}

# Function to run the CreateBusiness service
run_service() {
    echo -e "${YELLOW}Starting CreateBusiness service on port 63000...${NC}"
    
    cd "$SRC_DIR"
    
    # Check if the required files exist
    if [ ! -f "features/business/create_business/server.py" ]; then
        echo -e "${RED}✗ CreateBusiness service files not found!${NC}"
        echo "Please ensure all CreateBusiness files are created first."
        exit 1
    fi
    
    # Set PYTHONPATH
    export PYTHONPATH="$SRC_DIR"
    
    echo -e "${BLUE}Starting server... (Press Ctrl+C to stop)${NC}"
    python -m features.business.create_business.server
}

# Function to check dependencies
check_dependencies() {
    echo -e "${YELLOW}Checking dependencies...${NC}"
    
    # Check if grpc_tools is available
    python -c "import grpc_tools.protoc" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ grpc_tools not found!${NC}"
        echo "Please install grpc_tools: pip install grpcio-tools"
        exit 1
    fi
    
    echo -e "${GREEN}✓ All dependencies found${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [generate|run|both]"
    echo ""
    echo "Commands:"
    echo "  generate  - Generate gRPC code from proto files"
    echo "  run      - Run the CreateBusiness service"
    echo "  both     - Generate gRPC code and run the service"
    echo ""
    echo "If no command is provided, 'both' will be executed."
}

# Main script logic
case "${1:-both}" in
    "generate")
        check_dependencies
        generate_grpc_code
        echo -e "${GREEN}Done! You can now run the service with: $0 run${NC}"
        ;;
    "run")
        run_service
        ;;
    "both")
        check_dependencies
        generate_grpc_code
        echo -e "${BLUE}Now starting the service...${NC}"
        sleep 2
        run_service
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        echo -e "${RED}Invalid command: $1${NC}"
        show_usage
        exit 1
        ;;
esac
