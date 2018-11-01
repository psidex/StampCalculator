:: Compile the QT Designer files into .py Python files
@echo off
cd StampCalculator\gui
echo Compiling resources
pyrcc5 stampCalculator.qrc -o stampCalculator_rc.py
echo Compiling UI file(s)
pyuic5 -x stampCalculator.ui -o stampCalculatorUI.py
cd ..\..
echo Done
