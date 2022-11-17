import nextcloud_client
import glob
import os
import zipfile
from os.path import basename
from argparse import ArgumentParser
from dropbox import public_link


def upload(basepath):

    basepath = ""

    if not os.path.isdir(basepath):
        basepath = os.path.dirname(os.path.realpath(__file__))
    returntxt = f"LogDir: {basepath}"
    try:
        nc = nextcloud_client.Client.from_public_link(public_link)
        filepattern = os.path.join(basepath, "*.pqlog")
        for logfilename in glob.glob(filepattern):
            pre, ext = os.path.splitext(logfilename)
            zipfilename = pre + ".zip"
            zipObj = zipfile.ZipFile(zipfilename, "w")
            zipObj.write(
                logfilename, basename(logfilename), compress_type=zipfile.ZIP_DEFLATED
            )
            zipObj.close()

            if nc.drop_file(zipfilename):
                returntxt = f"Uploaded: {zipfilename}"
                os.remove(logfilename)
            else:
                returntxt = f"Upload Failed: {zipfilename}"
                os.remove(zipfilename)
    except:
        returntxt = f"Upload Failed"
    return returntxt


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("dir", help="Log Directory", type=str, nargs="?", default="./")
    args = parser.parse_args()
    basepath = os.path.abspath(args.dir)

    print(upload(basepath))
