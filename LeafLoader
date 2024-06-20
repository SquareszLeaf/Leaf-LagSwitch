# LoaderV1.0.4
import os
import sys
import requests
import hashlib
import subprocess
import customtkinter as ctk
from tkinter import messagebox
import re


class ScriptUpdater:
    def __init__(self, script_url, save_directory):
        self.script_url = script_url
        self.save_directory = save_directory
        self.local_script_path = None
        self.remote_script_content = None

        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Leaf Loader V1.0.4")
        self.root.geometry("400x275")  # Adjusted height to accommodate new button
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.create_widgets()
        self.update_versions_listbox()

    def create_widgets(self):
        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.check_update_button = ctk.CTkButton(self.button_frame, text="Check For Updates", command=self.check_for_update)
        self.check_update_button.grid(row=0, column=0, sticky="ew", pady=5)

        self.run_latest_button = ctk.CTkButton(self.button_frame, text="Run Latest Version", command=self.run_latest_version)
        self.run_latest_button.grid(row=1, column=0, sticky="ew", pady=5)

        self.run_older_button = ctk.CTkButton(self.button_frame, text="Run Selected Version", command=self.run_older_version)
        self.run_older_button.grid(row=2, column=0, sticky="ew", pady=5)

        self.delete_version_button = ctk.CTkButton(self.button_frame, text="Delete Selected Version", command=self.delete_selected_version)
        self.delete_version_button.grid(row=3, column=0, sticky="ew", pady=5)

        self.open_folder_button = ctk.CTkButton(self.button_frame, text="Open Folder", command=self.open_folder)
        self.open_folder_button.grid(row=4, column=0, sticky="ew", pady=5)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.root, width=190, height=100, label_text="Versions")
        self.scrollable_frame.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")

        self.selected_version = ctk.StringVar()

        self.credits = ctk.CTkLabel(self.root, text="Made By Squaresz")
        self.credits.grid(row=0, column=0, columnspan=1, pady=(200, 0))

    def run(self):
        self.root.mainloop()

    def get_remote_script_content(self):
        try:
            response = requests.get(self.script_url, timeout=3)
            if response.status_code == 200:
                self.remote_script_content = response.text
                print("Successfully retrieved remote script content.")
            else:
                print("Failed to retrieve script from URL. Status code:", response.status_code)
        except requests.RequestException as e:
            print("Error:", e)

    def extract_script_name(self):
        first_line = self.remote_script_content.split('\n', 1)[0]
        if first_line.startswith('#'):
            return first_line[1:].strip()
        return "LeafLag"

    def save_remote_script(self):
        if self.remote_script_content:
            if not os.path.exists(self.save_directory):
                os.makedirs(self.save_directory)

            script_name = self.extract_script_name()
            self.local_script_path = os.path.join(self.save_directory, f"{script_name}.py")

            with open(self.local_script_path, 'w', newline='\n') as file:
                file.write(self.remote_script_content)
            print(f"Saved new script version as {self.local_script_path}")

    def delete_selected_version(self):
        selected_version = self.selected_version.get()
        if selected_version:
            script_path = os.path.join(self.save_directory, selected_version)
            if os.path.exists(script_path):
                os.remove(script_path)
                self.update_versions_listbox()
                messagebox.showinfo("Delete", f"Version {selected_version} deleted successfully.")
            else:
                messagebox.showerror("Error", "Selected version not found.")
        else:
            messagebox.showerror("Error", "No version selected.")

    def list_versions(self):
        return sorted(f for f in os.listdir(self.save_directory) if f.endswith('.py') and os.path.isfile(os.path.join(self.save_directory, f)))

    def normalize_content(self, content):
        return content.replace('\r\n', '\n').strip()

    def is_script_different(self):
        versions = self.list_versions()
        if not versions:
            print("No previous script version found.")
            return True

        latest_script_path = os.path.join(self.save_directory, self.get_latest_version(versions))

        with open(latest_script_path, 'r', newline='\n') as file:
            local_content = file.read()

        remote_normalized = self.normalize_content(self.remote_script_content)
        local_normalized = self.normalize_content(local_content)

        remote_hash = hashlib.md5(remote_normalized.encode()).hexdigest()
        local_hash = hashlib.md5(local_normalized.encode()).hexdigest()

        is_different = remote_hash != local_hash
        if is_different:
            print("Remote script is different from the local script.")
        else:
            print("Remote script is the same as the local script.")

        return is_different

    def run_script(self, script_path):
        if script_path:
            print(f"Running script {script_path}")
            self.root.withdraw()
            try:
                result = subprocess.run(["pythonw", script_path], capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"Error running script: {e}")
                messagebox.showerror("Error", f"Error running script: {e}")
            self.root.deiconify()

    def select_version_to_run(self):
        selected_version = self.selected_version.get()
        if selected_version:
            script_path = os.path.join(self.save_directory, selected_version)
            return script_path
        else:
            messagebox.showerror("Error", "No version selected.")
            return None

    def check_for_update(self):
        self.get_remote_script_content()
        if self.remote_script_content:
            if self.is_script_different():
                self.save_remote_script()
                self.update_versions_listbox()
                messagebox.showinfo("Update", "New version downloaded and saved.")
            else:
                messagebox.showinfo("Update", "You are up to date.")
        else:
            messagebox.showerror("Error", "Failed to retrieve script.(prob 404)")
        self.update_versions_listbox()

    def run_latest_version(self):
        versions = self.list_versions()
        if not versions:
            print("No versions available. Checking for updates...")
            self.check_for_update()
            versions = self.list_versions()  # Re-fetch versions after attempting update
            if not versions:
                messagebox.showerror("Error", "No versions available to run.")
                return

        latest_version = self.get_latest_version(versions)
        latest_script_path = os.path.join(self.save_directory, latest_version)
        if os.path.exists(latest_script_path):
            self.run_script(latest_script_path)
        else:
            self.check_for_update()
        self.update_versions_listbox()

    def run_older_version(self):
        selected_script_path = self.select_version_to_run()
        if selected_script_path:
            self.run_script(selected_script_path)
        self.update_versions_listbox()

    def open_folder(self):
        if sys.platform == "win32":
            os.startfile(self.save_directory)
            self.update_versions_listbox()

    def update_versions_listbox(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        versions = self.list_versions()
        for version in versions:
            radio_button = ctk.CTkRadioButton(self.scrollable_frame, text=version, variable=self.selected_version, value=version)
            radio_button.pack(fill="x", padx=10, pady=5)

    def get_latest_version(self, versions):
        def parse_version(version):
            match = re.search(r'V?(\d+\.\d+\.\d+)', version)
            if match:
                return tuple(map(int, match.group(1).split('.')))
            return (0, 0, 0)

        versions.sort(key=parse_version, reverse=True)
        return versions[0]


def main():
    script_url = "https://raw.githubusercontent.com/LEAVEMEALONEHITHUB/NRQWO43XNF2GG2DMN5QWIZLS/main/leaflag.py"

    if getattr(sys, 'frozen', False):
        save_directory = os.path.join(os.path.dirname(sys.executable), "Leaf_Loader")
    else:
        save_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Leaf_Loader")

    updater = ScriptUpdater(script_url, save_directory)
    updater.run()


if __name__ == "__main__":
    main()
