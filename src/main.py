import tkinter as tk
from tkinter import ttk
import tkinter.font
import pywinstyles, sys # Window style
import sv_ttk # Sun Valley ttk theme
import darkdetect # Dark Mode detection
import os # Reading the file names
import time

class typing_tester_app(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title("Typing Tester")
        self.attributes('-alpha', 0.0) # Making window invisible
        self.is_it_full_screen = False
        self.default_font = tk.font.Font(family="Iosevka Term", size=25, weight="normal")
        
        # pywinstyles.apply_style(self, "acrylic") # Theme 
        print(f"Theme: {darkdetect.theme()}")
        sv_ttk.set_theme(darkdetect.theme())
        self.theme = darkdetect.theme()
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        
        for F in (WelcomePage, MainPage): # Initiallizing all the pages in the app
            
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
            
        self.geometry("1000x600")
        self.center_the_window()
        
        self.show_frame(WelcomePage)

        self.attributes('-alpha', 1.0) # Making window visiable
        self.bind("<Escape>", self.make_full_screen)

    def show_frame(self, cont): # Display a certain frame to this window
        frame = self.frames[cont]
        frame.tkraise()
        frame.focus_set()
        
    def make_full_screen(self, event): # Make the window into full screen
        if event.keysym == "Escape" and self.is_it_full_screen == False:
            self.attributes("-fullscreen", True)
            self.is_it_full_screen = True
        elif event.keysym =="Escape" and self.is_it_full_screen == True:
            self.attributes("-fullscreen", False)
            self.is_it_full_screen = False
        else:
            print(f"Something went wrong: keysym{event.keysym}, is_it_full_screen = {self.is_it_full_screen}")
        
    def center_the_window(self): # Center the window
            self.update_idletasks()
                
            width = self.winfo_width()
            self_width = self.winfo_rootx() - self.winfo_x()
            win_width = width + 2 * self_width
            height = self.winfo_height()
            titlebar_height = self.winfo_rooty() - self.winfo_y()
            win_height = height + titlebar_height + self_width
            
            x = self.winfo_screenwidth() // 2 - win_width // 2
            y = self.winfo_screenheight() // 2 - win_height // 2
            self.geometry(f'{width}x{height}+{x}+{y}')
            self.deiconify()
               
    def end_app(self, code): # Destroy the main window and exit program, (Return 0 for the successful exit, else is error)
        if code == 0:
            print("Successfully exit the program")
            self.destroy()
            return 0
        else:
            print(f"Exit the program with an error: Error code = {code}")
            self.destroy()
            return 1
        
class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent )
        
        
        self.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        title = tk.Label(self, text='Typing Tester', bd=4, font=controller.default_font, fg='green')
        title.grid(column=0, row=0, sticky="S")
        explaination = tk.Label(self, text='Press Any Button to Start', bd=4, font=controller.default_font)
        explaination.grid(column=0, row=1, sticky="N")
        full_screen = tk.Label(self, text='Press ESC to make it full screen', bd=4, font=("Iosevka Term", 14))
        full_screen.grid(column=0, row=0, sticky="WN")
        
        self.bind("<Key>", lambda event: self.on_key_press(event, controller))

    def on_key_press(self, event, controller):
        if event.keysym != "Escape":   # Ignore Escape (Escape is for full screen)
            print(f"User pressed: {event.char} ({event.keysym})")
            controller.show_frame(MainPage)   # switch page

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.cursor_position = 1
        self.grid(column=0, row=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        
        full_screen = tk.Label(self, text='Press ESC to make it full screen', bd=4, font=("Iosevka Term", 14))
        full_screen.grid(column=0, row=0, sticky="WN")
        
        self.list1 = tk.Label(self, text="Start", bd = 4, font=controller.default_font, fg='black')
        self.list1.grid(column=0, row=1, sticky='N')
        
        self.list2 = tk.Label(self, text="See Record", bd = 4, font=controller.default_font, fg='black')
        self.list2.grid(column=0, row=2, sticky='N')
        
        self.list3 = tk.Label(self, text="Exit", bd = 4, font=controller.default_font, fg='black')
        self.list3.grid(column=0, row=3, sticky='N')
        
        self.update_cursor()
        
        self.bind("<Up>", self.selectUpward)
        self.bind("<Down>", self.selectDownward)
        self.bind("<Return>", lambda event: self.selectOption(event, controller))
                  
    def selectUpward(self, event):
        if self.cursor_position == 1:
            pass
        elif self.cursor_position == 2:
            self.cursor_position = 1
        elif self.cursor_position == 3:
            self.cursor_position = 2
        else:
            print(f"selectUpward: cursor_position is not in the normal range. cursor_position(1-3) = {self.cursor_position}")
        self.update_cursor()
        print("cursor_position = ",self.cursor_position)
        
    def selectDownward(self, event):
        if self.cursor_position == 1:
            self.cursor_position = 2
        elif self.cursor_position == 2:
            self.cursor_position = 3
        elif self.cursor_position == 3:
            pass
        else:
            print(f"selectDownward: cursor_position is not in the normal range. cursor_position(1-3) = {self.cursor_position}")
        self.update_cursor()
        print("cursor_position = ", self.cursor_position)
        
    def selectOption(self, event, controller):
        if self.cursor_position == 1:
            controller.show_frame(TestPage)
        elif self.cursor_position == 2:
            controller.show_frame(RecordPage)
        elif self.cursor_position == 3:
            controller.end_app(0)
        else:
            print(f"selectDownward: cursor_position is not in the normal range. cursor_position(1-3) = {self.cursor_position}")
        
    def update_cursor(self):
        # reset all
        self.list1.config(fg="black")
        self.list2.config(fg="black")
        self.list3.config(fg="black")
        
        #Highlight the selected option
        if self.cursor_position == 1:
            self.list1.config(fg="green")
        elif self.cursor_position == 2:
            self.list2.config(fg="green")
        elif self.cursor_position == 3:
            self.list3.config(fg="green")
    
class TestPage(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Tk.__init__(self, parent)
        
        self.correct_words = 0
        
        self.total_words = 0
        self.total_charecters = 0
        
        self.wrong_words = 0
        self.wrong_characters = 0

        self.time = 0
        self.cpm = 0
        self.wpm = 0
        
    def read_file_name(dir_path): # Reads all the names of the files in a certain directory, Returns a list of the name
        try:
            file_name_list = []
            file_name_list = os.listdir(dir_path)
        except FileNotFoundError:
            print(f"Error: Cannot find any file in {dir_path}")
            return 1
        
        return file_name_list
            
    def read_file_content(file_path): # Reads all the content inside of the file, Returns a list of words in the file, returns 1 when it is failed to extracts words.
        try:
            words_list = []
            f = open(file_path, "rt")
            file = f.read()
            print(f.read())
            # Make the f.read() retuns into a list
            f.close()
            return words_list
            
        except FileNotFoundError:
            print(f"Error: Cannot find any file{file_path} in ")
            f.close()
            return 1
            
    def is_it_correct(self, controller, input, answer):
        if input == answer:
            print("Correct!")
            self.correct_words += 1
        else:
            print("Wrong!")
            self.wrong_words += 1
            input_letters = list(input)
            answer_letters = list(answer)
            
            for i in range(len(answer_letters)):
                if input_letters[i] == answer_letters[i]:
                    controller.correct_characters += 1
                else:
                    controller.wrong_characters += 1
                    
        controller.total_characters += len(list(input))
        controller.total_words += 1
                
    def save_record(self):
                     
#
        tk.Tk.__init__(self, parent)
       
if __name__ == '__main__': # Only runs if this file is executed directly.
    startapp = typing_tester_app()
    startapp.mainloop()