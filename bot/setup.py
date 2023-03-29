from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["base.db"]
options = {
    'build_exe': {
        'include_files': packages,
    },
}

setup(
    name="Bot",
    options=options,
    version="3.1",
    description='My',
    executables=executables
)