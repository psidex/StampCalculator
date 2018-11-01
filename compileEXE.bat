:: Creates .exe
@echo off
cd StampCalculator
pyinstaller --onefile --windowed --icon=gui/stamp.ico app.pyw
echo Done
