import time
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
import loguploader
import sys


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
            # servicemanager.LogInfoMsg("Service running...")
            servicemanager.LogInfoMsg(loguploader.upload())


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


if __name__ == "__main__":
    init()
