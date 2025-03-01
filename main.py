import os
import platform
import shutil
import subprocess
import shlex
url = "http://158.160.166.58:30002/messages"
headers = "Content-Type: application/json"


def install_custom_clang(syst):
    if syst == "Ubuntu":
        res = subprocess.run(["dpkg","-s","dobri-clang-tidy"], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        if res.returncode != 0:
            link = "https://downloader.disk.yandex.ru/disk/e0314e79388bef965c0b5e5bd0aa64d72520b5408d06e966d1d54d1ac581340d/67c2349d/J7_XO_jRy0WRNiQk2sRSelg6O-jOAJDuQYPBHutEeRp_dL28hqJgEnP7fKR6nceJFTz8Z_JQqS0UOQMlEGeuNQ%3D%3D?uid=0&filename=dobri-clang-tidy.deb&disposition=attachment&hash=jNLX%2B2tYX1hxbASuQON4TPNFT6WaBuxYjLQCMVSNiWmHmFFsZRnt6XvaownU6u4hq/J6bpmRyOJonT3VoXnDag%3D%3D&limit=0&content_type=application%2Fvnd.debian.binary-package&owner_uid=2014468968&fsize=205655362&hid=2190ee0b1bd351ef426b8a78ce61ef0c&media_type=compressed&tknv=v2"
            quoted_link = shlex.quote(link)
            subprocess.run(f"wget -O dobri-clang-tidy.deb {quoted_link}", shell=True)
            subprocess.run("sudo dpkg -i  --force-overwrite dobri-clang-tidy.deb; rm dobri-clang-tidy.deb", shell=True)
        res = subprocess.run(["dpkg","-s","dobri-clang-format"], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        if res.returncode != 0:
            link = "https://downloader.disk.yandex.ru/disk/5cb6a6abdbbc8c8c823246c0faa0b8951182433144751e564bd9c2110a3bc2e1/67c2488c/J7_XO_jRy0WRNiQk2sRSelOVP8hQHD1rhaLF0NfQAS_bQanQPjXwWfF06Q838ZzdA_dP_gZYGdBmcDnZNne3ew%3D%3D?uid=0&filename=dobri-clang-format.deb&disposition=attachment&hash=8V9AB40BezPQTRw9JzU8iJ3AqgojtHIuLCvuYhNZAP2K3JTQY7HPiEA6aQl3jtwJq/J6bpmRyOJonT3VoXnDag%3D%3D&limit=0&content_type=application%2Fvnd.debian.binary-package&owner_uid=2014468968&fsize=32794020&hid=5716110e52543b092502eeca0397496e&media_type=compressed&tknv=v2"
            quoted_link = shlex.quote(link)
            subprocess.run(f"wget -O dobri-clang-format.deb {quoted_link}", shell=True)
            subprocess.run("sudo dpkg -i dobri-clang-format.deb; rm dobri-clang-format.deb", shell=True)

def copy_config(dir, code_to_add):
    with open(dir + "/QtCreator.ini", "a", encoding="utf-8") as dest:
        dest.write("\n" + code_to_add)
    shutil.copy(dir + "/QtCreator.ini", dir + "/QtCreatorBackup.ini")
    destination_folder = dir + "/qtcreator"
    shutil.copytree("beautifier", os.path.join(destination_folder, os.path.basename("beautifier")), dirs_exist_ok=True)
    shutil.copytree("clang-format", os.path.join(destination_folder, os.path.basename("clang-format")),
                    dirs_exist_ok=True)
    if platform.system() == "Darwin":
        shutil.copy("forMac/profiles.xml", destination_folder)
        shutil.copy("forMac/qtversion.xml", destination_folder)


def install_updates(dir, syst):
    subprocess.run(['git', '-C', '.', 'reset', '--hard'])
    subprocess.run(['git', '-C', '.', 'pull'])
    if syst == "Ubuntu":
        with open("forConfigUbuntu.ini", "r", encoding="utf-8") as src:
            code_to_add = src.read()
        install_custom_clang(syst)
    elif syst == "MacOS":
        with open("forConfigMac.ini", "r", encoding="utf-8") as src:
            code_to_add = src.read()
    remove_old_config(dir + "/QtCreator.ini", "[Beautifier]", "ForceEnabled=Beautifier")
    with open(dir + "/QtCreator.ini", "a", encoding="utf-8") as dest:
        dest.write("\n" + code_to_add)
    file_path = "beautifier/clangformat/google/.clang-format"
    with open(file_path, "r") as code_style:
        code_to_add = code_style.read()
    destination_folder = dir + "/qtcreator/"
    with open(destination_folder + file_path, "w") as file:
        file.write(code_to_add)


def check_install(surname):
    print("\n(!) ОБЯЗАТЕЛЬНО ПЕРЕЗАПУСТИТЕ Qt Creator (!) Для проверки установки проделайте шаги указанные в файле check.txt, если все успешно, нажмите Y, иначе N")
    while (True):
        user_input = input().strip().upper()
        if user_input == 'Y':
            subprocess.run([
                "curl",
                "-X", "POST",
                "-d", f'{{"message": "{surname + ":OK"}"}}',
                "-H", headers,
                url
            ])
            break
        elif user_input == 'N':
            subprocess.run([
                "curl",
                "-X", "POST",
                "-d", f'{{"message": "{surname + ":FAIL"}"}}',
                "-H", headers,
                url
            ])
            break
        else:
            print("Неверный ввод! Пожалуйста, нажмите Y или N.")


def remove_old_config(file_path, start_marker, end_marker):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    inside_range = False
    result_lines = []

    for line in lines:
        if start_marker in line:
            inside_range = True
            continue

        if end_marker in line:
            inside_range = False
            continue

        if not inside_range:
            result_lines.append(line)
    with open(file_path, 'w') as file:
        file.writelines(result_lines)


def check_git_updates():
    subprocess.run(['git', '-C', '.', 'fetch'], check=True)

    result = subprocess.run(
        ['git', '-C', '.', 'log', f'HEAD..origin/main', '--oneline'],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip()


if platform.system() == "Linux":
    
    dir = os.getenv('HOME') + "/.config/QtProject"
    if os.path.exists(dir + "/QtCreatorBackup.ini"):
        print("Поиск обновлений")
        if check_git_updates():
            print("Найдено обновление")
            install_updates(dir, "Ubuntu")
            print("Обновление установлено")
        else:
            print("Обновление не найдено")
    else:
        print("Введите фамилию: ")
        surname = input()
        with open("forConfigUbuntu.ini", "r", encoding="utf-8") as src:
            code_to_add = src.read()
        copy_config(dir, code_to_add)
        install_custom_clang("Ubuntu")
        subprocess.run(
            "sudo apt update; sudo apt upgrade -y; sudo apt install -y curl; sudo apt install -y clazy; sudo apt install -y cmake; sudo apt-get install -f;",
            shell=True)
        check_install(surname)

elif platform.system() == "Darwin":
    dir = os.getenv('HOME') + "/.config/QtProject"
    if os.path.exists(dir + "/QtCreatorBackup.ini"):
        print("Поиск обновлений")
        if check_git_updates():
            print("Найдено обновление")
            install_updates(dir, "MacOS")
            print("Обновление установлено")
        else:
            print("Обновление не найдено")
    else:
        print("Введите фамилию: ")
        surname = input()
        with open("forConfigMac.ini", "r", encoding="utf-8") as src:
            code_to_add = src.read()
        copy_config(dir, code_to_add)
        subprocess.run("brew update && brew upgrade && brew install llvm && brew install clazy && brew install cmake",
                       shell=True)
        check_install(surname)
