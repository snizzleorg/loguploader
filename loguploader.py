import nextcloud_client
import glob
import os
import zipfile
from os.path import basename
from argparse import ArgumentParser
from dropbox import public_link
from systemdb import getSerialFromJennyDB


def upload(basepath="", serialnumber=""):

    if not os.path.isdir(basepath):
        basepath = os.path.dirname(os.path.realpath(__file__))
        return False
    returntxt = f"LogDir: {basepath}\n"
    try:
        nc = nextcloud_client.Client.from_public_link(public_link)
        filepattern = os.path.join(basepath, "*.pqlog")
        logfiles = glob.glob(filepattern)
        for logfilename in logfiles:
            pre, ext = os.path.splitext(os.path.basename(logfilename))
            zipfilename = os.path.join(basepath, serialnumber + "_" + pre + ".zip")
            print(zipfilename)
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
    except:
        returntxt = returntxt + f"Connection failed"
    return returntxt


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("dir", help="Log Directory", type=str, nargs="?", default="./")
    args = parser.parse_args()
    basepath = os.path.abspath(args.dir)
    serialnumber = getSerialFromJennyDB()
    if not serialnumber:
        print(f"Error getting Luminosa Serial Number")
    else:
        print(f"Luminosa Serial Number: {serialnumber}")
        print(upload(basepath, serialnumber))
