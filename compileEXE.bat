:: Creates .exe
@echo off
call compileGUI.bat
cd StampCalculator
:: Copy _rc.py files to the same location as the main Python file
:: See app.pyw comment for why this happens
copy gui\*_rc.py .
pyinstaller --onefile --windowed --icon=gui/stamp.ico app.pyw
:: Clean up
rd /s /q build
del *.spec 
del /Q *_rc.py
cd ..
echo Done
