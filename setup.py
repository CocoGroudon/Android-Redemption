import cx_Freeze
import os
import sys
import settings

program_name = "Android-Redemption"
ignorefiles = [".gitignore"]
ignoredicts = ["git", "__pycache__", "build"]

dict_len = len(settings.dictPath)
dict_len += 1
files = []
for item in os.walk(f"{settings.dictPath}"):
    # print(item)
    skip = False
    for dict in ignoredicts:
        if dict in str(item[0]):
            skip = True
            break
    for ignorefile in ignorefiles:
        for file in reversed(item[2]):
            if file.endswith(ignorefile):
                item[2].remove(file)
    if skip: continue
    for file in item[2]:
        res = f"{item[0]}/{file}"
        res = res[dict_len:]
        files.append(res)

print(files)


base = None
if sys.platform == "win32":
    base = "Win32GUI"


executables = [cx_Freeze.Executable("main.py", 
                                    base=base
                                    )]

cx_Freeze.setup(
    name=program_name,
    version = "0.1",
    description = "A Game",
    executables = executables,
    options={
        "build_exe": {
            "packages":["pygame", "numpy"],
            "include_files":files,
            "path":sys.path
            }
        }
    )