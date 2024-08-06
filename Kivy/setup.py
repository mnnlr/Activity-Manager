from cx_Freeze import setup, Executable

setup(
    name="Activity Monitor",
    version="1.0",
    description="Activity Monitor is an application to monitor the user intercation",
    executables=[Executable("monitor.py")],
)
