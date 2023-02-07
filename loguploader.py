import nextcloud_client
import glob
import os
import zipfile
from os.path import basename
from argparse import ArgumentParser
import settings
import winpath
import sys
import subprocess


def getLumiSerial(basepath):

    filename = os.path.join(basepath, "LastOpenSerial.txt")
    try:
        fp = open(filename, "r")
        serial = fp.read()
        serial = serial.split()[-1:][0]
        print(f"Serial {serial} read from {filename}")
        return serial
    except:
        return "0000000"


def upload(basepath="", serialnumber="0000000", current_machine_id = "00000000-0000-0000-0000-000000000000"):
    if not os.path.isdir(basepath):
        basepath = os.path.dirname(os.path.realpath(__file__))

    returntxt = f"LogDir: {basepath}\n"
    nc = nextcloud_client.Client.from_public_link(settings.public_link)
    if nc:
        filepattern = os.path.join(basepath, "*.pqlog")
        logfiles = glob.glob(filepattern)
        logfiles.sort()
        for logfilename in logfiles[:-1]:
            pre, ext = os.path.splitext(os.path.basename(logfilename))
            zipfilename = os.path.join(basepath, f"{serialnumber}_{current_machine_id}_{pre}.zip")
            zipObj = zipfile.ZipFile(zipfilename, "w")
            zipObj.write(
                logfilename, basename(logfilename), compress_type=zipfile.ZIP_DEFLATED
            )
            zipObj.close()

            if nc.drop_file(zipfilename):
                returntxt = returntxt + f"Uploaded: {zipfilename}\n"
                os.remove(logfilename)
            else:
                returntxt = returntxt + f"Upload Failed: {zipfilename}\n"
                os.remove(zipfilename)
    else:
        returntxt = returntxt + f"Connection failed"
    return returntxt


def init():
    if sys.platform == "win32":  # WinPath will only work on Windows
        path = winpath.get_common_appdata()
        defaultDir = os.path.join(path, "PicoQuant", "Luminosa", "Logs")
        current_machine_id = (
            subprocess.check_output("wmic csproduct get uuid")
            .decode()
            .split("\n")[1]
            .strip()
        )
        print(f"Machine ID: {current_machine_id}")
    else:
        defaultDir = "./"
        current_machine_id = "00000000-0000-0000-0000-000000000000"
        
    basepath = os.path.abspath(defaultDir)
    serialnumber = getLumiSerial(basepath)
    
    return [defaultDir, serialnumber, current_machine_id]


if __name__ == "__main__":
    [defaultDir, serialnumber,current_machine_id] = init()

    parser = ArgumentParser()
    parser.add_argument(
        "dir", help="Log Directory", type=str, nargs="?", default=defaultDir
    )
    args = parser.parse_args()

    if os.path.isdir(os.path.abspath(args.dir)):
        basepath = os.path.abspath(args.dir)
    else:
        basepath = os.path.abspath(defaultDir)

    print(f"trying to find {basepath}")
    if not os.path.isdir(basepath):
        basepath = os.path.dirname(os.path.realpath(__file__))
        print(f"Directory not found defaulting to {basepath}")

        print(f"Luminosa Serial Number: {serialnumber}")
    print(upload(basepath, serialnumber, current_machine_id))
