import nextcloud_client
import glob
import os
import zipfile
from argparse import ArgumentParser
from os.path import basename
import sys
from dropbox import public_link

import logging

logging.basicConfig(level=logging.DEBUG)


parser = ArgumentParser()
parser.add_argument("dir", help="log file directory", type=str, nargs="?", default="./")
args = parser.parse_args()
logging.debug(f"called with arguments: {args}")

basepath = os.path.abspath(args.dir)

if not os.path.isdir(basepath):
    basepath = os.path.dirname(os.path.realpath(__file__))
    logging.warning(f"No valid logfile path given. Using: {basepath} instead.")


logging.info(f"Logfile Path: {basepath}")


try:
    nc = nextcloud_client.Client.from_public_link(public_link)
except:
    logging.error(f"Cannot connect to {public_link}")
    sys.exit(1)

filepattern = os.path.join(basepath, "*.pqlog")
logging.debug(f"Logfile Pattern: {filepattern}")
for logfilename in glob.glob(filepattern):
    logging.info(f"Found: {logfilename}")
    pre, ext = os.path.splitext(logfilename)
    zipfilename = pre + ".zip"
    logging.debug(f"logfilename: {logfilename}")
    zipObj = zipfile.ZipFile(zipfilename, "w")
    zipObj.write(logfilename, basename(logfilename), compress_type=zipfile.ZIP_DEFLATED)
    zipObj.close()
    logging.info(f"Compressed: {logfilename} into: {zipfilename}")
    if nc.drop_file(zipfilename):
        logging.info(f"Uploaded: {zipfilename}")
        os.remove(logfilename)
        logging.debug(f"Deleted: {logfilename}")
    else:
        logging.error(f"Upload Failed: {zipfilename}")
        os.remove(zipfilename)
logging.info("Done.")
