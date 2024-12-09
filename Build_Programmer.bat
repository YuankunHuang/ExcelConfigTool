@echo off

set data_input_path="Output\proto"
set config_output_path="Output\config"

echo:
echo Building starts
echo:

call Build.bat

poetry run python Tools\generate_config_cs.py %data_input_path% %config_output_path%

echo:
echo Building ends
echo:

pause