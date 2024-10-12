import os
import keyboard
import tkinter as tk
import ctypes
import atexit

settings = {"Keybind": "`", "Lagswitch": "off", "Whitelisted_Apps": set(), "Select_All": False}

print("DO NOT CLOSE THIS CONSOLE WINDOW WHEN LAG SWITCH IS ON")

def toggle_lagswitch():
    settings["Lagswitch"] = "on" if settings["Lagswitch"] == "off" else "off"
    status_label.config(text=f"Lagswitch turned {'on' if settings['Lagswitch'] == 'on' else 'off'}.")

def change_keybind():
    keybind_label.config(text="Press a key...")
    keyboard.on_press(callback=set_keybind)

def set_keybind(event):
    new_keybind = event.name
    settings["Keybind"] = new_keybind
    keybind_label.config(text=f"Keybind: {new_keybind}")
    keyboard.unhook_all()
    keyboard.on_press_key(settings["Keybind"], toggle_block)

def toggle_block(event):
    if event.name == settings["Keybind"]:
        global block_flag
        block_flag = not block_flag
        if block_flag:
            if settings["Select_All"]:
                unblock_all_apps()
            else:
                unblock_apps(settings["Whitelisted_Apps"])
            status_text = "LagSwitch off."
        else:
            if settings["Select_All"]:
                block_all_apps()
            else:
                block_apps(settings["Whitelisted_Apps"])
            status_text = "LagSwitch on."
        status_label.config(text=status_text)

def block_all_apps():
    os.system(f'netsh advfirewall firewall add rule name="Block_All" dir=out action=block')

def unblock_all_apps():
    os.system(f'netsh advfirewall firewall delete rule name="Block_All"')

def block_apps(apps):
    for app in apps:
        os.system(f'netsh advfirewall firewall add rule name="Block_{app}" dir=out action=block program="{app}"')

def unblock_apps(apps):
    for app in apps:
        os.system(f'netsh advfirewall firewall delete rule name="Block_{app}"')

def add_app():
    new_app = app_entry.get()
    if new_app:
        if not (new_app.startswith('"') and new_app.endswith('"')):
            new_app = f'"{new_app}"'
        if new_app not in settings["Whitelisted_Apps"]:
            settings["Whitelisted_Apps"].add(new_app)
            whitelist_box.insert(tk.END, new_app)
        else:
            ctypes.windll.user32.MessageBoxW(0, f"{new_app} is already in the whitelist.", "Duplicate Entry", 0)
        app_entry.delete(0, tk.END)

def remove_app():
    selected_index = whitelist_box.curselection()
    if selected_index:
        app_to_remove = whitelist_box.get(selected_index)
        settings["Whitelisted_Apps"].remove(app_to_remove)
        whitelist_box.delete(selected_index)

def toggle_select_all():
    settings["Select_All"] = select_all_var.get()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def exit_handler():
    unblock_all_apps()

block_flag = settings["Lagswitch"] == "off"

if not is_admin():
    root = tk.Tk()
    root.withdraw()
    ctypes.windll.user32.MessageBoxW(0, "Please run the program as an administrator.", "Administrator Privileges Required", 0)
    root.destroy()
    exit()

keyboard.on_press_key(settings["Keybind"], toggle_block)
atexit.register(exit_handler)

root = tk.Tk()
root.title("Leaf Switch V2.2.1")
root.wm_attributes("-topmost", 1)

def toggle_always_on_top():
    root.attributes("-topmost", always_on_top_var.get())

always_on_top_var = tk.BooleanVar()
always_on_top_var.set(True)  

always_on_top_checkbox = tk.Checkbutton(root, text="Always on Top", variable=always_on_top_var, command=toggle_always_on_top)
always_on_top_checkbox.grid(row=9, column=3, columnspan=15)

status_label = tk.Label(root, text="LagSwitch off.")
status_label.grid(row=1, column=0, columnspan=2)

keybind_label = tk.Label(root, text=f"Keybind: {settings['Keybind']}")
keybind_label.grid(row=2, column=0, columnspan=2)

change_button = tk.Button(root, text="Change Keybind", command=change_keybind)
change_button.grid(row=3, column=0, columnspan=2)

add_app_label = tk.Label(root, text="Add Whitelisted App:")
add_app_label.grid(row=5, column=0, columnspan=2)

app_entry = tk.Entry(root)
app_entry.grid(row=6, column=0, columnspan=2)

add_button = tk.Button(root, text="Add", command=add_app)
add_button.grid(row=7, column=0, columnspan=2)

remove_button = tk.Button(root, text="Remove Selected", command=remove_app)
remove_button.grid(row=8, column=0, columnspan=2)

whitelist_label = tk.Label(root, text="")
whitelist_label.grid(row=0, column=2, rowspan=9)

whitelist_box = tk.Listbox(root)
whitelist_box.grid(row=1, column=3, rowspan=8)

for app in settings["Whitelisted_Apps"]:
    whitelist_box.insert(tk.END, app)

select_all_var = tk.BooleanVar()
select_all_checkbox = tk.Checkbutton(root, text="No Whitelist", variable=select_all_var, command=toggle_select_all)
select_all_checkbox.grid(row=9, column=0, columnspan=2)

root.geometry("255x200")
root.resizable(False, False)

root.mainloop()