import sqlite3

class Model():
    
    def __init__(self):
        self.dataPhieuThue = []
        self.phieuNhapTbAndFood = []
        self.dataDv = []
        self.dataNv = []
        self.dataKh = []
        self.dataPh = []

    def init_db(self):
        self.dataPhieuThue = [
            ['PDN0001', 'KH001', 'M001', 'P001', 'A101' , False, '20/10/2021'],
            ['PDN0002', 'KH002', 'M001', 'P002', 'A102', False, '30/01/2022'],
            ['PDN0003', 'KH001', 'M002', 'P003', 'A102', True, '18/06/2015'],
            ['PDN0004', 'KH003', 'M002', 'P008', 'B202', False, '08/01/2016'],
            ['PDN0005', 'KH004', 'M002', 'P008', 'B202', True, '08/01/2018'],
            ['PDN0006', 'KH006', 'M001', 'P004', 'B202', False, '08/01/2019']
        ]
        self.phieuNhapTbAndFood = [
            ['P001', 'Cà phê đen đá Robusta M', 12000, 'Yes'],
            ['P002', 'Cà phê đen đá Robusta L', 15000, 'Yes'],
            ['P003', 'Cappuccino không trang trí', 25000, 'Yes'],
            ['P004', 'Cappuccino có trang trí', 30000, 'Yes'],
            ['P005', 'Macchiato M', 23000, 'Yes'],
            ['P006', 'Macchiato L', 28000, 'Yes'],
            ['P007', 'Trà tắc', 8000, 'Yes'],
            ['P008', 'Mocha', 13000, 'No'],
            ['P009', 'Americano', 17000, 'Yes'],
            ['P009', 'Espresso', 21000, 'Yes'],
            ['P010', 'Cà phê đen đá Arabica M', 17000, 'Yes'],
            ['P011', 'Cà phê đen đá Arabica L', 20000, 'Yes']
            
        ]
        self.dataDv = [
            ['DV001', '2 bánh', 2000],
            ['DV002', '4 bánh', 10000]
        ]
        self.dataNv = [
            ['B001', 'Trịnh Quang', 'Hòa', 'Nam', 1979, 'TP.HCM', 'CEO', 'Hội đồng quản trị', 99999999, 99999999],
            ['B002', 'Kim Đức', 'Long', 'Nam', 1983, 'Quảng Nam', 'CTO', 'Hội đồng quản trị', 99999999, 99999999],
            ['B003', 'Huỳnh Nguyên', 'Khang', 'Nam', 1982, 'Bình Phước', 'CFO', 'Hội đồng quản trị', 99999999, 99999999],
            ['G001', 'Hoàng Hòa', 'Hợp', 'Nam', 1982, 'Bình Thuận', 'Nhân viên', 'Bảo vệ', 5000000, 800000],
            ['G002', 'Lưu Duy', 'Hiếu', 'Nam', 1991, 'Long An', 'Nhân viên', 'Bảo vệ', 5000000, 800000],
            ['G003', 'Hồ Văn', 'Thông', 'Nam', 1998, 'Gia Lai', 'Trưởng phòng', 'Bảo vệ', 6000000, 1000000],
            ['G004', 'Nguyễn Văn', 'Sinh', 'Nam', 1991, 'TP.HCM', 'Nhân viên', 'Bảo vệ', 5000000, 600000],
            ['E001', 'Châu Văn', 'Đạt', 'Nam', 1998, 'Quảng Nam', 'Trưởng phòng', 'Kế toán', 8000000, 600000],
            ['E002', 'Nguyễn Thị', 'Nga', 'Nữ', 1991, 'Long An', 'Nhân viên', 'Kế toán', 7000000, 600000],
            ['E003', 'Vũ Việt', 'Đông', 'Nam', 1982, 'Tiền Giang', 'Nhân viên', 'Kế toán', 7000000, 600000],
            ['C001', 'Đào Ngọc', 'Cẩm', 'Nữ', 1992, 'Bình Dương', 'Nhân viên', 'Vệ sinh', 4000000, 600000],
            ['C002', 'Huỳnh Thụy Phương', 'Khánh', 'Nữ', 1996, 'TP.HCM', 'Nhân viên', 'Vệ sinh', 4000000, 600000],
            ['F001', 'Nguyễn Văn Gia', 'Trí', 'Nam', 1992, 'Tiền Giang', 'Trưởng phòng', 'Quản trị nhân sự', 6000000, 600000],
            ['F002', 'Lưu Ngọc Hoài ', 'Trinh', 'Nữ', 1992, 'Bình Dương', 'Nhân viên', 'Quản trị nhân sự', 6000000, 600000],
            ['Z001', 'Đoàn Trần Văn ', 'Kha', 'Nam', 1996, 'Long An', 'Bếp trưởng', 'Bếp ăn', 4000000, 600000],
            ['Z002', 'David ', 'Joe', 'Nam', 1998, 'TP.HCM', 'Đầu bếp', 'Bếp ăn', 8700000, 900000],
            ['Z003', 'Phạm Toàn ', 'Thắng', 'Nam', 1998, 'TP.HCM', 'Đầu bếp', 'Bếp ăn', 4000000, 600000],
            ['M001', 'Phạm Quốc ', 'Khải', 'Nam', 1996, 'Tiền Giang', 'Tiếp tân', 'Lễ tân', 3000000, 600000],
            ['M002', 'Nguyễn Võ ', 'Lợi', 'Nam', 2000, 'Gia Lai', 'Tiếp tân', 'Lễ tân', 3000000, 600000],
            ['T001', 'Lưu Bích ', 'Thoa', 'Nữ', 1992, 'Quảng Nam', 'Nhân viên', 'massage', 7000000, 600000],
            ['T002', 'Trần Thục ', 'Quyên', 'Nữ', 2000, 'Tây Ninh', 'Nhân viên', 'massage', 7000000, 600000],
            ['K001', 'Hứa Vĩnh ', 'Đức', 'Nam', 1990, 'Bến Tre', 'Nhân viên', 'Kho vận', 7000000, 600000],
            ['K002', 'Trần Phùng ', 'Thọ', 'Nam', 1998, 'TP.HCM', 'Nhân viên', 'Kho vận', 7000000, 600000]
        ]
        self.dataPh = [
            ['A101', '2 người', 'available', 'Tầng trệt','Tròn', "Bình hoa hồng"],
            ['A102', '2 người', 'available', 'Tầng 1','Tròn', "Đèn Manchon"],
            ['B202', '2 người', 'available', 'Tầng 2','Vuông', "Bình hoa tulips"],
            ['B201', '3 người', 'available', 'Tầng 3','Vuông', "Guitar"],
            ['C301', '5 người', 'available', 'Tầng 2','Tròn', "Tivi"],
            ['C303', '8 người', 'occupied', 'Tầng trệt','Tròn',"Giá sách"],
            ['A103', '8 người', 'occupied', 'Tầng 2','Vuông', "Loa karaoke"]
        ]
        self.dataKh = [
            ['KH001', 'Nguyễn Thế', 'Doanh', 'Nam', 1983, '2 bánh'],
            ['KH002', 'Úc Quốc', 'Hải', 'Nam', 1982, '4 bánh'],
            ['KH003', 'Nguyễn Thiện', 'Ân', 'Nam', 1979, '4 bánh'],
            ['KH004', 'Vương Đăng', 'Đạt', 'Nam', 1982, '4 bánh'],
            ['KH005', 'Trang Diệu', 'Nương', 'Nữ', 1991, '4 bánh'],
            ['KH006', 'Nguyễn Chiêu', 'Dương', 'Nữ', 1998, '4 bánh'],
            ['KH007', 'Bùi Thúy', 'Vy', 'Nam', 1991,'4 bánh']
        ]
    def getDataPhieuThue(self):
        return self.dataPhieuThue
    def getDataNv(self):
        return self.dataNv
    def getDataKh(self):
        return self.dataKh
    def getDataDv(self):
        return self.dataDv
    def getDataPhieuNhapTbAndFood(self):
        return self.phieuNhapTbAndFood
    def getDataPh(self):
        return self.dataPh