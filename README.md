# Stamp_Calculator

## Build

`pyuic5 -x stamp_calc.ui -o stamp_calc_ui.py`

`pyuic5 -x config_setup.ui -o config_setup_ui.py`

## Compile

Copy /bin from PyQt path (example: `C:\Python35-32\Lib\site-packages\PyQt5\Qt\bin`)
into each dir and then use this command in each dir:

`pyinstaller --onefile --windowed --path bin --icon=icon.ico app.pyw`

## ToDo

 - fix both apps when launched & stamps.json does not exist
 - make sure user can only input legitimate values in inputs
