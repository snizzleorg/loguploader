import winpath
import sys
import winpath

if sys.platform == "win32":  # WinPath will only work on Windows
    path = winpath.get_common_appdata()
    print(path)
