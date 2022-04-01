# loguploader

## Building

`pip install -r requirements.txt`

`pip install pyinstaller`

pyinstaller will probably not be found by windows therefore run it using

`python -m pyinstaller --onefile logupdater.py`
 
 This should create `dist\logupdater.exe` which can be deployed directly without the need to install anything.
