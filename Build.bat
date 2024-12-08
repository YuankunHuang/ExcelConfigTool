@echo off

set excel_path="Excel"
set proto_output_path="Output\proto"
set dat_output_path="Output\dat"
set python_output_path="Output\proto_py"
set csharp_output_path="Output\proto_cs"

echo:
echo Start building...
echo:

poetry run python Tools\main.py %excel_path% %proto_output_path% %dat_output_path% %python_output_path% %csharp_output_path%

echo:
echo Building ends.
echo:

pause