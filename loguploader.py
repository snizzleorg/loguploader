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
logging.debug("called with arguments: %s" % args)

basepath = os.path.abspath(args.dir)

if not os.path.isdir(basepath):
    basepath = os.path.dirname(os.path.realpath(__file__))
    logging.warning("No valid logfile path given. Using: %s instead." % basepath)


logging.info("Logfile Path: %s" % basepath)


try:
    nc = nextcloud_client.Client.from_public_link(public_link)
except:
    logging.error("Cannot connect to %s" % public_link)
    sys.exit(1)

filepattern = os.path.join(basepath, "*.pqlog")
logging.debug("Logfile Pattern: %s" % filepattern)
for logfilename in glob.glob(filepattern):
    logging.info("Found: %s" % logfilename)
    pre, ext = os.path.splitext(logfilename)
    zipfilename = pre + ".zip"
    logging.debug("logfilename: %s" % logfilename)
    zipObj = zipfile.ZipFile(zipfilename, "w")
    zipObj.write(logfilename, basename(logfilename), compress_type=zipfile.ZIP_DEFLATED)
    zipObj.close()
    logging.info("Compressed: %s Into: %s" % (logfilename, zipfilename))
    if nc.drop_file(zipfilename):
        logging.info("Uploaded: %s" % zipfilename)
        os.remove(logfilename)
        logging.debug("Deleted: %s" % logfilename)
    else:
        logging.error("Upload Failed: %s" % zipfilename)
        os.remove(zipfilename)
logging.info("Done.")
