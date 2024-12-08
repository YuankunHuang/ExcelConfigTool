@echo off

set excel_path="Excel"
set output_path="Output"

echo Running configuration tool...

poetry run python Tools\main.py %excel_path% %output_path%

echo:
echo Configuration tool running ends.
echo:

pause