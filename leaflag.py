# LeafLagV2.3.1
# this code was optimised using minifier
import subprocess,ctypes,atexit,keyboard,psutil,threading,time,customtkinter as ctk,sys
_T='name'
_S='LagSwitch on.'
_R='RobloxPlayerBeta.exe'
_Q='TkDefaultFont'
_P='Overlay'
_O='block'
_N='-topmost'
_M='AutoTurnBackOn'
_L='rule'
_K='firewall'
_J='advfirewall'
_I='netsh'
_H='delete'
_G='red'
_F='LagSwitch off.'
_E='AutoTurnOff'
_D=None
_C='Keybind'
_B=True
_A=False
class LagSwitchApp:
	def __init__(A):A.settings={_C:'`','Lagswitch':'off',_E:_A,_M:_A,_P:_A};A.block_flag=_A;A.manual_override=_A;A.timer_duration=9.8;A.timer1_duration=.2;A.closed=_A;A.active_timer=_D;A.status_window=_D;A.in_reactivation_period=_A;ctk.set_appearance_mode('dark');ctk.set_default_color_theme('blue');A.root=ctk.CTk();A.root.title('Leaf Lag V2.3.1');A.root.geometry('370x185');A.root.resizable(_A,_A);A.root.attributes(_N,_B);A.check_requirements();A.setup_ui();A.setup_keybind()
	def setup_ui(A):A.status_label=ctk.CTkLabel(A.root,text=_F,text_color=_G,font=(_Q,15,'bold'));A.status_label.grid(row=0,column=0,padx=10,pady=0);ctk.CTkLabel(A.root,text='Made By Squaresz').grid(row=0,column=1,padx=0,pady=0);A.keybind_label=ctk.CTkLabel(A.root,text=f"Keybind: {A.settings[_C]}");A.keybind_label.grid(row=1,column=0,padx=10,pady=0);ctk.CTkButton(A.root,text='Change Keybind',command=A.change_keybind).grid(row=2,column=0,padx=10,pady=5);A.auto_turnoff_var=ctk.BooleanVar(value=_A);ctk.CTkCheckBox(A.root,text='Anti-Timeout',variable=A.auto_turnoff_var,command=A.update_auto_turnoff).grid(row=3,column=0,padx=10,pady=5);A.auto_turnbackon_var=ctk.BooleanVar(value=_A);ctk.CTkCheckBox(A.root,text='Reactivate',variable=A.auto_turnbackon_var,command=A.update_auto_turnbackon).grid(row=4,column=0,padx=10,pady=5);A.always_on_top_var=ctk.BooleanVar(value=_B);ctk.CTkCheckBox(A.root,text='Always on Top',variable=A.always_on_top_var,command=A.toggle_always_on_top).grid(row=2,column=1,padx=10,pady=5);A.timer_slider=ctk.CTkSlider(A.root,from_=0,to=9.8,number_of_steps=98,command=A.update_timer_duration);A.timer_slider.set(A.timer_duration);A.timer_slider.grid(row=3,column=1,padx=0,pady=5);A.timer_label=ctk.CTkLabel(A.root,text=f"{A.timer_duration:.1f}s");A.timer_label.grid(row=3,column=1,padx=0,pady=5);A.timer1_slider=ctk.CTkSlider(A.root,from_=0,to=1,number_of_steps=10,command=A.update_timer1_duration);A.timer1_slider.set(A.timer1_duration);A.timer1_slider.grid(row=4,column=1,padx=0,pady=5);A.timer1_label=ctk.CTkLabel(A.root,text=f"{A.timer1_duration:.1f}s");A.timer1_label.grid(row=4,column=1,padx=0,pady=5);A.overlay_var=ctk.BooleanVar(value=_A);ctk.CTkCheckBox(A.root,text=_P,variable=A.overlay_var,command=A.toggle_status_window).grid(row=1,column=1,padx=10,pady=5)
	def toggle_status_window(A):
		if A.overlay_var.get():A.open_status_window()
		else:A.close_status_window()
	def open_status_window(A):A.status_window=ctk.CTkToplevel(A.root);A.status_window.attributes(_N,_B);A.status_window.attributes('-fullscreen',_B);A.status_window.attributes('-transparentcolor',A.status_window['bg']);A.status_window_label=ctk.CTkLabel(A.status_window,text=_F,text_color=_G,font=(_Q,15,'bold'));A.status_window_label.place(relx=.5,rely=.5,anchor='center',y=80);A.update_status_window()
	def close_status_window(A):
		if A.status_window is not _D and A.status_window.winfo_exists():A.status_window.destroy()
	def update_auto_turnoff(A):A.settings[_E]=A.auto_turnoff_var.get()
	def update_auto_turnbackon(A):A.settings[_M]=A.auto_turnbackon_var.get()
	def update_timer_duration(A,value):A.timer_duration=float(value);A.timer_label.configure(text=f"{A.timer_duration:.1f}s")
	def update_timer1_duration(A,value):A.timer1_duration=float(value);A.timer1_label.configure(text=f"{A.timer1_duration:.1f}s")
	def check_requirements(A):
		if not A.is_admin():A.show_message('Please run the program as an administrator.');sys.exit()
		if not any(A.name()==_R for A in psutil.process_iter([_T])):A.show_message('Roblox not detected.');sys.exit()
	def is_admin(B):
		try:return ctypes.windll.shell32.IsUserAnAdmin()
		except Exception as A:print(f"Error checking admin status: {A}");return _A
	def show_message(A,message):ctypes.windll.user32.MessageBoxW(0,message,'Leaf',0)
	def toggle_always_on_top(A):A.root.attributes(_N,A.always_on_top_var.get())
	def change_keybind(A):A.keybind_label.configure(text='Press a key...');keyboard.on_press(callback=A.set_keybind)
	def set_keybind(A,event):B=event.name;A.settings[_C]=B;A.keybind_label.configure(text=f"Keybind: {B}");keyboard.unhook_all();keyboard.on_press_key(A.settings[_C],A.toggle_block)
	def toggle_block(A,event):
		if event.name==A.settings[_C]:
			if A.in_reactivation_period:
				if A.active_timer:A.active_timer.cancel()
				A.manual_override=_B;A.in_reactivation_period=_A;A.turn_off_lag_switch();return
			if A.block_flag:A.manual_override=_B;A.turn_off_lag_switch()
			else:
				A.manual_override=_A;A.block_flag=_B;A.update_firewall_rules(_O);A.update_status_label()
				if A.active_timer:A.active_timer.cancel()
				if A.settings[_E]:A.active_timer=threading.Timer(A.timer_duration,A.toggle_lag_switch);A.active_timer.start()
	def toggle_lag_switch(A):
		if A.manual_override or A.closed:return
		A.turn_off_lag_switch()
		if A.settings[_M]:
			A.in_reactivation_period=_B;time.sleep(A.timer1_duration);A.in_reactivation_period=_A
			if not A.manual_override:
				A.turn_on_lag_switch()
				if A.settings[_E]:A.active_timer=threading.Timer(A.timer_duration,A.toggle_lag_switch);A.active_timer.start()
	def turn_off_lag_switch(A):
		A.block_flag=_A;A.update_firewall_rules(_H);A.update_status_label()
		if A.active_timer:A.active_timer.cancel();A.active_timer=_D
	def turn_on_lag_switch(A):A.block_flag=_B;A.update_firewall_rules(_O);A.update_status_label()
	def update_status_label(A):
		B=_S if A.block_flag else _F;C='green'if A.block_flag else _G;A.status_label.configure(text=B,text_color=C)
		if hasattr(A,'status_window_label'):A.update_status_window()
	def update_status_window(A):B=_S if A.block_flag else _F;C='green'if A.block_flag else _G;A.status_window_label.configure(text=B,text_color=C)
	def update_firewall_rules(A,action):
		B='name=Roblox_Block'
		try:
			C=next((A for A in psutil.process_iter(['pid',_T])if A.info[_T]==_R),None)
			if not C:A.disable_lag_switch();return
			D=C.exe()
			if action==_O:E=f"program={D}";F=[_I,_J,_K,'add',_L,B,'dir=out','action=block',E];subprocess.run(F,creationflags=subprocess.CREATE_NO_WINDOW)
			else:G=[_I,_J,_K,_H,_L,B];subprocess.run(G,creationflags=subprocess.CREATE_NO_WINDOW)
		except psutil.NoSuchProcess:A.disable_lag_switch()
	def setup_keybind(A):keyboard.on_press_key(A.settings[_C],A.toggle_block)
	def run(A):atexit.register(A.exit_handler);A.root.mainloop()
	def exit_handler(A):A.update_firewall_rules(_H);print('LagSwitch disabled');A.closed=_B
	def disable_lag_switch(A):
		C=subprocess.run([_I,_J,_K,'show',_L,'name=all'],capture_output=True,text=True);D=[A.split(':')[1].strip()for A in C.stdout.splitlines()if'Rule Name:'in A]
		for B in D:
			if'Roblox_Block'in B:subprocess.run([_I,_J,_K,_H,_L,f"name={B}"])
		keyboard.unhook_all();A.closed=_B;A.root.destroy()
if __name__=='__main__':app=LagSwitchApp();app.run()
