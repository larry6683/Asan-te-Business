#!/bin/bash
PROTO_DIR="../new-grpc-api/src/protos"
OUT_DIR="./src/proto"
mkdir -p $OUT_DIR

echo "🔧 Generating JavaScript code from proto files..."

protoc -I=$PROTO_DIR \
  --js_out=import_style=commonjs:$OUT_DIR \
  --grpc-web_out=import_style=commonjs,mode=grpcwebtext:$OUT_DIR \
  $PROTO_DIR/error/error.proto \
  $PROTO_DIR/user/user.proto \
  $PROTO_DIR/business/business.proto \
  $PROTO_DIR/beneficiary/beneficiary.proto

echo "✅ Generated files:"
ls -la $OUT_DIR
echo "✅ Proto generation complete!"
EOF