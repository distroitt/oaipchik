import os
import platform
import shutil
import subprocess
if platform.system() == "Linux":
    print("Введите фамилию: )
    surname = input()
    dir = os.getenv('HOME') + "/.config/QtProject"
    with open("forConfigUbuntu.ini", "r", encoding="utf-8") as src:
        code_to_add = src.read()
    with open(dir+"/QtCreator.ini", "a", encoding="utf-8") as dest:
        dest.write("\n"+code_to_add)
    source_folder = "beautifier"
    destination_folder = dir+"/qtcreator"
    shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)), dirs_exist_ok=True)
    source_folder = "clang-format"
    shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)), dirs_exist_ok=True)
    subprocess.run("sudo apt update && sudo apt upgrade -y && sudo apt install -y clazy && sudo apt install -y clang-format && sudo apt install -y cmake && sudo apt-get install -f", shell=True)
    print("Для проверки установки проделайте шаги указанные в файле check.txt, если все успешно, нажмите Y, иначе N")
    while True:
        user_input = input().strip().upper()
        if user_input == 'Y':
            pass
        elif user_input == 'N':
            pass
        else:
        print("Неверный ввод! Пожалуйста, нажмите Y или N.")
elif platform.system() == "Darwin":
    dir = os.getenv('HOME') + "/.config/QtProject"
    with open("forConfigMac.ini", "r", encoding="utf-8") as src:
        code_to_add = src.read()
    with open(dir+"/QtCreator.ini", "a", encoding="utf-8") as dest:
        dest.write("\n"+code_to_add)
    source_folder = "beautifier"
    destination_folder = dir+"/qtcreator"
    shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)), dirs_exist_ok=True)
    source_folder = "clang-format"
    shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)), dirs_exist_ok=True)
