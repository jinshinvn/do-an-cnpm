import hashlib
import json
import threading
import time
import tkinter as Tk
from tkinter import Button, Entry, Label
from tkinter import PhotoImage
from tkinter import messagebox
from model import Model
from view import View


class Controller():
    def popUpWrongCredentialsLogin(self):
        time.sleep(2)
        try:
            self.login.labelImgNotify.place_forget()
        except Exception:
            print('Đã pop up exception và catch lỗi.')
        return

    def th_popUpWrongCredentialsLogin(self):
        thread = threading.Thread(target=self.popUpWrongCredentialsLogin)
        thread.start()

    def getUsernameAndLogin(self, event):
        username = self.login.entryLogin.get() 
        password = self.login.entryPassword.get()
        passwordHashed = hashlib.sha256(password.encode()).hexdigest()
        with open('./json/userData.json', encoding='utf8') as userDataJsonFile:
            tempDict = json.load(userDataJsonFile)
        if (tempDict.get(username) == passwordHashed):
            # messagebox.showwarning(title=None, message = 'Login thành công. Tắt thông báo để hiển thị bảng điều khiển')
            # time.sleep(1)
            self.login.destroy()
            self.__renderDash__()
        else:
            self.login.labelImgNotify.place(x=725, y=2.5)
            self.th_popUpWrongCredentialsLogin()

    def __init__(self):
        self.login = Tk.Tk()
        self.model = Model()
        # nạp login frame & Controller instance vào View()
        self.view = View(self.login, self, "login" )
        self.login.mainloop()
        # self.dshbrd = Tk.Tk()
        # self.view = View(self.dshbrd, self, "dash")
        # self.dshbrd.mainloop()
    
    def __renderDash__(self):
        self.dshbrd = Tk.Tk()
        self.view = View(self.dshbrd, self, "dash")
        self.dshbrd.mainloop()




    # def add10(self, event):
    #     self.action(10)

    # def add100(self, event):
    #     self.action(100)

    # def action(self, addnum):
    #     num_input = self.view.viewPanel.v_entry.get()
    #     try:
    #         result = self.model.addnum(int(num_input), int(addnum))
    #     except ValueError:
    #         result = '¯\_(ツ)_/¯'
    #     self.view.viewPanel.v_num.set(result)