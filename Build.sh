#!/bin/bash

excel_path="Excel"
proto_output_path="Output/proto"
dat_output_path="Output/dat"
python_output_path="Output/proto_py"
csharp_output_path="Output/proto_cs"

echo ""
echo "Start building..."
echo ""

poetry run python Tools/main.py "$excel_path" "$proto_output_path" "$dat_output_path" "$python_output_path" "$csharp_output_path"

echo ""
echo "Building ends."
echo ""

read -p "Press [Enter] to continue..."
