import tkinter as tk
from tkinter import ttk
import tkinter.font
import pywinstyles, sys
import sv_ttk # Sun Valley ttk theme
import darkdetect # Dark Mode detection

def center_the_window(win):
    win.update_idletasks()
        
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry(f'{width}x{height}+{x}+{y}')
    win.deiconify()

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.is_it_full_screen = 0
        self.default_font = tk.font.Font(family="Iosevka Term", size=14, weight="normal")
        self.root.attributes('-alpha', 0.0) # Making window invisible
        self.root.title("Typing Tester")
        
        #    pywinstyles.apply_style(self.root, "acrylic") # Theme 
        print(f"Theme: {darkdetect.theme()}")
        sv_ttk.set_theme(darkdetect.theme())
        self.welcome_page()
        self.root.attributes('-alpha', 1.0) # Making window visiable
        
        self.root.mainloop()
                
    def welcome_page(self):
        frm = tk.Frame(self.root)
        frm.grid(column=0, row=0, sticky="NEWS")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frm.columnconfigure(0, weight=1)
        frm.rowconfigure(0, weight=1)
        frm.rowconfigure(1, weight=1)
        
        title = tk.Label(frm, text='Typing Tester', bd=4, font=("Iosevka Term", 25), fg='green')
        title.grid(column=0, row=0, sticky="S")
        explaination = tk.Label(frm, text='Press Any Button to Start', bd=4, font=("Iosevka Term", 20))
        explaination.grid(column=0, row=1, sticky="N")
        full_screen = tk.Label(frm, text='Press ESC to make it full screen', bd=4, font=self.default_font)
        full_screen.grid(column=0, row=0, sticky="WN")
        self.root.geometry("1000x600")
        
        center_the_window(self.root)
        
        self.root.bind("<Escape>", self.make_full_screen)
        
    def make_full_screen(self, event):
        if event.keysym == "Escape" and self.is_it_full_screen == 0:
            self.root.attributes("-fullscreen", True)
            self.is_it_full_screen = 1
        elif event.keysym =="Escape" and self.is_it_full_screen == 1:
            self.root.attributes("-fullscreen", False)
            self.is_it_full_screen = 0
        else:
            print(f"Something went wrong: keysym{event.keysym}, is_it_full_screen = {self.is_it_full_screen}")
        

if __name__ == '__main__': # Only runs if this file is executed directly.
    MyGUI = GUI()
    