from requests import get
from shutil import copyfile, copytree
import datetime
import os
import tarfile

copy_mods = False
fp = get_server_dir()
time = get_time()

def get_latest_server(fp):
    url = "https://factorio.com/get-download/stable/headless/linux64"
    filename = "/factorio-headless-stable.tar.xz"
    print("Downloading latest stable server...")
    temp = get(url, allow_redirects=True)
    print("Download Complete! Saving file to:", fp + filename)
    open(fp + filename, 'wb').write(temp.content)

def get_time():
    return(datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))

def get_server_dir():
    try:
        fp = input("Enter fp to location server is stored in:")
        if 'factorio' in os.listdir(fp + '/factorio/bin/x64'):
            return(fp)
        else:
            print("Incorrect filepath")
            quit()
    except Exception as error:
        print(error)
        quit()

def rename_server(fp, time):
    print("Renaming existing server...")
    try:
        os.rename(fp + '/factorio' , fp + '/factorio' + time)
    except Exception as error:
        print(error)
        quit()

def extract_tar(fp, time):
    rename_server(fp, time)
    print("Extracting tar...")
    try:
        with tarfile.open(fp + '/factorio-headless-stable.tar.xz', 'r') as tar:
            tar.extractall(fp)
    except Exception as error:
        print(error)

def copy_server_data(fp,time,copy_mods):
    files_to_copy = ['/achievements.dat', '/player-data.json', '/data/server-settings.json', '/data/server-whitelist.json']
    print("Copying server files...")
    for i in files_to_copy:
        try:
            copyfile(fp + '/factorio' + time + i, fp + '/factorio' + i)
            print("Copied", i)
        except FileNotFoundError as error:
            print("the following file failed to copy:", error)
    if copy_mods:
        print("Copying mods...")
        try:
            copytree(fp + '/factorio' + time + '/mods', fp + '/factorio/mods')
        except Exception as error:
            print(error)
            print("Unable to copy mods")

if input("would you like to copy mods? y/n:").lower() == 'y':
    copy_mods = True

get_latest_server(fp)
extract_tar(fp, time)
copy_server_data(fp,time,copy_mods)

print("Done")
