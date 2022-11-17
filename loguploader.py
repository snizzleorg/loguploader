import nextcloud_client
import glob
import os
import zipfile
from os.path import basename
import sys
from dropbox import public_link
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
            upload()


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

    basepath = ""

    if not os.path.isdir(basepath):
        basepath = os.path.dirname(os.path.realpath(__file__))
        servicemanager.LogInfoMsg(
            f"No valid Log Directory given. Using: {basepath} instead."
        )

    servicemanager.LogInfoMsg(f"Log Directory: {basepath}")

    try:
        nc = nextcloud_client.Client.from_public_link(public_link)
        filepattern = os.path.join(basepath, "*.pqlog")
        servicemanager.LogInfoMsg(f"Log File Pattern: {filepattern}")
        for logfilename in glob.glob(filepattern):
            servicemanager.LogInfoMsg(f"Found: {logfilename}")
            pre, ext = os.path.splitext(logfilename)
            zipfilename = pre + ".zip"
            servicemanager.LogInfoMsg(f"Log File Name: {logfilename}")
            zipObj = zipfile.ZipFile(zipfilename, "w")
            zipObj.write(
                logfilename, basename(logfilename), compress_type=zipfile.ZIP_DEFLATED
            )
            zipObj.close()
            servicemanager.LogInfoMsg(f"Compressed: {logfilename} into: {zipfilename}")
            if nc.drop_file(zipfilename):
                servicemanager.LogInfoMsg(f"Uploaded: {zipfilename}")
                os.remove(logfilename)
                servicemanager.LogInfoMsg(f"Deleted: {logfilename}")
            else:
                servicemanager.LogInfoMsg(f"Upload Failed: {zipfilename}")
                os.remove(zipfilename)
        servicemanager.LogInfoMsg("Done.")
    except:
        servicemanager.LogInfoMsg(f"Cannot connect to {public_link}")


if __name__ == "__main__":
    init()
