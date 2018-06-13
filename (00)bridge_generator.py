import glob
from classes import *
#from functions import *
import xlsxwriter

path = r"K:\Wymiana danych\Staszek\KORN\budowle"

XS_txt = glob.glob(path+"\*.txt")
XS_base = []
for XS_raw in XS_txt:
    # with codecs.open(XS_raw, 'r', encoding='cp1250', errors='ignore') as f:
    with open(XS_raw, 'r') as f:
        XS_base.append(XS_t(f))
    f.close()

# stworzenie pliku do zapisu danych o obiektach
workbook = xlsxwriter.Workbook(r'K:\Wymiana danych\Staszek\KORN\budowle\Swidnik_budowle.xlsx')
for num in range(len(XS_base)):

    if "przekrój" in XS_base[num].type or "most" in XS_base[num].type or "cc" in XS_base[num].type:
        # sprowadzenie pkt na prosta
        x1, x2, y1, y2 = (XS_base[num].get_far())
        for pkt in XS_base[num].point_data:
            pkt.xp = (Points2Line(x1,x2,y1,y2, pkt.x, pkt.y).yp)
            pkt.yp = (Points2Line(x1, x2, y1, y2, pkt.x, pkt.y).xp)
        # pomiar odleglosci (station), i przypisanie pkt
        XS_base[num].distance()
        # przypisanie danych odpowiadajacych za culvert
        XS_base[num].get_culvert()
        XS_base[num].excel_print(workbook)
        # print(XS_base[num].point_data[-1].xp)
workbook.close()