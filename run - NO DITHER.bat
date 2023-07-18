@echo OFF
setlocal EnableExtensions EnableDelayedExpansion
if exist "C:\Program Files (x86)\" (
  for /f "tokens=4" %%a in ('dir "C:\Program Files (x86)" /ad ^| findstr /i "Dosbox*"') do (
  set Dosver=%%a
)
) else (
  for /f "tokens=4" %%a in ('dir "C:\Program Files" /ad ^| findstr /i "Dosbox*"') do (
  set Dosver=%%a
)
)
if not defined Dosver goto DOSBOX_NOT_FOUND
python -V >NUL
if ERRORLEVEL 1 goto PYTHON_DOES_NOT_EXIST
set PATH=%PATH%;C:\Program Files (x86)\%Dosver%
python imgflat-no-dither.py
Dosbox.exe imgview.com
:DOSBOX_NOT_FOUND
echo Please install Dosbox to run
exit
:PYTHON_DOES_NOT_EXIST
echo Please Install Python to continue
exit