# loguploader



```
git pull https://github.com/snizzleorg/loguploader.git
cd logupdater
pip install -r requirements.txt
```
then create a file `public_link` with the public link for the nextcloud dropbox folder:
```
public_link=https://<nexcloud-address>
```


To create an executable which can be run without installing Python first you need https://pyinstaller.readthedocs.io/en/stable/index.html which can be installed like so:

```
pip install pyinstaller
```

pyinstaller will probably not be found by Windows therefore run it using: 

```
python -m pyinstaller --onefile logupdater.py
```
 
 This should create `dist\logupdater.exe` which can be deployed directly without the need to install anything.
