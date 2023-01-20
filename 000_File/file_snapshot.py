import os
import time
import json
import shutil

from apscheduler.schedulers.background import BlockingScheduler


def Search_file_list(dir: str) -> dict:
    path = os.path.dirname(dir)
    file_list = []
    for path, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.abspath(
                os.path.join(path, file)))
    files = {}

    for file in file_list:
        files[file] = time.strftime(
            '%Y%m%d%H%M%S', time.localtime(os.path.getmtime(os.path.dirname(file))))
    return files


def Compare_file(jsonfile: str = '', file: dict = 0, backupdir: str = '', dir: str = "", main: str = '') -> list:
    inputdata = []
    try:
        with open(jsonfile, 'r', encoding='utf-8') as road_files:
            try:
                inputdata = json.load(road_files)
            except json.decoder.JSONDecodeError:
                inputdata = {}
    except FileNotFoundError:
        with open(jsonfile, 'w', encoding='utf-8') as road_files:
            json.dump(fp=road_files, ensure_ascii=False)
            inputdata = {}
    new_file = {}
    for i in file:
        if i in inputdata:
            if inputdata[i] != file[i]:
                inputdata[i] = file[i]
                new_file[i] = file[i]
        else:
            inputdata[i] = file[i]
            new_file[i] = file[i]

    Snapshot(dir, main, backupdir, new_file)
    with open(jsonfile, 'w', encoding='utf-8') as road_files:
        json.dump(inputdata, road_files, indent='\t', ensure_ascii=False)
    return new_file


def Snapshot(dir: str, main: str, backupdir: str, file_dict: dict):
    for file in file_dict:
        root = file[file.rfind(main)+7:]
        new_folder = root[:root.rfind('/')] if '/' in root else ""
        file_name = root[root.rfind('/')+1:]

        try:
            shutil.copy2(dir+root, backupdir+new_folder +
                         '/snapshot.'+file_dict[file]+file_name)
        except FileNotFoundError:
            os.makedirs(backupdir+new_folder)
            shutil.copy2(dir+root, backupdir+new_folder +
                         '/snapshot.'+file_dict[file]+file_name)


def main():
    MAIN_DIR = 'folder/'
    SRC_DIR = f'/path/{MAIN_DIR}'
    BACKUP_DIR = '/path/'
    JsonFile = 'indexing_list.json'
    FILE = Search_file_list(SRC_DIR)
    Compare_file(JsonFile, FILE, BACKUP_DIR, SRC_DIR, MAIN_DIR)


def schedulers():
    sched = BlockingScheduler(timezone='utc')
    # seconds | minutes | hours
    sched.add_job(main, 'interval', seconds=2, id='main')
    sched.start()


if __name__ == "__main__":
    schedulers()
