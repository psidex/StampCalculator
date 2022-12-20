:: Creates .exe
@echo off
call compileGUI.bat
cd src
:: Copy _rc.py files to the same location as the main Python file
copy gui\*_rc.py .
pyinstaller --onefile --windowed --icon=gui/stamp.ico app.pyw
:: Clean up
rd /s /q build
del *.spec
del /Q *_rc.py
rename dist\app.exe StampCalc.exe
cd ..
echo Done
