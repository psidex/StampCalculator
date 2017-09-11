@echo off
git clone https://github.com/thatguywiththatname/Stamp_Calculator
cd Stamp_Calculator
copy icon.ico config_setup_app
copy icon.ico stamp_calc_app
mkdir config_setup_app\bin
mkdir stamp_calc_app\bin
copy ..\bin config_setup_app
copy ..\bin stamp_calc_app
cd config_setup_app
pyinstaller --onefile --windowed --path bin --icon=icon.ico app.pyw
cd dist
ren app.exe config.exe
COPY config.exe ..\..\..
cd ..\..
cd stamp_calc_app
pyinstaller --onefile --windowed --path bin --icon=icon.ico app.pyw
cd dist
ren app.exe calc.exe
COPY calc.exe ..\..\..
cd ..\..
COPY stamps.json ..
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
