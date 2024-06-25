# LeafLagV2.2.5
import tkinter as tk
import subprocess
import ctypes
import atexit
import keyboard
import psutil
import threading
import time
class LagSwitchApp:
    def __init__(self):
        self.settings = {"Keybind": "`", "Lagswitch": "off", "AutoTurnOff": True, "AutoTurnBackOn": False}
        self.block_flag = False
        self.manual_override = False
        self.timer_duration = 9.8
        self.timer1_duration = 9.8
        self.closed = False
        self.active_timer = None

        self.root = tk.Tk()
        self.root.title("Lag")
        self.root.wm_attributes("-topmost", 1)
        self.setup_ui()
        self.check_requirements()
        self.setup_keybind()

    def setup_ui(self):
        self.status_label = tk.Label(self.root, text="LagSwitch off.", fg="red")
        self.status_label.grid(row=1, column=0)
        tk.Label(text="Leaf Lag V2.2.5beta").grid(row=1, column=1)
        self.keybind_label = tk.Label(self.root, text=f"Keybind: {self.settings['Keybind']}")
        self.keybind_label.grid(row=2, column=0)
        tk.Button(self.root, text="Change Keybind", command=self.change_keybind).grid(row=3, column=0)

        self.auto_turnoff_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Anti-Timeout", variable=self.auto_turnoff_var, command=self.update_auto_turnoff).grid(row=4, column=0)

        self.auto_turnbackon_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.root, text="Reactivate", variable=self.auto_turnbackon_var, command=self.update_auto_turnbackon).grid(row=5, column=0)

        self.always_on_top_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Always on Top", variable=self.always_on_top_var, command=self.toggle_always_on_top).grid(row=3, column=1)

        tk.Label(self.root).grid(row=6, column=0)
        self.timer_slider = tk.Scale(self.root, from_=0, to=9.8, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_timer_duration)
        self.timer_slider.set(self.timer_duration)
        self.timer_slider.grid(row=4, column=1)

        self.timer1_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_timer1_duration)
        self.timer1_slider.grid(row=5, column=1)

        tk.Label(text="Made by Squaresz").grid(row=2, column=1)

        self.root.geometry("210x150")
        self.root.resizable(False, False)

    def update_auto_turnoff(self):
        self.settings["AutoTurnOff"] = self.auto_turnoff_var.get()

    def update_auto_turnbackon(self):
        self.settings["AutoTurnBackOn"] = self.auto_turnbackon_var.get()

    def update_timer_duration(self, value):
        self.timer_duration = float(value)

    def update_timer1_duration(self, value):
        self.timer1_duration = float(value)

    def check_requirements(self):
        if not self.is_admin():
            self.show_message("Please run the program as an administrator.")
            self.disable_lag_switch()
            return

        roblox_running = any(proc.name() == 'RobloxPlayerBeta.exe' for proc in psutil.process_iter())
        if not roblox_running:
            self.show_message("Roblox not detected.")
            self.disable_lag_switch()

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            print(f"Error checking admin status: {e}")
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
            if self.block_flag:
                self.manual_override = True
                self.turn_off_lag_switch()
            else:
                self.manual_override = False
                self.block_flag = True
                self.update_firewall_rules("block")
                self.update_status_label()

                if self.active_timer:
                    self.active_timer.cancel()

                if self.settings["AutoTurnOff"]:
                    self.active_timer = threading.Timer(self.timer_duration, self.toggle_lag_switch)
                    self.active_timer.start()

    def toggle_lag_switch(self):
        if self.manual_override or self.closed:
            return
        self.turn_off_lag_switch()
        if self.settings["AutoTurnBackOn"]:
            time.sleep(self.timer1_duration)
            self.turn_on_lag_switch()
            if self.settings["AutoTurnOff"]:
                self.active_timer = threading.Timer(self.timer_duration, self.toggle_lag_switch)
                self.active_timer.start()

    def turn_off_lag_switch(self):
        self.block_flag = False
        self.update_firewall_rules("delete")
        self.update_status_label()
        if self.active_timer:
            self.active_timer.cancel()
            self.active_timer = None

    def turn_on_lag_switch(self):
        self.block_flag = True
        self.update_firewall_rules("block")
        self.update_status_label()

    def update_status_label(self):
        status_text = "LagSwitch on." if self.block_flag else "LagSwitch off."
        color = "green" if self.block_flag else "red"
        self.status_label.config(text=status_text, fg=color)

    def update_firewall_rules(self, action):
        if self.closed:
            return
        try:
            process = next((proc for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'] == 'RobloxPlayerBeta.exe'), None)
        except psutil.NoSuchProcess:
            self.disable_lag_switch()
            return

        if process:
            path = process.exe()
            command = ["netsh", "advfirewall", "firewall", "add", "rule", "name=Roblox_Block", "dir=out", "action=block", f"program={path}"] if action == "block" else ["netsh", "advfirewall", "firewall", "delete", "rule", "name=Roblox_Block"]
            subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            self.disable_lag_switch()

    def setup_keybind(self):
        keyboard.on_press_key(self.settings["Keybind"], self.toggle_block)

    def run(self):
        atexit.register(self.exit_handler)
        self.root.mainloop()

    def exit_handler(self):
        self.update_firewall_rules("delete")
        print("LagSwitch disabled")
        self.closed = True

    def disable_lag_switch(self):
        rules = subprocess.run(["netsh", "advfirewall", "firewall", "show", "rule", "name=all"], capture_output=True, text=True)
        rule_names = [line.split(":")[1].strip() for line in rules.stdout.splitlines() if "Rule Name:" in line]
        for rule_name in rule_names:
            if "Roblox_Block" in rule_name:
                subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}"])
        keyboard.unhook_all()
        self.closed = True
        self.root.destroy()

if __name__ == "__main__":
    app = LagSwitchApp()
    app.run()
