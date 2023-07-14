#!/bin/bash
echo "Creating proto grpc files..."
python -m grpc_tools.protoc -I=proto/ --python_out=proto/ --grpc_python_out=proto/ proto/chat.proto
sed -i 's/import chat_pb2 as chat__pb2/import proto.chat_pb2 as chat__pb2/g' proto/chat_pb2_grpc.py
mkdir ./logs
echo "DONE"
