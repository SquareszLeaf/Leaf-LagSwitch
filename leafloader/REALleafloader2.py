import os
import requests
import hashlib
import subprocess
import sys

URL = "https://raw.githubusercontent.com/SquareszLeaf/Leaf-LagSwitch/main/leafloader.py"
FOLDER_NAME = "Leaf_Loader"
LOCAL_FILE = os.path.join(FOLDER_NAME, "leafloader.py")

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_file(url, local_file):
    response = requests.get(url)
    response.raise_for_status()
    with open(local_file, 'wb') as file:
        file.write(response.content)

def file_checksum(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    return hashlib.sha256(file_content).hexdigest()

def check_for_update():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.RequestException:
        print("Could not connect to the internet to check for updates. Skipping update check.")
        return False, None
    
    remote_checksum = hashlib.sha256(response.content).hexdigest()
    
    if os.path.exists(LOCAL_FILE):
        local_checksum = file_checksum(LOCAL_FILE)
        if local_checksum != remote_checksum:
            with open(LOCAL_FILE, 'wb') as file:
                file.write(response.content)
            print(f"{LOCAL_FILE} has been updated.")
        else:
            print(f"{LOCAL_FILE} is up to date.")
    else:
        with open(LOCAL_FILE, 'wb') as file:
            file.write(response.content)
        print(f"{LOCAL_FILE} has been downloaded.")
    
    return True, remote_checksum

def main():
    ensure_directory_exists(FOLDER_NAME)
    # Run the script before checking for updates
    check_for_update()
    if os.path.exists(LOCAL_FILE):
        # Use subprocess to run the script without opening a new console window
        if sys.platform == "win32":
            subprocess.run(['pythonw', LOCAL_FILE], check=True)
        else:
            subprocess.run(['python', LOCAL_FILE], check=True)
    else:
        print(f"{LOCAL_FILE} does not exist. Downloading it first.")
        download_file(URL, LOCAL_FILE)
        if sys.platform == "win32":
            subprocess.run(['pythonw', LOCAL_FILE], check=True)
        else:
            subprocess.run(['python', LOCAL_FILE], check=True)

if __name__ == "__main__":
    main()
