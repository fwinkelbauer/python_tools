# Python Scripts

This repository contains a set of python scripts:

- **homebank_import:** A script that I am using to transform a Volksbank `.csv`
  file into a [HomeBank](http://homebank.free.fr/en/index.php) `.csv` file.

## PyInstaller

You can use [pyinstaller](http://www.pyinstaller.org/) to create an executable
from any of these python scripts:

### Windows

``` cmd
choco install python
pip install pyinstaller
```

Example:

``` cmd
cd homebank_import
pyinstaller.exe --onefile homebank_import.py
cd dist
homebank_import.exe
```

### Ubuntu

``` shell
sudo apt install python3-pip
pip3 install pyinstaller
```

Example:

``` shell
cd homebank_import
# Find the full path of pyinstaller using 'find / -name "pyinstaller"'
pyinstaller --onefile homebank_import.py
cd dist
./homebank_import.exe
```
