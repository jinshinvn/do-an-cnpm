import json
import sqlite3
import tkinter as Tk

import re
from datetime import date, datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import to_rgba_array
from model import Model
from tkcalendar import Calendar
from tkinter import Toplevel, ttk
from tkinter import Button, Checkbutton, IntVar, Label, messagebox, PhotoImage, Radiobutton, StringVar, Text
from tksheet import Sheet
from PIL import Image, ImageTk
import matplotlib.figure
import matplotlib.patches
from operator import itemgetter
from fpdf import FPDF

tabSel = [True, False, False, False, False, False, False]
dataPhieuThue = []

class View():
    def __init__(self, master, controller, passStr):
        self.controller = controller
        # self.frame = Tk.Frame(master)
        # self.frame.pack()
        if (passStr == "login"):
            self.viewPanel = ViewLogin(master, controller)
        elif (passStr == "dash"):
            self.viewPanel = ViewDash(master, controller)


class ViewLogin():
    width = 1024
    height = 576
    xaxis = 150
    yaxis = 75
    emailPassEntryWidth = 30
    emailPassEntryHeight = 35
    def __init__(self, root, controller):
        self.controller = controller

        # frame 1
        self.controller.login.title("Đăng nhập cùng chúng tôi")
        self.controller.login.iconbitmap('login.ico')
        self.controller.login.configure(bg='white')
        temp = str(self.width) + 'x' + str(self.height) + '+' + str(self.xaxis) + '+' +  str(self.yaxis)
        self.controller.login.geometry(temp)

        global imgIllus
        # garbage collector Python 
        # https://stackoverflow.com/questions/26964091/pil-image-for-tkinter-doesnt-render-unless-photoimage-variable-is-global
        imgIllus = Tk.PhotoImage(file = './img/undraw1.png')
        self.controller.login.labelIllus = Tk.Label(self.controller.login, image = imgIllus, bg='white')
        self.controller.login.labelIllus.place(x=100, y=100)

        self.controller.login.labelTitle = Tk.Label(
            self.controller.login, 
            text = "ĐĂNG NHẬP", 
            font= ('Times New Roman', 24), 
            foreground= "blue3",
            bg='white'
        )
        self.controller.login.labelTitle.place(x=675, y=90)

        self.controller.login.labelLogin = Tk.Label(
            self.controller.login, 
            text = "Email: ", 
            font= ('Times New Roman', 14), 
            foreground= "black",
            bg = 'white'
        )
        self.controller.login.labelLogin.place(x=625, y=150)

        self.controller.login.entryLogin = Tk.Entry(
            self.controller.login, 
            borderwidth=2,
            font= ('Times New Roman', 14), 
            width=self.emailPassEntryWidth,

        )
        self.controller.login.entryLogin.place(x=625, y=200, height=self.emailPassEntryHeight)

        self.controller.login.labelPassword = Tk.Label(
            self.controller.login, 
            text = "Mật khẩu: ", 
            font= ('Times New Roman', 14),
            foreground= "black",
            bg = 'white'
        )
        self.controller.login.labelPassword.place(x=625, y=250)

        self.controller.login.entryPassword = Tk.Entry(
            self.controller.login, 
            show = '*', 
            borderwidth=2,
            font= ('Times New Roman', 14), 
            width=self.emailPassEntryWidth
        )
        self.controller.login.entryPassword.place(x=625, y=300, height=self.emailPassEntryHeight)

        global imgLoginBut        
        imgLoginBut = Tk.PhotoImage(file = './img/login.png')
        self.controller.login.labelLoginBut = Tk.Label(self.controller.login, image = imgLoginBut, bg='white')
        self.controller.login.labelLoginBut.bind('<Button-1>', self.controller.getUsernameAndLogin)
        self.controller.login.bindedBut = Tk.Button(self.controller.login, image=imgLoginBut, command=self.controller.getUsernameAndLogin)
        self.controller.login.labelLoginBut.place(x=665, y=370)

        global imgWrongPass
        imgWrongPass = Tk.PhotoImage(file = './img/vnwronglogin.png')
        self.controller.login.labelImgNotify = Tk.Label(self.controller.login, image = imgWrongPass, bg='white')

        # self.framePanel = Tk.Frame(root)
        # self.framePanel.pack()

        # self.label = Tk.Label(self.framePanel, text="Enter integer, click to add num")
        # self.label.pack()

        # self.v_num = Tk.StringVar()
        # self.num = Tk.Label(self.framePanel, textvariable=self.v_num)
        # self.num.pack()

        # self.v_entry = Tk.StringVar()
        # self.entry = Tk.Entry(self.framePanel, textvariable=self.v_entry)
        # self.entry.pack()

        # frame 2
        # self.framePanel2 = Tk.Frame(root)
        # self.framePanel2.pack()

        # self.btn = Tk.Button(self.framePanel2, text="10")
        # self.btn.pack(side='left')
        # self.btn.bind("<Button>", controller.add10)

        # self.btn2 = Tk.Button(self.framePanel2, text="100")
        # self.btn2.pack(side='left')
        # self.btn2.bind("<Button>", controller.add100)