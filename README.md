# Python Scripts

This repository contains a set of python scripts:

- **homebank_import:** A script that I am using to transform a Volksbank `.csv`
  file into a [HomeBank](http://homebank.free.fr/en/index.php) `.csv` file.

## Windows

You can use [pyinstaller](http://www.pyinstaller.org/) to create an executable
from any of these python scripts:

``` shell
pip install pyinstaller
```

Example:

``` shell
cd homebank_import
pyinstaller.exe --onefile homebank_import.py
cd dist
homebank_import.exe
```
