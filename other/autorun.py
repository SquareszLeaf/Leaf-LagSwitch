import ctypes
import atexit
import threading
import time
import customtkinter as ctk  # If customtkinter is too large, consider using tkinter
import tkinter as tk

class AutoRunApp:
    def __init__(self):
        self.settings = {
            "Keybind": "`",
            "AutoRun": "off",
            "Overlay": False
        }
        self.block_flag = False
        self.manual_override = False
        self.delay_duration = 0.1
        self.min_delay_duration = 0.029
        self.max_delay_duration = 0.305
        self.closed = False
        self.active_timer = None
        self.status_window = None
        self.spam_thread = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("AutoRun v1.0.3")
        self.root.geometry("370x145")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.setup_ui()
        self.setup_keybind()
        self.setup_delay_adjustment()

    def setup_ui(self):
        self.status_label = ctk.CTkLabel(self.root, text="AutoRun off.", text_color="red", font=("TkDefaultFont", 15, "bold"))
        self.status_label.grid(row=0, column=0, padx=10, pady=0)

        ctk.CTkLabel(self.root, text="Made By Squaresz").grid(row=0, column=1, padx=0, pady=0)
        
        self.keybind_label = ctk.CTkLabel(self.root, text=f"Keybind: {self.settings['Keybind']}")
        self.keybind_label.grid(row=1, column=0, padx=10, pady=0)

        change_keybind_button = ctk.CTkButton(self.root, text="Change Keybind", command=self.change_keybind)
        change_keybind_button.grid(row=2, column=0, padx=10, pady=5)

        self.always_on_top_var = ctk.BooleanVar(value=True)
        always_on_top_checkbox = ctk.CTkCheckBox(self.root, text="Always on Top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        always_on_top_checkbox.grid(row=2, column=1, padx=10, pady=5)
        self.create_tooltip(always_on_top_checkbox, "Keep this window always on top.")

        self.overlay_var = ctk.BooleanVar(value=False)
        overlay_checkbox = ctk.CTkCheckBox(self.root, text="Overlay", variable=self.overlay_var, command=self.toggle_status_window)
        overlay_checkbox.grid(row=1, column=1, padx=10, pady=5)
        self.create_tooltip(overlay_checkbox, "Toggle the overlay window.")

        self.adjust_delay_var = ctk.BooleanVar(value=False)
        adjust_delay_checkbox = ctk.CTkCheckBox(self.root, text="Delay Adjust", variable=self.adjust_delay_var)
        adjust_delay_checkbox.grid(row=3, column=0, padx=10, pady=5)
        self.create_tooltip(adjust_delay_checkbox, "Enable delay adjustment using 'f' and 'g' keys to change by 5 and 'r' and 't' to change by 1 without having to use slider.")

        self.delay_slider = ctk.CTkSlider(self.root, from_=self.min_delay_duration, to=self.max_delay_duration, number_of_steps=267, command=self.update_delay_duration)
        self.delay_slider.set(self.delay_duration)
        self.delay_slider.grid(row=3, column=1, padx=0, pady=5)
        self.create_tooltip(self.delay_slider, "Adjust spam speed/delay.")

        self.delay_label = ctk.CTkLabel(self.root, text=f"{self.delay_duration:.3f}s")
        self.delay_label.grid(row=3, column=1, padx=0, pady=5, sticky="e")

    def setup_delay_adjustment(self):
        import keyboard  # Imported here to reduce startup impact if it's not needed immediately
        keyboard.on_press_key("f", self.decrease_delay)
        keyboard.on_press_key("g", self.increase_delay)
        keyboard.on_press_key("r", self.decrease_delay1)
        keyboard.on_press_key("t", self.increase_delay1)

    def decrease_delay(self, event):
        if self.adjust_delay_var.get():
            self.delay_duration = max(self.min_delay_duration, self.delay_duration - 0.005)
            self.update_delay_label()

    def increase_delay(self, event):
        if self.adjust_delay_var.get():
            self.delay_duration = min(self.max_delay_duration, self.delay_duration + 0.005)
            self.update_delay_label()

    def decrease_delay1(self, event):
        if self.adjust_delay_var.get():
            self.delay_duration = max(self.min_delay_duration, self.delay_duration - 0.001)
            self.update_delay_label()

    def increase_delay1(self, event):
        if self.adjust_delay_var.get():
            self.delay_duration = min(self.max_delay_duration, self.delay_duration + 0.001)
            self.update_delay_label()

    def update_delay_label(self):
        self.delay_label.configure(text=f"{self.delay_duration:.3f}s")
        self.delay_slider.set(self.delay_duration)
        self.update_status_window()

    def toggle_status_window(self):
        if self.overlay_var.get():
            self.open_status_window()
        else:
            self.close_status_window()

    def open_status_window(self):
        self.status_window = ctk.CTkToplevel(self.root)
        self.status_window.attributes("-topmost", True)
        self.status_window.attributes("-fullscreen", True)
        self.status_window.attributes("-transparentcolor", self.status_window['bg'])
        
        self.status_window_label = ctk.CTkLabel(self.status_window, text="AutoRun off.", text_color="red", font=("TkDefaultFont", 15, "bold"))
        self.status_window_label.place(relx=0.5, rely=0.5, anchor="center", y=80)

        self.delay_window_label = ctk.CTkLabel(self.status_window, text=f"Delay: {self.delay_duration:.3f}s", text_color="white", font=("TkDefaultFont", 15, "bold"))
        self.delay_window_label.place(relx=0.5, rely=0.5, anchor="center", y=100)

        self.update_status_window()

    def close_status_window(self):
        if self.status_window is not None and self.status_window.winfo_exists():
            self.status_window.destroy()

    def update_delay_duration(self, value):
        self.delay_duration = float(value)
        self.delay_label.configure(text=f"{self.delay_duration:.3f}s")
        self.update_status_window()

    def show_message(self, message):
        ctypes.windll.user32.MessageBoxW(0, message, "AutoRun", 0)

    def toggle_always_on_top(self):
        self.root.attributes("-topmost", self.always_on_top_var.get())

    def change_keybind(self):
        self.keybind_label.configure(text="Press a key...")
        import keyboard  # Imported here to reduce startup impact if it's not needed immediately
        keyboard.on_press(callback=self.set_keybind)

    def set_keybind(self, event):
        new_keybind = event.name
        self.settings["Keybind"] = new_keybind
        self.keybind_label.configure(text=f"Keybind: {new_keybind}")
        import keyboard  # Imported here to reduce startup impact if it's not needed immediately
        keyboard.unhook_all()
        keyboard.on_press_key(self.settings["Keybind"], self.toggle_block)
        self.setup_delay_adjustment()

    def toggle_block(self, event):
        if event.name == self.settings["Keybind"]:
            if self.block_flag:
                self.manual_override = True
                self.turn_off_autorun()
            else:
                self.manual_override = False
                self.block_flag = True
                self.update_status_label()
                self.start_spamming_keys()

    def turn_off_autorun(self):
        self.block_flag = False
        self.update_status_label()
        self.stop_spamming_keys()

    def update_status_label(self):
        status_text = "AutoRun on." if self.block_flag else "AutoRun off."
        color = "green" if self.block_flag else "red"
        self.status_label.configure(text=status_text, text_color=color)
        if hasattr(self, 'status_window_label'):
            self.status_window_label.configure(text=status_text, text_color=color)

    def update_status_window(self):
        status_text = "AutoRun on." if self.block_flag else "AutoRun off."
        color = "green" if self.block_flag else "red"
        
        if hasattr(self, 'status_window_label'):
            self.status_window_label.configure(text=status_text, text_color=color)
        if hasattr(self, 'delay_window_label'):
            self.delay_window_label.configure(text=f"Delay: {self.delay_duration:.3f}s")

    def setup_keybind(self):
        import keyboard  # Imported here to reduce startup impact if it's not needed immediately
        keyboard.on_press_key(self.settings["Keybind"], self.toggle_block)

    def run(self):
        atexit.register(self.exit_handler)
        self.root.mainloop()

    def exit_handler(self):
        print("AutoRun disabled")
        self.closed = True

    def start_spamming_keys(self):
        if self.spam_thread and self.spam_thread.is_alive():
            return

        self.spam_thread = threading.Thread(target=self.spam_keys)
        self.spam_thread.start()

    def stop_spamming_keys(self):
        if self.spam_thread and self.spam_thread.is_alive():
            self.spam_thread.do_run = False
            self.spam_thread.join()

    def spam_keys(self):
        t = threading.current_thread()
        while getattr(t, "do_run", True):
            import keyboard  # Imported here to reduce startup impact if it's not needed immediately
            keyboard.press_and_release('q')
            time.sleep(self.delay_duration)
            keyboard.press_and_release('e')
            time.sleep(self.delay_duration)

    def create_tooltip(self, widget, text):
        tooltip = Tooltip(widget, text)

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_attributes("-topmost", True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left', background="#ffffff", relief='solid', borderwidth=1, wraplength=200)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

if __name__ == "__main__":
    app = AutoRunApp()
    app.run()
