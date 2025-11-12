#!/bin/bash

set -e

echo "🔧 Generating Python protobuf files..."

PROTO_DIR="src/protos"
OUT_DIR="src/codegen"

mkdir -p $OUT_DIR

# Generate protobuf files
python -m grpc_tools.protoc \
  -I=$PROTO_DIR \
  --python_out=$OUT_DIR \
  --grpc_python_out=$OUT_DIR \
  $PROTO_DIR/error/error.proto \
  $PROTO_DIR/user/user.proto \
  $PROTO_DIR/business/business.proto \
  $PROTO_DIR/beneficiary/beneficiary.proto \
  $PROTO_DIR/analytics/analytics.proto

echo "✅ Protobuf files generated"
echo "🔧 Fixing import paths..."

# Fix ALL imports for macOS
find $OUT_DIR -type f \( -name "*_pb2.py" -o -name "*_pb2_grpc.py" \) | while read file; do
  # Fix error imports
  sed -i '' 's/^from error import error_pb2/from codegen.error import error_pb2/g' "$file"
  sed -i '' 's/^import error_pb2/from codegen.error import error_pb2/g' "$file"
  
  # Fix user imports
  sed -i '' 's/^from user import user_pb2/from codegen.user import user_pb2/g' "$file"
  sed -i '' 's/^import user_pb2/from codegen.user import user_pb2/g' "$file"
  
  # Fix business imports
  sed -i '' 's/^from business import business_pb2/from codegen.business import business_pb2/g' "$file"
  sed -i '' 's/^import business_pb2/from codegen.business import business_pb2/g' "$file"
  
  # Fix beneficiary imports
  sed -i '' 's/^from beneficiary import beneficiary_pb2/from codegen.beneficiary import beneficiary_pb2/g' "$file"
  sed -i '' 's/^import beneficiary_pb2/from codegen.beneficiary import beneficiary_pb2/g' "$file"

  # Fix analytics imports
  sed -i '' 's/^from analytics import analytics_pb2/from codegen.analytics import analytics_pb2/g' "$file"
  sed -i '' 's/^import analytics_pb2/from codegen.analytics import analytics_pb2/g' "$file"
done

# Add __init__.py files
touch $OUT_DIR/__init__.py
touch $OUT_DIR/error/__init__.py
touch $OUT_DIR/user/__init__.py
touch $OUT_DIR/business/__init__.py
touch $OUT_DIR/beneficiary/__init__.py
touch $OUT_DIR/analytics/__init__.py

echo "✅ Import paths fixed"
echo "✅ Complete!"

echo ""
echo "Generated files:"
find $OUT_DIR -type f -name "*.py" | sort