import nextcloud_client
import glob
import os
import zipfile
from argparse import ArgumentParser
from os.path import basename
import sys
from dropbox import public_link
import logging
import time

import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging


class LumiLogUploadService:
    """Luminosa Log Upload Service"""

    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        self.running = True
        while self.running:
            time.sleep(10)  # Important work
            servicemanager.LogInfoMsg("Service running...")


class LumiLogUploadServiceFramework(win32serviceutil.ServiceFramework):

    _svc_name_ = "LumiLogUploadService"
    _svc_display_name_ = "Luminosa Log Upload Service"

    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """Start the service; does not return until stopped"""
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = LumiLogUploadService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Run the service
        self.service_impl.run()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(LumiLogUploadServiceFramework)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(LumiLogUploadServiceFramework)


def upload():
    logging.basicConfig(level=logging.DEBUG)

    parser = ArgumentParser()
    parser.add_argument("dir", help="Log Directory", type=str, nargs="?", default="./")
    args = parser.parse_args()
    logging.debug(f"Called with Arguments: {args}")

    basepath = os.path.abspath(args.dir)

    if not os.path.isdir(basepath):
        basepath = os.path.dirname(os.path.realpath(__file__))
        logging.warning(f"No valid Log Directory given. Using: {basepath} instead.")

    logging.info(f"Log Directory: {basepath}")

    try:
        nc = nextcloud_client.Client.from_public_link(public_link)
    except:
        logging.error(f"Cannot connect to {public_link}")
        sys.exit(1)

    filepattern = os.path.join(basepath, "*.pqlog")
    logging.debug(f"Log File Pattern: {filepattern}")
    for logfilename in glob.glob(filepattern):
        logging.info(f"Found: {logfilename}")
        pre, ext = os.path.splitext(logfilename)
        zipfilename = pre + ".zip"
        logging.debug(f"Log File Name: {logfilename}")
        zipObj = zipfile.ZipFile(zipfilename, "w")
        zipObj.write(
            logfilename, basename(logfilename), compress_type=zipfile.ZIP_DEFLATED
        )
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


if __name__ == "__main__":
    init()
