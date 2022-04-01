import nextcloud_client
import glob
import os
import zipfile
from argparse import ArgumentParser
from os.path import basename
import sys
from dropbox import public_link

parser = ArgumentParser()
parser.add_argument("dir", help="log file directory", type=str, nargs="?", default="./")
args = parser.parse_args()
basepath = os.path.abspath(args.dir)
if not os.path.isdir(basepath):
    basepath = os.path.dirname(os.path.realpath(__file__))


print("Reading logs from %s" % basepath)


try:
    nc = nextcloud_client.Client.from_public_link(public_link)
except:
    print("Connection error")
    sys.exit(1)

filepattern = os.path.join(basepath, "*.pqlog")
print(filepattern)
for logfilename in glob.glob(filepattern):
    print(logfilename)
    pre, ext = os.path.splitext(logfilename)
    zipfilename = pre + ".zip"
    print(zipfilename)
    zipObj = zipfile.ZipFile(zipfilename, "w")
    zipObj.write(logfilename, basename(logfilename), compress_type=zipfile.ZIP_DEFLATED)
    if nc.drop_file(zipfilename):
        print("success")
        os.remove(logfilename)
    else:
        os.remove(zipfilename)
