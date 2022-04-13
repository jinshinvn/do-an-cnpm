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

class ViewDash():
    chungTaDangODau = 'phieuThue'
    appWidth = 1200
    appHeight = 768
    navWidth = appWidth//4
    cfg_clr = 'white'
    tblWidth = 825
    tblHeight = 425
    def __init__(self, root, controller):
        self.controller = controller
        self.controller.dshbrd.title("Dashboard")
        self.controller.dshbrd.iconbitmap('login.ico')
        self.controller.dshbrd.configure(bg='white')
        temp = str(self.appWidth) + 'x' + str(self.appHeight) + '+' + str(60) + '+' + str(0)
        self.controller.dshbrd.geometry(temp)
        self.controller.dshbrd.resizable(False, False)

        a = [i for i in range(200, 1200, 60)]
        b = [i-10 for i in range(260, 1200, 60)]

        model = Model()
        # model.init_db()
        model.fetch_db()

        global dataPhieuThue
        dataPhieuThue = model.getDataPhieuThue()
        global dataNv
        dataNv = model.getDataNv()
        global dataPh 
        dataPh = model.getDataPh()
        global dataDv
        dataDv = model.getDataDv()
        global phieuNhapTbAndFood
        phieuNhapTbAndFood = model.getDataPhieuNhapTbAndFood()
        global dataKh
        dataKh = model.getDataKh()

        self.controller.dshbrd.lftNavDiv = Tk.Canvas(
            self.controller.dshbrd,
            width = self.navWidth,
            height = self.appHeight,
            background = 'white'
        )
        self.controller.dshbrd.lftNavDiv.place(x=0, y=0)
        
        LblPlacing = [30]
        for i in range(1,8):
            LblPlacing.append(LblPlacing[i-1]+50)
        
        def genIco1():
            global icoimg1
            rawIcoImg = Image.open('./img/formIcon.png')
            rawIcoImg = rawIcoImg.resize((25, 25), Image.Resampling.LANCZOS)
            icoimg1 = ImageTk.PhotoImage(rawIcoImg)
            self.controller.dshbrd.lblIcoImg1 = Tk.Label(image = icoimg1, bg = self.cfg_clr, cursor = 'hand2')
            self.controller.dshbrd.lblIcoImg1.place(x = 90, y = a[0]+10)
            return
        def genIco2():
            global icoimg2
            rawIcoImg = Image.open('./img/formIcon.png')
            rawIcoImg = rawIcoImg.resize((25, 25), Image.Resampling.LANCZOS)
            icoimg2 = ImageTk.PhotoImage(rawIcoImg)
            self.controller.dshbrd.lblIcoImg2 = Tk.Label(image = icoimg2, bg = self.cfg_clr, cursor = 'hand2')
            self.controller.dshbrd.lblIcoImg2.place(x = 90, y = a[1]+10)
            return
        def genIco3():
            global icoimg3
            rawIcoImg = Image.open('./img/ban.png')
            rawIcoImg = rawIcoImg.resize((25, 25), Image.Resampling.LANCZOS)
            icoimg3 = ImageTk.PhotoImage(rawIcoImg)
            self.controller.dshbrd.lblIcoImg3 = Tk.Label(image = icoimg3, bg = self.cfg_clr, cursor = 'hand2')
            self.controller.dshbrd.lblIcoImg3.place(x = 90, y = a[2]+10)
            return
        def genIco4():
            global icoimg4
            rawIcoImg = Image.open('./img/nhanvien.png')
            rawIcoImg = rawIcoImg.resize((25, 25), Image.Resampling.LANCZOS)
            icoimg4 = ImageTk.PhotoImage(rawIcoImg)
            self.controller.dshbrd.lblIcoImg4 = Tk.Label(image = icoimg4, bg = self.cfg_clr, cursor = 'hand2')
            self.controller.dshbrd.lblIcoImg4.place(x = 90, y = a[3]+10)
            return
        def genIco5():
            global icoimg5
            rawIcoImg = Image.open('./img/khachhang.png')
            rawIcoImg = rawIcoImg.resize((25, 25), Image.Resampling.LANCZOS)
            icoimg5 = ImageTk.PhotoImage(rawIcoImg)
            self.controller.dshbrd.lblIcoImg5 = Tk.Label(image = icoimg5, bg = self.cfg_clr, cursor = 'hand2')
            self.controller.dshbrd.lblIcoImg5.place(x = 90, y = a[4]+10)
            return
        def genIco6():
            global icoimg6
            rawIcoImg = Image.open('./img/giuxe.png')
            rawIcoImg = rawIcoImg.resize((25, 25), Image.Resampling.LANCZOS)
            icoimg6 = ImageTk.PhotoImage(rawIcoImg)
            self.controller.dshbrd.lblIcoImg6 = Tk.Label(image = icoimg6, bg = self.cfg_clr, cursor = 'hand2')
            self.controller.dshbrd.lblIcoImg6.place(x = 90, y = a[5]+10)
            return
        def genIco7():
            global icoimg7
            rawIcoImg = Image.open('./img/douong.png')
            rawIcoImg = rawIcoImg.resize((25, 25), Image.Resampling.LANCZOS)
            icoimg7 = ImageTk.PhotoImage(rawIcoImg)
            self.controller.dshbrd.lblIcoImg7 = Tk.Label(image = icoimg7, bg = self.cfg_clr, cursor = 'hand2')
            self.controller.dshbrd.lblIcoImg7.place(x = 90, y = a[6]+10)
            return
        def genIco8():
            global icoimg8
            rawIcoImg = Image.open('./img/thongke.png')
            rawIcoImg = rawIcoImg.resize((25, 25), Image.Resampling.LANCZOS)
            icoimg8 = ImageTk.PhotoImage(rawIcoImg)
            self.controller.dshbrd.lblIcoImg8 = Tk.Label(image = icoimg8, bg = self.cfg_clr, cursor = 'hand2')
            self.controller.dshbrd.lblIcoImg8.place(x = 90, y = a[7]+10)
            return

        
        def genBut1(x, y, filename):
            global icoBut1
            rawIcoBut1 = Image.open('./img/'+filename)
            rawIcoBut1 = rawIcoBut1.resize((x, y), Image.Resampling.LANCZOS)
            icoBut1 = ImageTk.PhotoImage(rawIcoBut1)
            global lblIcoBut1
            self.controller.dshbrd.lblIcoBut1 = Tk.Label(self.controller.dshbrd, image = icoBut1, bg = self.cfg_clr)
        genBut1(200, 60, 'but.png')
        def genBut2(x, y):
            global icoBut2
            rawIcoBut2 = Image.open('./img/but.png')
            rawIcoBut2 = rawIcoBut2.resize((x, y), Image.Resampling.LANCZOS)
            icoBut2 = ImageTk.PhotoImage(rawIcoBut2)
            global lblIcoBut2
            self.controller.dshbrd.lblIcoBut2 = Tk.Label(self.controller.dshbrd, image = icoBut2, bg = self.cfg_clr)
            return
        genBut2(200, 60)
        def genBut3(x, y):
            global icoBut3
            rawIcoBut3 = Image.open('./img/but.png')
            rawIcoBut3 = rawIcoBut3.resize((x, y), Image.Resampling.LANCZOS)
            icoBut3 = ImageTk.PhotoImage(rawIcoBut3)
            global lblIcoBut3
            self.controller.dshbrd.lblIcoBut3 = Tk.Label(self.controller.dshbrd, image = icoBut3, bg = self.cfg_clr)
            return
        genBut3(200, 60)
        def genBut4(x, y):
            global icoBut4
            rawIcoBut4 = Image.open('./img/but.png')
            rawIcoBut4 = rawIcoBut4.resize((x, y), Image.Resampling.LANCZOS)
            icoBut4 = ImageTk.PhotoImage(rawIcoBut4)
            global lblIcoBut4
            self.controller.dshbrd.lblIcoBut4 = Tk.Label(self.controller.dshbrd, image = icoBut4, bg = self.cfg_clr)
            return
        genBut4(200, 60)
        def genBut5(x, y):
            global icoBut5
            rawIcoBut5 = Image.open('./img/but.png')
            rawIcoBut5 = rawIcoBut5.resize((x, y), Image.Resampling.LANCZOS)
            icoBut5 = ImageTk.PhotoImage(rawIcoBut5)
            global lblIcoBut5
            self.controller.dshbrd.lblIcoBut5 = Tk.Label(self.controller.dshbrd, image = icoBut5, bg = self.cfg_clr)
            return
        genBut5(200, 60)
        def genBut6(x, y):
            global icoBut6
            rawIcoBut6 = Image.open('./img/but.png')
            rawIcoBut6 = rawIcoBut6.resize((x, y), Image.Resampling.LANCZOS)
            icoBut6 = ImageTk.PhotoImage(rawIcoBut6)
            global lblIcoBut6
            self.controller.dshbrd.lblIcoBut6 = Tk.Label(self.controller.dshbrd, image = icoBut2, bg = self.cfg_clr)
            return
        genBut6(200, 60)
        def genBut7(x, y):
            global icoBut7
            rawIcoBut7 = Image.open('./img/but.png')
            rawIcoBut7 = rawIcoBut7.resize((x, y), Image.Resampling.LANCZOS)
            icoBut7 = ImageTk.PhotoImage(rawIcoBut7)
            global lblIcoBut7
            self.controller.dshbrd.lblIcoBut7 = Tk.Label(self.controller.dshbrd, image = icoBut7, bg = self.cfg_clr)
            return
        genBut7(200, 60)
        def genBut8(x, y):
            global icoBut8
            rawIcoBut8 = Image.open('./img/but.png')
            rawIcoBut8 = rawIcoBut8.resize((x, y), Image.Resampling.LANCZOS)
            icoBut8 = ImageTk.PhotoImage(rawIcoBut8)
            global lblIcoBut8
            self.controller.dshbrd.lblIcoBut8 = Tk.Label(self.controller.dshbrd, image = icoBut8, bg = self.cfg_clr)
            return
        genBut8(200, 60)