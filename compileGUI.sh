#!/bin/bash
# A bash version so pyqt5-tools can be used from WSL that has a lower Python version

# :: Compile the QT Designer files into .py Python files
cd ./src/gui
echo "Compiling resources"
pyrcc5 stampCalculator.qrc -o stampCalculator_rc.py
# :: Copy any _rc.py files next to app.pyw so it can "see" them
cp *_rc.py ..
echo "Compiling UI file(s)"
pyuic5 -x stampCalculator.ui -o stampCalculatorUI.py
pyuic5 -x parcelPriceEditor.ui -o parcelPriceEditor.py
cd ../..
echo "Done"
