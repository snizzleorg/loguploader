import winpath
import sys
import os

if sys.platform == "win32":  # WinPath will only work on Windows
    path = winpath.get_common_appdata()
    print(os.path.join(path, "Luminosa", "Logs"))
