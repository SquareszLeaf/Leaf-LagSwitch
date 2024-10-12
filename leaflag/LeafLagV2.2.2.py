import tkinter as tk
import subprocess
import ctypes
import atexit
import keyboard
import psutil
import sys

class LagSwitchApp:
    def __init__(self):
        self.settings = {"Keybind": "`", "Lagswitch": "on"}
        self.block_flag = self.settings["Lagswitch"] == "off"
        self.root = tk.Tk()
        self.root.title("Lag")
        self.root.wm_attributes("-topmost", 1)
        self.setup_ui()
        self.check_requirements()
        self.setup_keybind()

    def setup_ui(self):
        self.status_label = tk.Label(self.root, text="LagSwitch off.", fg="red")  # Default color is red
        self.status_label.grid(row=1, column=0)

        self.label = tk.Label(text="Made by Squaresz")
        self.label.grid(row=1, column=2)

        self.label = tk.Label(text="Version 2.2.2")
        self.label.grid(row=2, column=2)

        self.keybind_label = tk.Label(self.root, text=f"Keybind: {self.settings['Keybind']}")
        self.keybind_label.grid(row=2, column=0)

        self.change_button = tk.Button(self.root, text="Change Keybind", command=self.change_keybind)
        self.change_button.grid(row=3, column=0)

        self.always_on_top_var = tk.BooleanVar(value=True)
        self.always_on_top_checkbox = tk.Checkbutton(self.root, text="Always on Top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        self.always_on_top_checkbox.grid(row=3, column=2)

        self.root.geometry("200x70")
        self.root.resizable(False, False)

    def check_requirements(self):
        roblox_running = any(proc.name() == 'RobloxPlayerBeta.exe' for proc in psutil.process_iter())
        if not roblox_running:
            ctypes.windll.user32.MessageBoxW(0, "Roblox not detected.", "Roblox Not Found", 0)
            sys.exit()

        if not self.is_admin():
            ctypes.windll.user32.MessageBoxW(0, "Please run the program as an administrator.", "Administrator Privileges Required", 0)
            sys.exit()

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            print("Error checking admin privileges:", e)
            return False

    def toggle_always_on_top(self):
        self.root.attributes("-topmost", self.always_on_top_var.get())

    def change_keybind(self):
        self.keybind_label.config(text="Press a key...")
        keyboard.on_press(callback=self.set_keybind)

    def set_keybind(self, event):
        new_keybind = event.name
        self.settings["Keybind"] = new_keybind
        self.keybind_label.config(text=f"Keybind: {new_keybind}")
        keyboard.unhook_all()
        keyboard.on_press_key(self.settings["Keybind"], self.toggle_block)

    def toggle_block(self, event):
        if event.name == self.settings["Keybind"]:
            self.block_flag = not self.block_flag
            self.update_firewall_rules("block" if self.block_flag else "delete")
            self.status_label.config(text="LagSwitch on." if self.block_flag else "LagSwitch off.", fg="green" if self.block_flag else "red")

    def update_firewall_rules(self, action):
        process = next((proc for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'] == 'RobloxPlayerBeta.exe'), None)
        if process:
            path = process.exe()
            command = ["netsh", "advfirewall", "firewall"]
            command += ["add", "rule", "name=Roblox_Block", "dir=out", "action=block", f"program={path}"] if action == "block" else ["delete", "rule", "name=Roblox_Block"]
            subprocess.run(command)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Roblox Game Client not found in Task Manager.", "Process Not Found", 0)
            sys.exit()

    def setup_keybind(self):
        keyboard.on_press_key(self.settings["Keybind"], self.toggle_block)

    def run(self):
        atexit.register(self.exit_handler)
        self.root.mainloop()

    def exit_handler(self):
        self.update_firewall_rules("delete")

if __name__ == "__main__":
    app = LagSwitchApp()
    app.run()
