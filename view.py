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

        self.controller.dshbrd.brand = Tk.Label(
            self.controller.dshbrd,
            text = 'SADDAM HUSSEIN',
            font = ('Montserrat', 18),
            foreground = 'black',
            bg = 'white'
        )
        self.controller.dshbrd.brand.place(x=60, y=10)

        def genLogo(x, y):
            global logo
            rawLogo = Image.open('./img/logo.jpg')
            rawLogo = rawLogo.resize((x, y), Image.Resampling.LANCZOS)
            logo = ImageTk.PhotoImage(rawLogo)
            global lblLogo
            self.controller.dshbrd.lblLogo = Tk.Label(self.controller.dshbrd, image = logo, bg = self.cfg_clr)
            return
        genLogo(120, 120)
        self.controller.dshbrd.lblLogo.place(x = 90, y = 60)
        
        def genIco():
            genIco1()
            genIco2()
            genIco3()
            genIco4()
            genIco5()
            genIco6()
            genIco7()
            genIco8()
        genIco()
        
        self.controller.dshbrd.lbl1 = Tk.Label(cursor = 'hand2', text = 'Phiếu đặt',bg = self.cfg_clr,font = ('Chirp', 14))
        self.controller.dshbrd.lbl2 = Tk.Label(cursor = 'hand2', text = 'Hóa đơn',bg = self.cfg_clr,font = ('Chirp', 14))
        self.controller.dshbrd.lbl3 = Tk.Label(cursor = 'hand2', text = 'Bàn',bg = self.cfg_clr,font = ('Chirp', 14))
        self.controller.dshbrd.lbl4 = Tk.Label(cursor = 'hand2', text = 'Nhân viên',bg = self.cfg_clr,font = ('Chirp', 14))
        self.controller.dshbrd.lbl5 = Tk.Label(cursor = 'hand2', text = 'Khách hàng' ,bg = self.cfg_clr,font = ('Chirp', 14))
        self.controller.dshbrd.lbl6 = Tk.Label(cursor = 'hand2', text = 'Giữ xe', bg = self.cfg_clr, font = ('Chirp', 14))
        self.controller.dshbrd.lbl7 = Tk.Label(cursor = 'hand2', text = 'Thức uống',bg = self.cfg_clr,font = ('Chirp', 14))
        self.controller.dshbrd.lbl8 = Tk.Label(cursor = 'hand2', text = 'Thống kê',bg = self.cfg_clr,font = ('Chirp', 14))
        
        def mouEnBut1(e):
            self.controller.dshbrd.lbl1['font'] = ('Chirp', 14, 'bold')
        def mouLeBut1(e):
            self.controller.dshbrd.lbl1['font'] = ('Chirp', 14)
        def mouEnBut2(e):
            self.controller.dshbrd.lbl2['font'] = ('Chirp', 14, 'bold')
        def mouLeBut2(e):
            self.controller.dshbrd.lbl2['font'] = ('Chirp', 14)
        def mouEnBut3(e):
            self.controller.dshbrd.lbl3['font'] = ('Chirp', 14, 'bold')
        def mouLeBut3(e):
            self.controller.dshbrd.lbl3['font'] = ('Chirp', 14)
        def mouEnBut4(e):
            self.controller.dshbrd.lbl4['font'] = ('Chirp', 14, 'bold')
        def mouLeBut4(e):
            self.controller.dshbrd.lbl4['font'] = ('Chirp', 14)
        def mouEnBut5(e):
            self.controller.dshbrd.lbl5['font'] = ('Chirp', 14, 'bold')
        def mouLeBut5(e):
            self.controller.dshbrd.lbl5['font'] = ('Chirp', 14)
        def mouEnBut6(e):
            self.controller.dshbrd.lbl6['font'] = ('Chirp', 14, 'bold')
        def mouLeBut6(e):
            self.controller.dshbrd.lbl6['font'] = ('Chirp', 14)
        def mouEnBut7(e):
            self.controller.dshbrd.lbl7['font'] = ('Chirp', 14, 'bold')
        def mouLeBut7(e):
            self.controller.dshbrd.lbl7['font'] = ('Chirp', 14)
        def mouEnBut8(e):
            self.controller.dshbrd.lbl8['font'] = ('Chirp', 14, 'bold')
        def mouLeBut8(e):
            self.controller.dshbrd.lbl8['font'] = ('Chirp', 14)

        def lblIcoButPlacing():
            self.controller.dshbrd.lblIcoBut1.place(x = 60, y = 195)
            self.controller.dshbrd.lblIcoBut2.place(x = 60, y = 257)
            self.controller.dshbrd.lblIcoBut3.place(x = 60, y = 317)
            self.controller.dshbrd.lblIcoBut4.place(x = 60, y = 377)
            self.controller.dshbrd.lblIcoBut5.place(x = 60, y = 437)
            self.controller.dshbrd.lblIcoBut6.place(x = 60, y = 497)
            self.controller.dshbrd.lblIcoBut7.place(x = 60, y = 557)
            self.controller.dshbrd.lblIcoBut8.place(x = 60, y = 617)
        lblIcoButPlacing()
        
        def lblPlacing():
            self.controller.dshbrd.lbl1.place(x=125, y=a[0]+10)
            self.controller.dshbrd.lbl2.place(x=125, y=a[1]+10)
            self.controller.dshbrd.lbl3.place(x=125, y=a[2]+10)
            self.controller.dshbrd.lbl4.place(x=125, y=a[3]+10)
            self.controller.dshbrd.lbl5.place(x=125, y=a[4]+10)
            self.controller.dshbrd.lbl6.place(x=125, y=a[5]+10)
            self.controller.dshbrd.lbl7.place(x=125, y=a[6]+10)
            self.controller.dshbrd.lbl8.place(x=125, y=a[7]+10)
        lblPlacing()

        
        
        def genRight(s, includeSearch):
            global nvHeader
            nvHeader = ["ID", "Họ", "Tên", "Giới tính", "Năm sinh", "Quê quán", "Chức vụ", "Bộ phận", "Lương", "Thưởng"]

            global khHeader
            khHeader = ['ID', 'Họ', 'Tên', 'Giới tính', 'Năm sinh', 'Loại xe']

            global dvHeader
            dvHeader = ['ID', 'Loại xe', 'Chi phí']
            
            global banHeader
            banHeader = ['ID', 'Cỡ bàn', 'Trạng thái', 'Vị trí', 'Kiểu bàn', 'Trang trí']
            
            global ptpHeader
            ptpHeader = ["ID Phiếu", "ID Khách hàng", "ID Nhân viên", "Thức uống", "ID Bàn", "Trả trước", "Ngày lập"]
            
            global pttHeader
            pttHeader = ['ID Phiếu', 'Thức uống', 'Tên thức uống', 'ID nhân viên', 'Tên nhân viên', 'Tiền nước', 'Phí gửi xe','Tổng cộng', 'VAT', 'Tiền phải trả', 'Ngày in' ]
            
            global pnHeader
            pnHeader = ['ID thức uống', 'Tên thức uống', 'Giá thức uống', 'Trang thái']



            # generate bill from pre-paid bill 
            global dataPhieuTT
            dataPhieuTT = []
            for row in dataPhieuThue:
                tmp = []
                # id phiếu
                tmp.append('PTT' + row[0][3:])
                # thức uống
                tmp.append(row[3])
                #tên thức uống            
                for item in phieuNhapTbAndFood:
                    if (item[0] == row[3]):
                        tmp.append(item[1])
                # id nhân viên
                tmp.append(row[2])
                # lấy tên nhân viên trong bảng dataNv
                for item in dataNv:
                    if (item[0] == row[2]):
                        tmp.append(item[1]+ ' ' +item[2])
                        break
                # lấy tiền thức uống trong bảng phieuNhapTbAndFood
                rentFee = 0
                for row1 in phieuNhapTbAndFood: 
                    if (row1[0] == row[3]):
                        rentFee = int(row1[2])
                        tmp.append(rentFee)
                        break
                # lấy tiền giữ xe trong bảng dataKh, dataNv
                serviceFee = 0
                for item in dataKh:
                    if (item[0] == row[1]):
                        for item2 in dataDv:
                            if (item[5] == item2[1]):
                                serviceFee = item2[2]
                                tmp.append(serviceFee)

                tmp.append(rentFee+serviceFee)
                tmp.append(.15)
                tmp.append(
                        round((rentFee+serviceFee)*1.15, 1)
                )
                tmp.append(str(date.today().isoformat()))
                dataPhieuTT.append(tmp)
            
            dct = {
                'nhanVien': dataNv,
                'khachHang': dataKh,
                'phieuThue': dataPhieuThue,
                'phieuThanhToan': dataPhieuTT,
                'pNhapTbiAndFood': phieuNhapTbAndFood,
                'ban': dataPh,
                'dichVu': dataDv
            }

            with open('./json/data.json', 'w', encoding='utf-8') as fi:
                json.dump(dct, fi, ensure_ascii=False, indent=4)

            with open('./json/data.json', 'r', encoding='utf-8') as fo:
                dataRead = json.loads(fo.read())
            
            # print(json.dumps(dataRead['khachHang'], ensure_ascii=False, indent = 4))
            dataTbl = json.dumps(dataRead[s], ensure_ascii=False)
            global dataTblList
            if (not includeSearch):
                dataTblList = json.loads(dataTbl)
            
            global toRenderHeader
            toRenderHeader = []
            if (s == 'nhanVien'):
                toRenderHeader = nvHeader
            elif (s == 'phieuThue'):
                toRenderHeader = ptpHeader
            elif (s == 'khachHang'):
                toRenderHeader = khHeader
            elif (s == 'phieuThanhToan'):
                toRenderHeader = pttHeader
                # ???
                # tmpnvTbl = json.loads(json.dumps(dataRead['nhanVien'], ensure_ascii=False))
                # tmpDataTbl = dataTblList
                # for r1 in tmpDataTbl:
                #     isFound = False
                #     for r2 in tmpnvTbl:
                #         if (r2[0] == r1[2]):
                #             r1[3] = r2[1] + r2[2]
                #             isFound = True
                #     if (not isFound):
                #         r1[3] = '<Not found>'
            elif (s == 'pNhapTbiAndFood'):
                toRenderHeader = pnHeader
            elif (s == 'dichVu'):
                toRenderHeader = dvHeader
            elif (s == 'ban'):
                toRenderHeader = banHeader
            global rSh
            rSh = Sheet(self.controller.dshbrd, 
                show_table = True,
                width = self.tblWidth,
                height = self.tblHeight,
                show_header = True,
                row_height = 70,
                data = dataTblList,
                headers = list(toRenderHeader)
            )
            # rSh.set_cell_data(0, 0, value = 999, set_copy = True, redraw = False)
            rSh.set_all_cell_sizes_to_text(redraw = True)
            rSh.enable_bindings('all')
            rSh.place(x=340, y=180)
        
        genRight('phieuThue', False)
        
        self.controller.dshbrd.refreshBut = Button(self.controller.dshbrd, text = 'Refresh', bg = 'white')
        self.controller.dshbrd.refreshBut.place(x = 960, y = 105)
        self.controller.dshbrd.deleteBut = Button(self.controller.dshbrd, text = 'Delete', bg = 'white')
        self.controller.dshbrd.deleteBut.place(x = 1020, y = 105)

        def deleteRow(e):
            
            a = rSh.get_currently_selected(get_coords = False, return_nones_if_not = False)
                
            try:
                if (a[0] == 'row'):
                    index = a[1]
                else:
                    index = a[0]
            # chọn hàng hay chọn ô trên tksheet sẽ nhảy chỉ số row khác nhau 
            except (IndexError):
                messagebox.showwarning(title = 'Cảnh báo', message = 'Vui lòng chọn hàng để xóa.')

            if (self.chungTaDangODau == 'phieuThanhToan'):
                messagebox.showwarning(title='Cảnh báo', message='Hóa đơn được sinh ra tương ứng từ phiếu đặt. \nVui lòng xóa phiếu đặt nước.')
                return
            
            def deleteAndExit():
                try:
                    k = index + 1
                except:
                    messagebox.showwarning(title='Cảnh báo', message='Vui lòng nhập đúng định dạng.')
                if (self.chungTaDangODau == 'phieuThue'):
                    global dataPhieuThue
                    del dataPhieuThue[k-1]
                    genRight('phieuThue', False)
                if (self.chungTaDangODau == 'nhanVien'):
                    global dataNv
                    del dataNv[k-1]
                    genRight('nhanVien', False)
                if (self.chungTaDangODau == 'ban'):
                    global dataPh
                    del dataPh[k-1]
                    genRight('ban', False)
                if (self.chungTaDangODau == 'khachHang'):
                    global dataKh
                    del dataKh[k-1]
                    genRight('khachHang', False)
                if (self.chungTaDangODau == 'dichVu'):
                    global dataDv
                    del dataDv[k-1]
                    genRight('dichVu', False)
                if (self.chungTaDangODau == 'pNhapTbiAndFood'):
                    global phieuNhapTbAndFood
                    del phieuNhapTbAndFood[k-1]
                    genRight('pNhapTbiAndFood', False)
            deleteAndExit()
            return
        self.controller.dshbrd.deleteBut.bind("<Button-1>", deleteRow)

        def genBotBut(strTable):
            global chungTaDangODau
            self.chungTaDangODau = strTable
            with open('./json/data.json', 'r', encoding='utf-8') as fo:
                dataRead = json.loads(fo.read())
            dataTbl4GenRight = json.dumps(dataRead[strTable], ensure_ascii=False)
            dataTblList4GenRight = json.loads(dataTbl4GenRight)
            # print(dataTblList4GenRight[0][0])

            saveBotBut = Button(
                self.controller.dshbrd,
                font = ('Chirp', 14),
                text = 'Save ',
                bg = 'white',
                border = '1px solid black',
                height = 1,
                width = 7
            )
            def printSelectedRow():
                data2Print = []
                if (strTable != 'phieuThanhToan'):
                    messagebox.showwarning(title='Cảnh báo', message='Tính năng không khả dụng. Vui lòng chọn mục Hóa đơn để in.')
                    return
                a = rSh.get_currently_selected(get_coords = False, return_nones_if_not = False)
                
                try:
                    if (a[0] == 'row'):
                        data2Print = dataTblList[a[1]]
                        index = a[1]
                    else:
                        data2Print = dataTblList[a[0]]
                        index = a[0]
                # chọn hàng hay chọn ô trên tksheet sẽ nhảy chỉ số row khác nhau 
                except (IndexError):
                    messagebox.showwarning(title = 'Cảnh báo', message = 'Vui lòng chọn hàng để xuất hóa đơn.')
                # print(data2Print)
                pdf = FPDF()
                pdf.alias_nb_pages()
                pdf.add_page()
                pdf.add_font("NotoSans", style="", fname="./fonts/NotoSans-Regular.ttf", uni=True)
                pdf.add_font("NotoSans", style="B", fname="./fonts/NotoSans-Bold.ttf", uni=True)
                pdf.add_font("NotoSans", style="I", fname="./fonts/NotoSans-Italic.ttf", uni=True)
                pdf.add_font("NotoSans", style="BI", fname="./fonts/NotoSans-BoldItalic.ttf", uni=True)
                
                pdf.set_font("NotoSans", style="B", size=12)
                pdf.cell(0, 15, 'CÀ PHÊ SADDAM HUSSEIN', 0, 1, 'C')
                pdf.set_font("NotoSans", style="", size=12)
                #image
                pdf.cell(0, 10, '84/176 Phan Văn Trị, P.2, Q.5, TP.HCM', 0, 1, 'C')
                pdf.cell(0, 10, 'ĐT: 0828.049.514 - 0123.456.789', 0, 1, 'C')
                pdf.set_font("NotoSans", style="B", size=12)
                pdf.cell(0, 15, 'BIÊN LAI KHÁCH HÀNG', 0, 1, 'C')
                pdf.set_font("NotoSans", style="", size=12)
                pdf.ln(5)
                pdf.set_left_margin(20)
                pdf.cell(100, 10, 'Ngày in: ' + str(date.today()), 'L')
                pdf.cell(100, 10, 'Mã số:' + data2Print[0], 'R')
                pdf.ln(5)
                pdf.cell(100, 10, 'Nhân viên: ' + data2Print[3] + "-" + re.sub(' +', ' ',data2Print[4]), 'L', )
                pdf.cell(100, 10, 'In lúc:' + datetime.now().strftime("%H:%M:%S"), 'R')
                pdf.ln(5)
                pdf.cell(100, 10, 'Bàn: ' + str(dataPhieuThue[index][4]) , 'L')
                pdf.cell(100, 10, 'Trả trước: ' + str(dataPhieuThue[index][5]) , 'R')
                pdf.ln(10)
                # print(dataPhieuThue[index])
                pdf.set_left_margin(20)
                exceptThis = [1, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15]
                for i in range(0, len(pttHeader)):
                    if (i == 2):
                        pdf.cell(56, 10, str(pttHeader[i]), border=1)
                    elif (not i in exceptThis):
                        pdf.cell(28, 10, str(pttHeader[i]), border=1)
                pdf.ln(10)
                pdf.set_left_margin(20)
                print(data2Print)
                for i in range(0, len(data2Print)):
                    if (i == 2):
                        pdf.cell(56, 10, str(data2Print[i]), border=1)
                    elif (not i in exceptThis):
                        pdf.cell(28, 10, str(data2Print[i]), border=1)
                pdf.ln(10)

                pdf.set_left_margin(100)
                pdf.set_font("NotoSans", style="BI", size=12)
                pdf.cell(0, 10, 'Thuế VAT: ' + str(int(data2Print[8]*100)) + ' %', 'L')
                pdf.ln(10)
                pdf.cell(0, 10, 'Tổng tiền: ' + str(int(data2Print[9])+1000) + ' VNĐ', 'L')
                pdf.ln(10)
                try:
                    pdf.output('bill.pdf', 'F')
                except:
                    messagebox.showwarning(title = "", message = "File bill.pdf đang được sử dụng, không thể ghi đè")
            
            exportBotBut = Button(
                self.controller.dshbrd,
                font = ('Chirp', 14),
                text = 'Export to PDF',
                bg = 'white',
                border = '1px solid black',
                height = 1,
                width = 15,
                command = printSelectedRow
            )

            sortBut2 = ttk.Combobox(
                self.controller.dshbrd,
                font = ('Chirp', 10),
                values = ['Tăng dần', 'Giảm dần'],
                width = 20,
                cursor = 'hand2')
            sortBut2.set('--Thứ tự--')

            # ???

            srhBox1 = Text(
                height = 1,
                cursor = 'xterm',
                font = ('Chirp', 10),
                width = 20,
                border = '2px solid black'
            )

            # Tìm kiếm Nâng cao - Advanced Searching
            toRenderHeader1 = toRenderHeader
            global toRenderHeader2
            global toRenderHeader3
            global toRenderHeader4
            toRenderHeader2 = []
            toRenderHeader3 = []
            toRenderHeader4 = []
            sAdTextLbl1 = Label(self.controller.dshbrd, text = 'Tìm kiếm nâng cao', bg = 'white')
            sAdTextLbl2 = Label(self.controller.dshbrd, text = 'Từ', bg = 'white')
            sAdTextLbl3 = Label(self.controller.dshbrd, text = 'Đến', bg = 'white')

            selected0 = StringVar()
            sortBut1 = ttk.Combobox(
                self.controller.dshbrd,
                values = list(toRenderHeader1), 
                width = 20,
                textvariable = selected0
            )
            sortBut1.set('--Tiêu chí--')

            selected1 = StringVar()

            sAdLbl1 = ttk.Combobox(
                self.controller.dshbrd,
                values = list(toRenderHeader1), 
                width = 20,
                textvariable= selected1
            )
            sAdLbl1.set('--Tiêu chí--')

            selected2 = StringVar()
            
            sAdLbl2 = ttk.Combobox(
                self.controller.dshbrd,
                values = list(toRenderHeader2),
                width = 20,
                textvariable= selected2
            )
            sAdLbl2.set('--Giá trị--')

            sAdLbl3 = Text(
                self.controller.dshbrd,
                font = ('Chirp', 10),
                width = 10,
                height = 1
            )

            sAdLbl4 = Text(
                self.controller.dshbrd,
                font = ('Chirp', 10),
                width = 10,
                height = 1
            )
            
            def handleNormSearch():
                inp = srhBox1.get("1.0",'end-1c')
                # https://stackoverflow.com/questions/63525858/typeerror-get-missing-1-required-positional-argument-index1
                tmp = []
                for item in dataTblList4GenRight:
                    for jtem in item:
                        if (str(jtem).upper().find(inp.upper()) != -1):
                            tmp.append(item)
                            break
                global dataTblList
                dataTblList = tmp
                genRight(strTable, True)
                return
            def handleAdvancedSearch():
                # Link code: https://www.pythontutorial.net/tkinter/tkinter-combobox/
                tmp = []
                try:
                    index = toRenderHeader1.index(selected1.get())
                except ValueError:
                    messagebox.showwarning(title='Cảnh báo', message='Vui lòng chọn tiêu chí')
                # print(index)
                # print(dataTblList4GenRight[3])
                # print(dataTblList4GenRight[3][index])

                if (strTable == 'nhanVien'):
                    stweird = 3
                else:
                    stweird = 0
                if (not str(dataTblList4GenRight[stweird][index]).isnumeric()):
                    messagebox.showwarning(title='Lỗi', message='Dữ liệu không phải số.')
                    return
                x = sAdLbl3.get("1.0",'end-1c')
                y = sAdLbl4.get("1.0",'end-1c')
                if (x != '' and y != ''):
                    if (x == ''): x = 0
                    if (y == ''): y = 0
                    x = int(x)
                    y = int(y)
                    if (x > y):
                        messagebox.showwarning(title='Lỗi', message='Điểm dưới nhỏ hơn điểm trên.')
                    else:
                        tmp = []
                        for row in dataTblList4GenRight:
                            if ((int(row[index]) > x) and (int(row[index]) < y) ):
                                # lần trước lỡ import lộn NoneType vào database
                                # https://stackoverflow.com/questions/3930188/how-to-convert-nonetype-to-int-or-string
                                tmp.append(row)
                        global dataTblList
                        oldDataHehe = dataTblList
                        dataTblList = tmp
                        genRight(strTable, True)
                        dataTblList = oldDataHehe
                else:
                    messagebox.showwarning(title='Lỗi', message='Bạn chưa nhập khoảng cần tìm.')
                return
            
            global icoSearch
            rawIcoSearch = Image.open('./img/sIco.png')
            rawIcoSearch = rawIcoSearch.resize((20, 20), Image.Resampling.LANCZOS)
            icoSearch = ImageTk.PhotoImage(rawIcoSearch)
            lblSrh1 = Button(self.controller.dshbrd, image = icoSearch, font = ('Chirp', 14),bg = 'white', command = handleNormSearch)
            lblSrh2 = Button(self.controller.dshbrd, image = icoSearch, font = ('Chirp', 14),bg = 'white', command = handleAdvancedSearch)

            # binding 
            def tmp1(e): 
                global toRenderHeader2
                toRenderHeader2 = []
                usrSel1 = e.widget.get()
                sAdLbl1.set(e.widget.get())
                if (tabSel[0] and usrSel1 in ptpHeader):
                    for item in dataTblList4GenRight:
                        toRenderHeader2.append(item[ptpHeader.index(usrSel1)])
                    toRenderHeader2 = list(set(toRenderHeader2))
                    sAdLbl2['values'] = toRenderHeader2
                if (tabSel[1] and usrSel1 in pttHeader):
                    for item in dataTblList4GenRight:
                        toRenderHeader2.append(item[pttHeader.index(usrSel1)])
                    toRenderHeader2 = list(set(toRenderHeader2))
                    sAdLbl2['values'] = toRenderHeader2
                if (tabSel[2] and usrSel1 in banHeader):
                    for item in dataTblList4GenRight:
                        toRenderHeader2.append(item[banHeader.index(usrSel1)])
                    toRenderHeader2 = list(dict.fromkeys(toRenderHeader2))
                    sAdLbl2['values'] = toRenderHeader2
                if (tabSel[3] and usrSel1 in nvHeader):
                    for item in dataTblList4GenRight:
                        toRenderHeader2.append(item[nvHeader.index(usrSel1)])
                    toRenderHeader2 = list(set(toRenderHeader2))
                    sAdLbl2['values'] = toRenderHeader2
                if (tabSel[4] and usrSel1 in khHeader):
                    for item in dataTblList4GenRight:
                        toRenderHeader2.append(item[khHeader.index(usrSel1)])
                    toRenderHeader2 = list(set(toRenderHeader2))
                    sAdLbl2['values'] = toRenderHeader2
                if (tabSel[5] and usrSel1 in dvHeader):
                    for item in dataTblList4GenRight:
                        toRenderHeader2.append(item[dvHeader.index(usrSel1)])
                    toRenderHeader2 = list(set(toRenderHeader2))
                    sAdLbl2['values'] = toRenderHeader2
                if (tabSel[5] and usrSel1 in pnHeader):
                    for item in dataTblList4GenRight:
                        toRenderHeader2.append(item[pnHeader.index(usrSel1)])
                    toRenderHeader2 = list(set(toRenderHeader2))
                    sAdLbl2['values'] = toRenderHeader2
            def tmp2(e): 
                sAdLbl2.set(e.widget.get())
                sample = e.widget.get()
                index = toRenderHeader1.index(selected1.get())
                tmp = []
                global dataTblList
                for row in dataTblList:
                    if (sample == row[index]):
                        tmp.append(row)
                    elif (sample == str(row[index])):
                        tmp.append(row)
                oldDataHehe = dataTblList
                dataTblList = tmp
                genRight(strTable, True)
                dataTblList = oldDataHehe
                return
            def tmp3(e):
                global dataTblList
                index = toRenderHeader1.index(selected0.get())
                if (e.widget.get() == 'Tăng dần'):
                    dataTblList = sorted(dataTblList, key = itemgetter(index))
                    genRight(strTable, True)
                else:
                    dataTblList = sorted(dataTblList, key = itemgetter(index))
                    dataTblList = dataTblList[::-1]
                    genRight(strTable, True)
                return

            def parseAndSave(e):
                new_table = rSh.get_sheet_data(False, False, False)
                try:
                    con = sqlite3.connect('example.db')
                except:
                    print('Không kết nối được file *.db')

                cur = con.cursor()

                if (strTable == 'phieuThue'):
                    try:
                        cur.execute('drop table '+strTable)
                    except sqlite3.OperationalError:
                        print('Không drop được table phiếu đặt.')
                    cur.execute('''CREATE TABLE  '''
                    + strTable
                    + '''
                        (id text, 
                        idkh text,
                        idnv text,
                        iddv text,
                        idban text,
                        tratruoc bool,
                        ngaylap text
                    )''')
                    for row in new_table:
                        cur.execute(
                            '''
                            INSERT INTO {}
                            VALUES ('{}', '{}', '{}', '{}', '{}', {}, '{}')
                            '''.format(strTable, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                        )
                    print('Đã insert value thành công')
                    print(new_table)
                    con.commit()
                elif (strTable == 'phieuThanhToan'):
                    try:
                        cur.execute('drop table '+strTable)
                    except sqlite3.OperationalError:
                        pass
                    cur.execute('''CREATE TABLE  '''
                    + strTable
                    + '''    
                        (id text, 
                        iddrink text,
                        tendrink text,
                        idnv text,
                        tennv text,
                        price int,
                        guixe int,
                        tong int,
                        vat real,
                        tienphaitra real,
                        ngayin text
                    )''')
                    for row in new_table:
                        cur.execute(
                            '''
                            INSERT INTO {}
                            VALUES ('{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, '{}')
                            '''.format(strTable, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                        )
                    con.commit()
                    genRight('phieuThue', False)
                elif (strTable == 'ban'):
                    try:
                        cur.execute('drop table ban')
                    except sqlite3.OperationalError:
                        pass
                    cur.execute('''CREATE TABLE ban '''
                        + '''    
                            (id text, 
                            people text,
                            status text,
                            pos text,
                            shape text,
                            deco text
                        )'''
                    )
                    for row in new_table:
                        cur.execute('''
                            INSERT INTO {}
                            VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
                            '''.format(strTable, row[0], row[1], row[2], row[3], row[4], row[5])
                        )
                    con.commit()
                elif (strTable == 'nhanVien'):
                    try:
                        cur.execute('drop table '+strTable)
                    except sqlite3.OperationalError:
                        pass
                    cur.execute('''CREATE TABLE  '''
                    + strTable
                    + '''    
                        (id text, 
                        ho text,
                        ten text,
                        gender text,
                        year int,
                        quequan text,
                        chucvu text,
                        tochuc text,
                        luong int,
                        thuong int
                    )''')
                    for row in new_table:
                        cur.execute(
                            '''
                            INSERT INTO {}
                            VALUES ('{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', {}, {})
                            '''.format(strTable, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                        )
                    con.commit()
                elif (strTable == 'khachHang'):
                    try:
                        cur.execute('drop table '+strTable)
                    except sqlite3.OperationalError:
                        pass
                    cur.execute('''CREATE TABLE  '''
                    + strTable
                    + '''    
                        (id text, 
                        ho text,
                        ten text,
                        gender text,
                        namsinh int,
                        typexe text
                    )''')
                    for row in new_table:
                        cur.execute(
                            '''
                            INSERT INTO {}
                            VALUES ('{}', '{}', '{}', '{}', {}, '{}')
                            '''.format(strTable, row[0], row[1], row[2], row[3], row[4], row[5])
                        )
                    con.commit()
                elif (strTable == 'dichVu'):
                    try:
                        cur.execute('drop table '+strTable)
                    except sqlite3.OperationalError:
                        print("Không drop được table dịch vụ.")
                        pass
                    cur.execute('''CREATE TABLE  '''
                    + strTable
                    + '''    
                        (id text, 
                        ten text,
                        price int
                    )''')
                    for row in new_table:
                        cur.execute(
                            '''
                            INSERT INTO {}
                            VALUES ('{}', '{}', {})
                            '''.format(strTable, row[0], row[1], row[2])
                        )
                    con.commit()
                elif (strTable == 'pNhapTbiAndFood'):
                    try:
                        cur.execute('drop table '+strTable)
                    except sqlite3.OperationalError:
                        pass
                    cur.execute('''CREATE TABLE  '''
                    + strTable
                    + '''    
                        (id text, 
                        name text,
                        price int,
                        status text
                    )''')
                    for row in new_table:
                        cur.execute(
                            '''
                            INSERT INTO {}
                            VALUES ('{}', '{}', {}, '{}')
                            '''.format(strTable, row[0], row[1], row[2], row[3])
                        )
                    con.commit()

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
                    
                cur.execute('''
                            SELECT * FROM {}
                        '''.format(strTable))
                # print(cur.fetchall())

                return

            sAdLbl1.bind("<<ComboboxSelected>>", tmp1)
            sAdLbl2.bind("<<ComboboxSelected>>", tmp2)
            sortBut2.bind("<<ComboboxSelected>>", tmp3)
            saveBotBut.bind("<Button-1>", parseAndSave)
            # end binding

            saveBotBut.place(x=750, y=630)
            exportBotBut.place(x=900, y=630)

            srhBox1.place(x=390, y=110)
            lblSrh1.place(x=555, y=105)
            sortBut1.place(x=625, y=110)
            sortBut2.place(x=780, y=110)

            sAdTextLbl1.place(x=340, y=150)
            sAdTextLbl2.place(x=845, y=150)
            sAdTextLbl3.place(x=975, y=150)
            sAdLbl1.place(x=475, y =150)
            sAdLbl2.place(x=650, y =150)
            sAdLbl3.place(x=745+130, y =150)
            sAdLbl4.place(x=745+260, y =150)
            lblSrh2.place(x=1095, y= 150)

        genBotBut('phieuThue')

        def renderInpPhieuThue(e):
            self.controller.dshbrd.inpPTP = Toplevel(self.controller.dshbrd)
            self.controller.dshbrd.inpPTP.title('Nhập thông tin phiếu đặt thức uống')
            self.controller.dshbrd.inpPTP.geometry('800x400')
            self.controller.dshbrd.inpPTP.lbl1 = Label(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), text = 'ID phiếu')
            self.controller.dshbrd.inpPTP.lbl2 = Label(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), text = 'ID khách hàng')
            self.controller.dshbrd.inpPTP.lbl3 = Label(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), text = 'ID nhân viên')
            self.controller.dshbrd.inpPTP.lbl4 = Label(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), text = 'ID bàn')
            self.controller.dshbrd.inpPTP.lbl5 = Label(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), text = 'Tên thức uống')
            self.controller.dshbrd.inpPTP.lbl6 = Label(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), text = 'Trả trước')
            heightSpacing = 50
            
            self.controller.dshbrd.inpPTP.lbl1.place(x = 10, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpPTP.lbl2.place(x = 10, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpPTP.lbl3.place(x = 10, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.inpPTP.lbl4.place(x = 10, y = 10 + heightSpacing * 3)
            self.controller.dshbrd.inpPTP.lbl5.place(x = 10, y = 10 + heightSpacing * 4)
            self.controller.dshbrd.inpPTP.lbl6.place(x = 10, y = 10 + heightSpacing * 5)
            max = 0
            for row in dataPhieuThue:
                here = int(row[0][3:])
                if (here > max): max = here
            new_code = 'PDN' + str(max+1).zfill(4)
            kh = []
            nv = []
            drink = []
            ban = []
            for row in dataKh: kh.append(row[0])
            for row in dataNv: nv.append(row[0])
            for row in phieuNhapTbAndFood: drink.append(row[1])
            for row in dataPh: ban.append(row[0])
            self.controller.dshbrd.inpPTP.txt1 = Label(self.controller.dshbrd.inpPTP, text = new_code, font = ('Chirp', 10), height = 1, width = 30)
            self.controller.dshbrd.inpPTP.txt2 = ttk.Combobox(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), height = 1, width = 30, values = kh)
            # khách hàng
            self.controller.dshbrd.inpPTP.txt3 = ttk.Combobox(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), height = 1, width = 30, values = nv)
            # nhân viên
            self.controller.dshbrd.inpPTP.txt4 = ttk.Combobox(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), height = 1, width = 30, values = ban)
            # bàn
            self.controller.dshbrd.inpPTP.txt5 = ttk.Combobox(self.controller.dshbrd.inpPTP, font = ('Chirp', 10), height = 1, width = 30, values = drink)
            # thức uống
            self.controller.dshbrd.inpPTP.txt6Var = ttk.Combobox(self.controller.dshbrd.inpPTP, values = ['True', 'False'], text = 'Đã trả')
            # trả trước

            self.controller.dshbrd.inpPTP.txt1.place(x = 120, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpPTP.txt2.place(x = 120, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpPTP.txt3.place(x = 120, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.inpPTP.txt4.place(x = 120, y = 10 + heightSpacing * 3)
            self.controller.dshbrd.inpPTP.txt5.place(x = 120, y = 10 + heightSpacing * 4)
            self.controller.dshbrd.inpPTP.txt6Var.place(x = 120, y = 10 + heightSpacing * 5)
            
            def addData():
                tmp = []
                tmp.append(new_code)
                tmp.append(self.controller.dshbrd.inpPTP.txt2.get())
                tmp.append(self.controller.dshbrd.inpPTP.txt3.get())
                tmp.append(self.controller.dshbrd.inpPTP.txt4.get())
                temp = self.controller.dshbrd.inpPTP.txt5.get()
                for row in phieuNhapTbAndFood:
                    if (temp == row[1]):
                        tmp.append(row[0])
                        break
                tmp.append(bool(self.controller.dshbrd.inpPTP.txt6Var.get()))
                tmp.append('01/01/2001')
                tmp[3], tmp[4] = tmp[4], tmp[3]
                for row in phieuNhapTbAndFood:
                    if (row[0] == tmp[3] and row[3] == 'No'):
                        messagebox.showwarning(title='Thông báo', message = 'Thức uống không sẵn sàng để phục vụ.')
                        return
                global dataPhieuThue
                dataPhieuThue.append(tmp)
                messagebox.showwarning(title='Thông báo', message = 'Đã thêm thành công.')
                genRight('phieuThue', False)
                self.controller.dshbrd.inpPTP.destroy()
                return
            def quitjob():
                self.controller.dshbrd.inpPTP.destroy()
                return
            self.controller.dshbrd.inpPTP.but1 = Button(self.controller.dshbrd.inpPTP, text='Save', font = ('Chirp', 11), command =  addData)
            self.controller.dshbrd.inpPTP.but2 = Button(self.controller.dshbrd.inpPTP, text='Cancel', font = ('Chirp', 11), command = quitjob)
            self.controller.dshbrd.inpPTP.but1.place(x=120, y = 10 + heightSpacing * 6)
            self.controller.dshbrd.inpPTP.but2.place(x=240, y = 10 + heightSpacing * 6)
            self.controller.dshbrd.inpPTP.mainloop()
            return

        def renderInpBan(e):
            self.controller.dshbrd.phg = Toplevel(self.controller.dshbrd)
            self.controller.dshbrd.phg.title('Thông tin bàn ghế')
            self.controller.dshbrd.phg.geometry('400x400')
            self.controller.dshbrd.phg.lbl1 = Label(self.controller.dshbrd.phg, font = ('Chirp', 10), text = 'ID bàn')
            self.controller.dshbrd.phg.lbl2 = Label(self.controller.dshbrd.phg, font = ('Chirp', 10), text = 'Loại bàn')
            self.controller.dshbrd.phg.lbl3 = Label(self.controller.dshbrd.phg, font = ('Chirp', 10), text = 'Trang thái')
            self.controller.dshbrd.phg.lbl4 = Label(self.controller.dshbrd.phg, font = ('Chirp', 10), text = 'Vị trí')
            self.controller.dshbrd.phg.lbl5 = Label(self.controller.dshbrd.phg, font = ('Chirp', 10), text = 'Kiểu bàn')
            self.controller.dshbrd.phg.lbl6 = Label(self.controller.dshbrd.phg, font = ('Chirp', 10), text = 'Trang trí')
            heightSpacing = 50
            self.controller.dshbrd.phg.lbl1.place(x = 10, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.phg.lbl2.place(x = 10, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.phg.lbl3.place(x = 10, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.phg.lbl4.place(x = 10, y = 10 + heightSpacing * 3)
            self.controller.dshbrd.phg.lbl5.place(x = 10, y = 10 + heightSpacing * 4)
            self.controller.dshbrd.phg.lbl6.place(x = 10, y = 10 + heightSpacing * 5)
            
            self.controller.dshbrd.phg.txt1 = Text(self.controller.dshbrd.phg, font = ('Chirp', 10), height = 1, width = 40)
            self.controller.dshbrd.phg.txt2 = ttk.Combobox(self.controller.dshbrd.phg, font = ('Chirp', 10), height = 1, width = 40, values = ['2 người', '3 người', '5 người', '8 người'])
            self.controller.dshbrd.phg.txt3 = ttk.Combobox(self.controller.dshbrd.phg, font = ('Chirp', 10), height = 1, width = 40, values = ['Tầng trệt', 'Tầng 1', 'Tầng 2', 'Tầng 3'])
            self.controller.dshbrd.phg.txt4 = ttk.Combobox(self.controller.dshbrd.phg, values = ['available', 'occupied'])
            self.controller.dshbrd.phg.txt5 = ttk.Combobox(self.controller.dshbrd.phg, values = ['Vuông', 'Tròn'])
            self.controller.dshbrd.phg.txt6 = Text(self.controller.dshbrd.phg, font = ('Chirp', 10), height = 1, width = 40)
            

            self.controller.dshbrd.phg.txt1.place(x = 100, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.phg.txt2.place(x = 100, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.phg.txt3.place(x = 100, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.phg.txt4.place(x = 100, y = 10 + heightSpacing * 3)
            self.controller.dshbrd.phg.txt5.place(x = 100, y = 10 + heightSpacing * 4)
            self.controller.dshbrd.phg.txt6.place(x = 100, y = 10 + heightSpacing * 5)
            
            def addData():
                tmp = []
                tmp.append(self.controller.dshbrd.phg.txt1.get("1.0",'end-1c'))
                if (len(tmp[0]) != 4):
                    messagebox.showwarning(title = "Lỗi", message = "Vui lòng nhập đúng định dạng 1 ký tự + 3 chữ số.")
                    return
                global dataPh
                for row in dataPh:
                    if (tmp[0] == row[0]):
                        messagebox.showwarning(title = "Lỗi", message = "ID bàn này đã có rồi.")
                        return
                tmp.append(self.controller.dshbrd.phg.txt2.get())
                tmp.append(self.controller.dshbrd.phg.txt3.get())
                tmp.append(self.controller.dshbrd.phg.txt4.get())
                tmp.append(self.controller.dshbrd.phg.txt5.get())
                tmp.append(self.controller.dshbrd.phg.txt6.get("1.0",'end-1c'))
                tmp[2], tmp[3] = tmp[3], tmp[2]
                dataPh.append(tmp)
                genRight('ban', False)
                self.controller.dshbrd.phg.destroy()
            def quitjob():
                self.controller.dshbrd.phg.destroy()

            self.controller.dshbrd.phg.but1 = Button(self.controller.dshbrd.phg, text='Save', font = ('Chirp', 11), command =  addData)
            self.controller.dshbrd.phg.but2 = Button(self.controller.dshbrd.phg, text='Cancel', font = ('Chirp', 11), command = quitjob)
            self.controller.dshbrd.phg.but1.place(x=120, y= 10 + heightSpacing * 6)
            self.controller.dshbrd.phg.but2.place(x=240, y= 10 + heightSpacing * 6)


        def renderInpKh(e):
            self.controller.dshbrd.inpKh = Toplevel(self.controller.dshbrd)
            self.controller.dshbrd.inpKh.title('Thông tin khách hàng')
            self.controller.dshbrd.inpKh.geometry('400x380')
            self.controller.dshbrd.inpKh.lbl1 = Label(self.controller.dshbrd.inpKh, font = ('Chirp', 10), text = 'ID')
            self.controller.dshbrd.inpKh.lbl2 = Label(self.controller.dshbrd.inpKh, font = ('Chirp', 10), text = 'Họ')
            self.controller.dshbrd.inpKh.lbl3 = Label(self.controller.dshbrd.inpKh, font = ('Chirp', 10), text = 'Tên')
            self.controller.dshbrd.inpKh.lbl4 = Label(self.controller.dshbrd.inpKh, font = ('Chirp', 10), text = 'Giới tính')
            self.controller.dshbrd.inpKh.lbl5 = Label(self.controller.dshbrd.inpKh, font = ('Chirp', 10), text = 'Năm sinh')
            self.controller.dshbrd.inpKh.lbl6 = Label(self.controller.dshbrd.inpKh, font = ('Chirp', 10), text = 'Loại xe')
            
            heightSpacing = 50
            self.controller.dshbrd.inpKh.lbl1.place(x = 10, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpKh.lbl2.place(x = 10, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpKh.lbl3.place(x = 10, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.inpKh.lbl4.place(x = 10, y = 10 + heightSpacing * 3)
            self.controller.dshbrd.inpKh.lbl5.place(x = 10, y = 10 + heightSpacing * 4)
            self.controller.dshbrd.inpKh.lbl6.place(x = 10, y = 10 + heightSpacing * 5)
            
            autoKh = 'KH' + str(len(dataKh)+1).zfill(3)
            self.controller.dshbrd.inpKh.txt1 = Label(self.controller.dshbrd.inpKh, font = ('Chirp', 10), height = 1, width = 30, text = autoKh)
            self.controller.dshbrd.inpKh.txt2 = Text(self.controller.dshbrd.inpKh, font = ('Chirp', 10), height = 1, width = 30)
            self.controller.dshbrd.inpKh.txt3 = Text(self.controller.dshbrd.inpKh, font = ('Chirp', 10), height = 1, width = 30)
            var = StringVar()
            years = list(range(1960, 2020, 1))
            self.controller.dshbrd.inpKh.gender = ttk.Combobox(self.controller.dshbrd.inpKh, values = ['Nam', 'Nữ'])
            self.controller.dshbrd.inpKh.txt5 = ttk.Combobox(self.controller.dshbrd.inpKh, font = ('Chirp', 10), height = 1, width = 30, values = years)
            self.controller.dshbrd.inpKh.txt6 = ttk.Combobox(self.controller.dshbrd.inpKh, font = ('Chirp', 10), height = 1, width = 30, values = ['2 bánh', '4 bánh'])
            

            self.controller.dshbrd.inpKh.txt1.place(x = 100, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpKh.txt2.place(x = 100, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpKh.txt3.place(x = 100, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.inpKh.gender.place(x = 100, y = 10 + heightSpacing * 3)
            self.controller.dshbrd.inpKh.txt5.place(x = 100, y = 10 + heightSpacing * 4)
            self.controller.dshbrd.inpKh.txt6.place(x = 100, y = 10 + heightSpacing * 5)
            
            def addData():
                tmp = []
                tmp.append(autoKh)
                tmp.append(self.controller.dshbrd.inpKh.txt2.get("1.0",'end-1c'))
                tmp.append(self.controller.dshbrd.inpKh.txt3.get("1.0",'end-1c'))
                tmp.append(self.controller.dshbrd.inpKh.gender.get())
                tmp.append(int(self.controller.dshbrd.inpKh.txt5.get()))
                tmp.append(self.controller.dshbrd.inpKh.txt6.get())
                global dataKh
                dataKh.append(tmp)
                genRight('khachHang', False)
            def quitjob(): self.controller.dshbrd.inpKh.destroy()

            self.controller.dshbrd.inpKh.but1 = Button(self.controller.dshbrd.inpKh, text='Save', font = ('Chirp', 11), command =  addData)
            self.controller.dshbrd.inpKh.but2 = Button(self.controller.dshbrd.inpKh, text='Cancel', font = ('Chirp', 11), command = quitjob)
            self.controller.dshbrd.inpKh.but1.place(x=120, y= 10 + heightSpacing * 6)
            self.controller.dshbrd.inpKh.but2.place(x=240, y= 10 + heightSpacing * 6)
            return

        def renderInpNhanVien(e):
            self.controller.dshbrd.inpNv = Toplevel(self.controller.dshbrd)
            self.controller.dshbrd.inpNv.title(' Thông tin nhân viên')
            self.controller.dshbrd.inpNv.geometry('700x800')
            self.controller.dshbrd.inpNv.lbl1 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'ID:')
            self.controller.dshbrd.inpNv.lbl2 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'Họ')
            self.controller.dshbrd.inpNv.lbl3 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'Tên')
            self.controller.dshbrd.inpNv.lbl4 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'Giới tính')
            self.controller.dshbrd.inpNv.lbl5 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'Năm sinh')
            self.controller.dshbrd.inpNv.lbl6 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'Quê quán')
            self.controller.dshbrd.inpNv.lbl7 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'Chức vụ')
            self.controller.dshbrd.inpNv.lbl8 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'Bộ phận')
            self.controller.dshbrd.inpNv.lbl9 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'Lương')
            self.controller.dshbrd.inpNv.lbl10 = Label(self.controller.dshbrd.inpNv, font = ('Chirp', 10), text = 'Thưởng')
            heightSpacing = 50
            self.controller.dshbrd.inpNv.lbl1.place(x = 10, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpNv.lbl2.place(x = 10, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpNv.lbl3.place(x = 10, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.inpNv.lbl4.place(x = 10, y = 10 + heightSpacing * 3)
            self.controller.dshbrd.inpNv.lbl5.place(x = 10, y = 10 + heightSpacing * 4)
            self.controller.dshbrd.inpNv.lbl6.place(x = 10, y = 10 + heightSpacing * 5)
            self.controller.dshbrd.inpNv.lbl7.place(x = 10, y = 10 + heightSpacing * 6)
            self.controller.dshbrd.inpNv.lbl8.place(x = 10, y = 10 + heightSpacing * 7)
            self.controller.dshbrd.inpNv.lbl9.place(x = 10, y = 10 + heightSpacing * 8)
            self.controller.dshbrd.inpNv.lbl10.place(x = 10, y = 10 + heightSpacing * 9)
            
            self.controller.dshbrd.inpNv.txt1 = Text(self.controller.dshbrd.inpNv, font = ('Chirp', 10), height = 1, width = 40)
            self.controller.dshbrd.inpNv.txt2 = Text(self.controller.dshbrd.inpNv, font = ('Chirp', 10), height = 1, width = 40)
            self.controller.dshbrd.inpNv.txt3 = Text(self.controller.dshbrd.inpNv, font = ('Chirp', 10), height = 1, width = 40)

            self.controller.dshbrd.inpNv.txt4 = ttk.Combobox( self.controller.dshbrd.inpNv, values = ['Nam', 'Nữ'])
            years = list(range(1960, 2020, 1))
            self.controller.dshbrd.inpNv.txt5 = ttk.Combobox( self.controller.dshbrd.inpNv, font = ('Chirp', 10), height = 1, width = 40, values = years)
            self.controller.dshbrd.inpNv.txt6 = Text( self.controller.dshbrd.inpNv, font = ('Chirp', 10), height = 1, width = 40)
            self.controller.dshbrd.inpNv.txt7 = Text( self.controller.dshbrd.inpNv, font = ('Chirp', 10), height = 1, width = 40)
            bophan = ['Lễ tân', 'Vệ sinh', 'Hội đồng quản trị', 'Quản trị nhân sự', 'Kế toán', 'Bảo vệ', 'Vận chuyển']
            self.controller.dshbrd.inpNv.txt8 = ttk.Combobox( self.controller.dshbrd.inpNv, font = ('Chirp', 10), height = 1, width = 40, values = bophan)
            self.controller.dshbrd.inpNv.txt9 = Text( self.controller.dshbrd.inpNv, font = ('Chirp', 10), height = 1, width = 40)
            self.controller.dshbrd.inpNv.txt10 = Text( self.controller.dshbrd.inpNv, font = ('Chirp', 10), height = 1, width = 40)

            self.controller.dshbrd.inpNv.txt1.place(x = 100, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpNv.txt2.place(x = 100, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpNv.txt3.place(x = 100, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.inpNv.txt4.place(x = 100, y = 10 + heightSpacing * 3)
            self.controller.dshbrd.inpNv.txt5.place(x = 100, y = 10 + heightSpacing * 4)
            self.controller.dshbrd.inpNv.txt6.place(x = 100, y = 10 + heightSpacing * 5)
            self.controller.dshbrd.inpNv.txt7.place(x = 100, y = 10 + heightSpacing * 6)
            self.controller.dshbrd.inpNv.txt8.place(x = 100, y = 10 + heightSpacing * 7)
            self.controller.dshbrd.inpNv.txt9.place(x = 100, y = 10 + heightSpacing * 8)
            self.controller.dshbrd.inpNv.txt10.place(x = 100, y = 10 + heightSpacing * 9)
            
            def addData():
            
                tmp = []
                tmp.append(self.controller.dshbrd.inpNv.txt1.get("1.0",'end-1c'))
                tmp.append(self.controller.dshbrd.inpNv.txt2.get("1.0",'end-1c'))
                tmp.append(self.controller.dshbrd.inpNv.txt3.get("1.0",'end-1c'))
                tmp.append(self.controller.dshbrd.inpNv.txt4.get())
                try:
                    tmp.append(int(self.controller.dshbrd.inpNv.txt5.get("1.0",'end-1c')))
                except ValueError:
                    messagebox.showwarning(title='Cảnh báo', message = 'Vui lòng nhập năm sinh bằng số.')
                tmp.append(self.controller.dshbrd.inpNv.txt6.get("1.0",'end-1c'))
                tmp.append(self.controller.dshbrd.inpNv.txt7.get("1.0",'end-1c'))
                tmp.append(self.controller.dshbrd.inpNv.txt8.get())
                tmp.append(int(self.controller.dshbrd.inpNv.txt9.get()))
                try:
                    tmp.append(int(self.controller.dshbrd.inpNv.txt10.get("1.0",'end-1c')))
                except ValueError:
                    messagebox.showwarning(title = 'Cảnh báo', message = 'Vui lòng nhập tiền thưởng bằng số.')
                global dataNv
                for row in dataNv:
                    if (row[0] == tmp[0]):
                        messagebox.showwarning(title = 'Cảnh báo', message = 'ID này đã tồn tại.')
                        return
                if (len(tmp) != 10): return
                dataNv.append(tmp)
                messagebox.showwarning(title='Thông báo', message = 'Đã thêm thành công.')
                quitjob()
                genRight('nhanVien', False)
            def quitjob():  self.controller.dshbrd.inpNv.destroy()
            self.controller.dshbrd.inpNv.but1 = Button(self.controller.dshbrd.inpNv, text='Save', font = ('Chirp', 11), command =  addData)
            self.controller.dshbrd.inpNv.but2 = Button(self.controller.dshbrd.inpNv, text='Cancel', font = ('Chirp', 11), command = quitjob)
            self.controller.dshbrd.inpNv.but1.place(x=120, y= 10 + heightSpacing * 10)
            self.controller.dshbrd.inpNv.but2.place(x=240, y= 10 + heightSpacing * 10)

        def renderInpDv(e):
            self.controller.dshbrd.inpDv = Toplevel(self.controller.dshbrd)
            self.controller.dshbrd.inpDv.title('Thông tin dịch vụ')
            self.controller.dshbrd.inpDv.geometry('400x380')
            self.controller.dshbrd.inpDv.lbl1 = Label(self.controller.dshbrd.inpDv, font = ('Chirp', 10), text = 'ID')
            self.controller.dshbrd.inpDv.lbl2 = Label(self.controller.dshbrd.inpDv, font = ('Chirp', 10), text = 'Tên dịch vụ')
            self.controller.dshbrd.inpDv.lbl3 = Label(self.controller.dshbrd.inpDv, font = ('Chirp', 10), text = 'Chi phí')

            heightSpacing = 50
            self.controller.dshbrd.inpDv.lbl1.place(x = 10, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpDv.lbl2.place(x = 10, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpDv.lbl3.place(x = 10, y = 10 + heightSpacing * 2)

            self.controller.dshbrd.inpDv.txt1 = Text(self.controller.dshbrd.inpDv, font = ('Chirp', 10), height = 1, width = 40)
            self.controller.dshbrd.inpDv.txt2 = Text(self.controller.dshbrd.inpDv, font = ('Chirp', 10), height = 1, width = 40)
            self.controller.dshbrd.inpDv.txt3 = Text(self.controller.dshbrd.inpDv, font = ('Chirp', 10), height = 1, width = 40)

            self.controller.dshbrd.inpDv.txt1.place(x = 100, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpDv.txt2.place(x = 100, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpDv.txt3.place(x = 100, y = 10 + heightSpacing * 2)
            global dataDv
            self.controller.dshbrd.inpDv.txt1.insert('end', 'DV' + str(len(dataDv)+1).zfill(3))

            def addData():
                tmp = []
                global dataDv
                tmp.append(self.controller.dshbrd.inpDv.txt1.get("1.0",'end-1c'))
                tmp.append(self.controller.dshbrd.inpDv.txt2.get("1.0",'end-1c'))
                try:
                    tmp.append(int(self.controller.dshbrd.inpDv.txt3.get("1.0",'end-1c')))
                except ValueError:
                    messagebox.showwarning(title='Cảnh báo', message = 'Vui lòng nhập giá dịch vụ ở định dạng số.')
                for row in dataDv:
                    if (row[0] == self.controller.dshbrd.inpDv.txt1.get("1.0",'end-1c')):
                        messagebox.showwarning(title='Cảnh báo', message = 'ID dịch vụ đã tồn tại. Vui lòng dùng ID khác.')
                        return
                dataDv.append(tmp)
                genRight('dichVu', False)
            def quitjob(): self.controller.dshbrd.inpDv.destroy()
            self.controller.dshbrd.inpDv.but1 = Button(self.controller.dshbrd.inpDv, text='Save', font = ('Chirp', 11), command =  addData)
            self.controller.dshbrd.inpDv.but2 = Button(self.controller.dshbrd.inpDv, text='Cancel', font = ('Chirp', 11), command = quitjob)
            self.controller.dshbrd.inpDv.but1.place(x=120, y= 10 + heightSpacing * 3)
            self.controller.dshbrd.inpDv.but2.place(x=240, y= 10 + heightSpacing * 3)
            return

        

        def renderInpProduct(e):
            self.controller.dshbrd.inpPr = Toplevel(self.controller.dshbrd)
            self.controller.dshbrd.inpPr.title('Nhập thông tin đồ uống')
            self.controller.dshbrd.inpPr.geometry('600x400')
            self.controller.dshbrd.inpPr.lbl1 = Label(self.controller.dshbrd.inpPr, font = ('Chirp', 10), text = 'ID thức uống')
            self.controller.dshbrd.inpPr.lbl2 = Label(self.controller.dshbrd.inpPr, font = ('Chirp', 10), text = 'Tên thức uống')
            self.controller.dshbrd.inpPr.lbl3 = Label(self.controller.dshbrd.inpPr, font = ('Chirp', 10), text = 'Giá thức uống')
            self.controller.dshbrd.inpPr.lbl4 = Label(self.controller.dshbrd.inpPr, font = ('Chirp', 10), text = 'Trạng thái')
            
            heightSpacing = 50
            self.controller.dshbrd.inpPr.lbl1.place(x = 10, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpPr.lbl2.place(x = 10, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpPr.lbl3.place(x = 10, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.inpPr.lbl4.place(x = 10, y = 10 + heightSpacing * 3)
            idpro = 'P' + str(len(phieuNhapTbAndFood)+1).zfill(3)
            self.controller.dshbrd.inpPr.txt1 = Label(self.controller.dshbrd.inpPr, font = ('Chirp', 10), height = 1, width = 40, text = idpro)
            self.controller.dshbrd.inpPr.txt2 = Text(self.controller.dshbrd.inpPr, font = ('Chirp', 10), height = 1, width = 40)
            self.controller.dshbrd.inpPr.txt3 = Text(self.controller.dshbrd.inpPr, font = ('Chirp', 10), height = 1, width = 40)
            self.controller.dshbrd.inpPr.txt4 = ttk.Combobox(self.controller.dshbrd.inpPr, font = ('Chirp', 10), height = 1, width = 40, values = ["Yes", "No"])

            self.controller.dshbrd.inpPr.txt1.place(x = 125, y = 10 + heightSpacing * 0)
            self.controller.dshbrd.inpPr.txt2.place(x = 125, y = 10 + heightSpacing * 1)
            self.controller.dshbrd.inpPr.txt3.place(x = 125, y = 10 + heightSpacing * 2)
            self.controller.dshbrd.inpPr.txt4.place(x = 125, y = 10 + heightSpacing * 3)
            def addData():
                tmp = []
                tmp.append(idpro)
                tmp.append(self.controller.dshbrd.inpPr.txt2.get("1.0",'end-1c'))
                tmp.append(int(self.controller.dshbrd.inpPr.txt3.get("1.0",'end-1c')))
                tmp.append(self.controller.dshbrd.inpPr.txt4.get())
                global phieuNhapTbAndFood
                phieuNhapTbAndFood.append(tmp)
                genRight('pNhapTbiAndFood', False)
                return
            def quitjob(): self.controller.dshbrd.inpPr.destroy()
            self.controller.dshbrd.inpPr.but1 = Button(self.controller.dshbrd.inpPr, text='Save', font = ('Chirp', 11), command =  addData)
            self.controller.dshbrd.inpPr.but2 = Button(self.controller.dshbrd.inpPr, text='Cancel', font = ('Chirp', 11), command = quitjob)
            self.controller.dshbrd.inpPr.but1.place(x=120, y= 10 + heightSpacing * 4)
            self.controller.dshbrd.inpPr.but2.place(x=240, y= 10 + heightSpacing * 4)
            return

        global icoAdd
        rawIcoAdd = Image.open('./img/add.png')
        rawIcoAdd = rawIcoAdd.resize((20, 20), Image.Resampling.LANCZOS)
        icoAdd = ImageTk.PhotoImage(rawIcoAdd)

        self.controller.dshbrd.addBut1 = Button(
            self.controller.dshbrd,
            image = icoAdd,
            font = ('Chirp', 14),
            bg = 'white',
            border = '1px solid black'
        )
        self.controller.dshbrd.addBut1.bind("<Button-1>", renderInpPhieuThue)
        self.controller.dshbrd.addBut1.place(x=340, y=110)

        def temp1(e):
            global tabSel
            tabSel = [False] * 7
            tabSel[0] = True
            genRight('phieuThue', False)
            genBotBut('phieuThue')
            self.controller.dshbrd.refreshBut.bind("<Button-1>", temp1)
            self.controller.dshbrd.addBut1.bind("<Button-1>", renderInpPhieuThue)
            return

        def temp2(e): 
            global tabSel
            tabSel = [False] * 7
            tabSel[1] = True
            genRight('phieuThanhToan', False)
            genBotBut('phieuThanhToan')
            self.controller.dshbrd.refreshBut.bind("<Button-1>", temp2)
            self.controller.dshbrd.addBut1.bind("<Button-1>", renderInpPhieuThue)
        def temp3(e): 
            global tabSel
            tabSel = [False] * 7
            tabSel[2] = True
            genRight('ban', False)
            genBotBut('ban')
            self.controller.dshbrd.refreshBut.bind("<Button-1>", temp3)
            self.controller.dshbrd.addBut1.bind("<Button-1>", renderInpBan)
        def temp4(e): 
            global tabSel
            tabSel = [False] * 7
            tabSel[3] = True
            genRight('nhanVien', False)
            genBotBut('nhanVien')
            self.controller.dshbrd.refreshBut.bind("<Button-1>", temp4)
            self.controller.dshbrd.addBut1.bind("<Button-1>", renderInpNhanVien)
        def temp5(e): 
            global tabSel
            tabSel = [False] * 7
            tabSel[4] = True
            genRight('khachHang', False)
            genBotBut('khachHang')
            self.controller.dshbrd.refreshBut.bind("<Button-1>", temp5)
            self.controller.dshbrd.addBut1.bind("<Button-1>", renderInpKh)
        def temp6(e): 
            global tabSel
            tabSel = [False] * 7
            tabSel[5] = True
            genRight('dichVu', False)
            genBotBut('dichVu')
            self.controller.dshbrd.refreshBut.bind("<Button-1>", temp6)
            self.controller.dshbrd.addBut1.bind("<Button-1>", renderInpDv)

        def temp7(e): 
            global tabSel
            tabSel = [False] * 7
            tabSel[6] = True
            genRight('pNhapTbiAndFood', False)
            genBotBut('pNhapTbiAndFood')
            self.controller.dshbrd.refreshBut.bind("<Button-1>", temp7)
            self.controller.dshbrd.addBut1.bind("<Button-1>", renderInpProduct)
        def thongke():
            import matplotlib.pyplot as plt
            import numpy as np
            value = [20, 20]
            y = np.array(value)
            label = ['Phi', 'Minh']

            plt.pie(y, labels = label)
            plt.show() 

            # thongke.mainloop()
            return

        def temp8(e): 
            global tabSel
            tabSel = [False] * 7
            thongke()

        def bindMouseClick():
            self.controller.dshbrd.lblIcoBut1.bind("<Button-1>", temp1)
            self.controller.dshbrd.lbl1.bind("<Button-1>", temp1)
            self.controller.dshbrd.lblIcoImg1.bind("<Button-1>", temp1)

            self.controller.dshbrd.lblIcoBut2.bind("<Button-1>", temp2)
            self.controller.dshbrd.lbl2.bind("<Button-1>", temp2)
            self.controller.dshbrd.lblIcoImg2.bind("<Button-1>", temp2)

            self.controller.dshbrd.lblIcoBut3.bind("<Button-1>", temp3)
            self.controller.dshbrd.lbl3.bind("<Button-1>", temp3)
            self.controller.dshbrd.lblIcoImg3.bind("<Button-1>", temp3)
            
            self.controller.dshbrd.lblIcoBut4.bind("<Button-1>", temp4)
            self.controller.dshbrd.lbl4.bind("<Button-1>", temp4)
            self.controller.dshbrd.lblIcoImg4.bind("<Button-1>", temp4)

            self.controller.dshbrd.lblIcoBut5.bind("<Button-1>", temp5)
            self.controller.dshbrd.lbl5.bind("<Button-1>", temp5)
            self.controller.dshbrd.lblIcoImg5.bind("<Button-1>", temp5)

            self.controller.dshbrd.lblIcoBut6.bind("<Button-1>", temp6)
            self.controller.dshbrd.lbl6.bind("<Button-1>", temp6)
            self.controller.dshbrd.lblIcoImg6.bind("<Button-1>", temp6)

            self.controller.dshbrd.lblIcoBut7.bind("<Button-1>", temp7)
            self.controller.dshbrd.lbl7.bind("<Button-1>", temp7)
            self.controller.dshbrd.lblIcoImg7.bind("<Button-1>", temp7)

            self.controller.dshbrd.lblIcoBut8.bind("<Button-1>", temp8)
            self.controller.dshbrd.lbl8.bind("<Button-1>", temp8)
            self.controller.dshbrd.lblIcoImg8.bind("<Button-1>", temp8)

        bindMouseClick()

        def lblIcoButHovering():
            self.controller.dshbrd.lblIcoBut1.bind("<Enter>", mouEnBut1)
            self.controller.dshbrd.lblIcoBut1.bind("<Leave>", mouLeBut1)
            self.controller.dshbrd.lbl1.bind("<Enter>", mouEnBut1)
            self.controller.dshbrd.lbl1.bind("<Leave>", mouLeBut1)
            self.controller.dshbrd.lblIcoImg1.bind("<Enter>", mouEnBut1)
            self.controller.dshbrd.lblIcoImg1.bind("<Leave>", mouLeBut1)

            self.controller.dshbrd.lblIcoBut2.bind("<Enter>", mouEnBut2)
            self.controller.dshbrd.lblIcoBut2.bind("<Leave>", mouLeBut2)
            self.controller.dshbrd.lbl2.bind("<Enter>", mouEnBut2)
            self.controller.dshbrd.lbl2.bind("<Leave>", mouLeBut2)
            self.controller.dshbrd.lblIcoImg2.bind("<Enter>", mouEnBut2)
            self.controller.dshbrd.lblIcoImg2.bind("<Leave>", mouLeBut2)

            self.controller.dshbrd.lblIcoBut3.bind("<Enter>", mouEnBut3)
            self.controller.dshbrd.lblIcoBut3.bind("<Leave>", mouLeBut3)
            self.controller.dshbrd.lbl3.bind("<Enter>", mouEnBut3)
            self.controller.dshbrd.lbl3.bind("<Leave>", mouLeBut3)
            self.controller.dshbrd.lblIcoImg3.bind("<Enter>", mouEnBut3)
            self.controller.dshbrd.lblIcoImg3.bind("<Leave>", mouLeBut3)
            
            self.controller.dshbrd.lblIcoBut4.bind("<Enter>", mouEnBut4)
            self.controller.dshbrd.lblIcoBut4.bind("<Leave>", mouLeBut4)
            self.controller.dshbrd.lbl4.bind("<Enter>", mouEnBut4)
            self.controller.dshbrd.lbl4.bind("<Leave>", mouLeBut4)
            self.controller.dshbrd.lblIcoImg4.bind("<Enter>", mouEnBut4)
            self.controller.dshbrd.lblIcoImg4.bind("<Leave>", mouLeBut4)

            self.controller.dshbrd.lblIcoBut5.bind("<Enter>", mouEnBut5)
            self.controller.dshbrd.lblIcoBut5.bind("<Leave>", mouLeBut5)
            self.controller.dshbrd.lbl5.bind("<Enter>", mouEnBut5)
            self.controller.dshbrd.lbl5.bind("<Leave>", mouLeBut5)
            self.controller.dshbrd.lblIcoImg5.bind("<Enter>", mouEnBut5)
            self.controller.dshbrd.lblIcoImg5.bind("<Leave>", mouLeBut5)

            self.controller.dshbrd.lblIcoBut6.bind("<Enter>", mouEnBut6)
            self.controller.dshbrd.lblIcoBut6.bind("<Leave>", mouLeBut6)
            self.controller.dshbrd.lbl6.bind("<Enter>", mouEnBut6)
            self.controller.dshbrd.lbl6.bind("<Leave>", mouLeBut6)
            self.controller.dshbrd.lblIcoImg6.bind("<Enter>", mouEnBut6)
            self.controller.dshbrd.lblIcoImg6.bind("<Leave>", mouLeBut6)

            self.controller.dshbrd.lblIcoBut7.bind("<Enter>", mouEnBut7)
            self.controller.dshbrd.lblIcoBut7.bind("<Leave>", mouLeBut7)
            self.controller.dshbrd.lbl7.bind("<Enter>", mouEnBut7)
            self.controller.dshbrd.lbl7.bind("<Leave>", mouLeBut7)
            self.controller.dshbrd.lblIcoImg7.bind("<Enter>", mouEnBut7)
            self.controller.dshbrd.lblIcoImg7.bind("<Leave>", mouLeBut7)

            self.controller.dshbrd.lblIcoBut8.bind("<Enter>", mouEnBut8)
            self.controller.dshbrd.lblIcoBut8.bind("<Leave>", mouLeBut8)
            self.controller.dshbrd.lbl8.bind("<Enter>", mouEnBut8)
            self.controller.dshbrd.lbl8.bind("<Leave>", mouLeBut8)
            self.controller.dshbrd.lblIcoImg8.bind("<Enter>", mouEnBut8)
            self.controller.dshbrd.lblIcoImg8.bind("<Leave>", mouLeBut8)
        lblIcoButHovering()

class ViewRightDash():
    def __init__(self):
        pass
    pass