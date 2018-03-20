import glob
from classes import XS_t, points2Line
import xlsxwriter
import codecs


path = r"C:\Users\sbidowaniec\PycharmProjects\xlsx_XS_txt\Wynik"

XS_txt = glob.glob(path+"\*.txt")
XS_base = []
for XS_raw in XS_txt:
    #with codecs.open(XS_raw, 'r', encoding='cp1250', errors='ignore') as f:
    with open(XS_raw, 'r') as f:
        XS_base.append(XS_t(f))
    f.close()

#stworzenie pliku do zapisu danych o obiektach
workbook = xlsxwriter.Workbook('boru.xlsx')
for num in range(len(XS_base)):

    if "przepust" in XS_base[num].type or "most" in XS_base[num].type or "rurociąg" in XS_base[num].type:
        #sprowadzenie pkt na prosta
        x1, x2, y1, y2 = (XS_base[num].get_far())
        for pkt in XS_base[num].point_data:
            pkt.xp = (points2Line(x1,x2,y1,y2, pkt.x, pkt.y).yp)
            pkt.yp = (points2Line(x1, x2, y1, y2, pkt.x, pkt.y).xp)
        #pomiar odleglosci (station), i przypisanie pkt
        XS_base[num].distance()
        # przypisanie danych odpowiadajacych za culvert
        XS_base[num].get_culvert()
        XS_base[num].excel_print(workbook)
        #print(XS_base[num].point_data[-1].xp)
workbook.close()