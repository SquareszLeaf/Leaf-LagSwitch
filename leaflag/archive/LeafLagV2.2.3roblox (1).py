import tkinter as tk
import subprocess
import ctypes
import atexit
import keyboard
import psutil
import threading

class LagSwitchApp:
    def __init__(self):
        self.settings = {"Keybind": "`", "Lagswitch": "off"}
        self.root = tk.Tk()
        self.setup_ui()
        self.check_requirements()
        self.setup_keybind()
        self.active_timer = None
        self.last_toggle_time = 0

    def setup_ui(self):
        self.root.title("Lag")
        self.status_label = tk.Label(self.root, text="LagSwitch off.", fg="red")
        self.status_label.grid(row=1, column=0)
        self.keybind_label = tk.Label(self.root, text=f"Keybind: {self.settings['Keybind']}")
        self.keybind_label.grid(row=2, column=0)
        self.change_button = tk.Button(self.root, text="Change Keybind", command=self.change_keybind)
        self.change_button.grid(row=3, column=0)
        self.always_on_top_var = tk.BooleanVar(value=True)
        self.always_on_top_checkbox = tk.Checkbutton(self.root, text="Always on Top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        self.always_on_top_checkbox.grid(row=3, column=2)
        self.label = tk.Label(text="Made by Squaresz")
        self.label.grid(row=1, column=2)
        self.label_version = tk.Label(text="Version 2.2.3")
        self.label_version.grid(row=2, column=2)
        self.root.geometry("200x70")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", 1)

    def check_requirements(self):
        try:
            if not self.is_admin():
                self.show_message("Please run the program as an administrator.")
                self.disable_lag_switch()
                return

            roblox_running = any(proc.name() == 'RobloxPlayerBeta.exe' for proc in psutil.process_iter())
        except psutil.NoSuchProcess:
            self.disable_lag_switch()
            return

        if not roblox_running:
            self.show_message("Roblox not detected.")
            self.disable_lag_switch()

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            print("Error:", e)
            return False

    def show_message(self, message):
        ctypes.windll.user32.MessageBoxW(0, message, "Leaf", 0)

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
            if self.active_timer:
                self.active_timer.cancel()

            if self.block_flag:
                self.turn_off_lag_switch()
            else:
                self.block_flag = True
                self.update_firewall_rules("block")
                self.update_status_label()
                self.active_timer = threading.Timer(ACTIVE_TIMER_DURATION, self.turn_off_lag_switch)
                self.active_timer.start()

    def turn_off_lag_switch(self):
        self.block_flag = False
        self.update_firewall_rules("delete")
        self.update_status_label()

    def update_status_label(self):
        status_text = "LagSwitch on." if self.block_flag else "LagSwitch off."
        color = "green" if self.block_flag else "red"
        self.status_label.config(text=status_text, fg=color)

    def update_firewall_rules(self, action):
        try:
            process = next((proc for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'] == 'RobloxPlayerBeta.exe'), None)
            if process:
                path = process.exe()
                command = ["netsh", "advfirewall", "firewall"]
                command += ["add", "rule", "name=Roblox_Block", "dir=out", "action=block", f"program={path}"] if action == "block" else ["delete", "rule", "name=Roblox_Block"]
                subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            print("Error updating firewall rules:", e)

    def setup_keybind(self):
        keyboard.on_press_key(self.settings["Keybind"], self.toggle_block)

    def run(self):
        atexit.register(self.exit_handler)
        self.root.mainloop()

    def exit_handler(self):
        self.update_firewall_rules("delete")

    def disable_lag_switch(self):
        rules = subprocess.run(["netsh", "advfirewall", "firewall", "show", "rule", "name=all"], capture_output=True, text=True)
        rule_names = [line.split(":")[1].strip() for line in rules.stdout.splitlines() if "Rule Name:" in line]
        for rule_name in rule_names:
            if "Roblox_Block" in rule_name:
                subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}"])
        keyboard.unhook_all()
        self.root.destroy()

ACTIVE_TIMER_DURATION = 9.8

if __name__ == "__main__":
    app = LagSwitchApp()
    app.run()
