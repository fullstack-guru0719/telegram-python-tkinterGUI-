import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import*
from PIL import ImageTk
from register import Register
from botmanagement import BotManagement

class Main:
    def __init__(self):
        self.root = ttk.Window(themename="superhero")
        self.root.title("Telegram Bot")
        self.root.geometry("1000x550+0+0")
        self.root.config(bg="#2b3e50")
        # set background image
        bg= ImageTk.PhotoImage(file="./image/index_bg.jpg")
        bg_lbl= Canvas(self.root,width= 1000, height= 730)
        bg_lbl.pack(expand=True, fill= BOTH)
        bg_lbl.create_image(0,0,image=bg, anchor="nw")

        button_style = ttk.Style()
        button_style.configure('my.TButton', font=('Helvetica', 12))
        btn_register=ttk.Button(self.root,text="Telegram Register", command=self.fnAutoRegister,cursor="hand2",width= 40, bootstyle='success-outline')
        btn_register.place(x=540,y=300,  height = 50)
        btn_bot=ttk.Button(self.root,text="Telegram Bot Management", command=self.fnBotManage,cursor="hand2",width= 40, bootstyle='success-outline')
        btn_bot.place(x=540,y=370,  height = 50)
        self.root.mainloop()
    def fnAutoRegister(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)


    def fnBotManage(self):
        self.new_window=Toplevel(self.root)
        self.app=BotManagement(self.new_window)


if __name__ == '__main__':
    Main()