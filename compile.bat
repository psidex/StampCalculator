@echo off
git clone https://github.com/thatguywiththatname/Stamp_Calculator
cd Stamp_Calculator
mkdir stamp_calc_app\bin
copy ..\bin stamp_calc_app
cd stamp_calc_app
pyinstaller --onefile --windowed --path bin --icon=icon.ico app.pyw
cd dist
ren app.exe "Postage Stamp Calculation.exe"
copy calc.exe ..\..\..
echo.
echo.
echo.
echo.
echo == DONE ==
echo.
echo.
echo.
echo.
pause
