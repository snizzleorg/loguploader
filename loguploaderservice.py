import time
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
import loguploader
import sys
import win32timezone


class LumiLogUploadService:
    """Luminosa Log Upload Service"""

    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        self.running = True
        while self.running:
            servicemanager.LogInfoMsg("Service running...")
            [defaultDir, serialnumber, currentMachineID] = loguploader.init()
            servicemanager.LogInfoMsg(f"Log Directory: {defaultDir}")
            servicemanager.LogInfoMsg(f"System Serial Number: {serialnumber}")
            servicemanager.LogInfoMsg(f"ID: {currentMachineID}")
            rtn = loguploader.copyDB(basepath=defaultDir)
            servicemanager.LogInfoMsg(rtn)
            servicemanager.LogInfoMsg(rtn)
            rtn = loguploader.uploadSettings(
                basepath=defaultDir,
                serialnumber=serialnumber,
                current_machine_id=currentMachineID,
            )
            servicemanager.LogInfoMsg(rtn)
            rtn = loguploader.uploadUserSettings(
                basepath=defaultDir,
                serialnumber=serialnumber,
                current_machine_id=currentMachineID,
            )
            servicemanager.LogInfoMsg(rtn)
            rtn = loguploader.uploadLaserPowerLog(
                basepath=defaultDir,
                serialnumber=serialnumber,
                current_machine_id=currentMachineID,
            )
            rtn = loguploader.uploadlog(
                basepath=defaultDir,
                serialnumber=serialnumber,
                current_machine_id=currentMachineID,
            )
            servicemanager.LogInfoMsg(rtn)
            time.sleep(300)


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
        servicemanager.LogInfoMsg("Loguploader Service started")
    else:
        win32serviceutil.HandleCommandLine(LumiLogUploadServiceFramework)


if __name__ == "__main__":
    init()
