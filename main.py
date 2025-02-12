import os
import platform
import shutil
import subprocess
if platform.system == "Linux":
    dir = os.getenv('HOME') + "/.config/QtProject"
    with open("forConfig.ini", "r", encoding="utf-8") as src:
        code_to_add = src.read()
    with open(dir+"/QtCreator.ini", "a", encoding="utf-8") as dest:
        dest.write("\n"+code_to_add)
    source_folder = "beautifier"
    destination_folder = dir+"/qtcreator"
    shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)), dirs_exist_ok=True)
    source_folder = "clang-format"
    shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)), dirs_exist_ok=True)
    subprocess.run("sudo apt install clazy && sudo apt install clang-format", shell=True)
elif platform.system == "Windows":