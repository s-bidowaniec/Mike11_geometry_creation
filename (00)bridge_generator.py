import glob
from classes import *
from functions import read_NWK
import xlsxwriter

path = r"K:\Wymiana danych\Staszek\Ymitr\DLUGI_POTOK"
inputNwkDir = r"K:\Wymiana danych\Staszek\Ymitr\DLUGI_POTOK\S01_DLUGI_POTOK.nwk11"
workbook = xlsxwriter.Workbook(r'K:\Wymiana danych\Staszek\Ymitr\DLUGI_POTOK\Dlugi_potok_budowle.xlsx')

fileWejscieNWK = open(inputNwkDir, 'r')
nwk = read_NWK(fileWejscieNWK)
print("NWK zaczytane")
XS_txt = glob.glob(path+"\mosty_out"+"\*.txt")
XS_base = []
for XS_raw in XS_txt:
    # with codecs.open(XS_raw, 'r', encoding='cp1250', errors='ignore') as f:
    with open(XS_raw, 'r') as f:
        XS_base.append(XS_t(f))
    f.close()
XS_base.sort(key=lambda x: float(x.lp))
# stworzenie pliku do zapisu danych o obiektach

for num in range(len(XS_base)):

    if "przepust" in XS_base[num].type or "most" in XS_base[num].type or "kładka" in XS_base[num].type:
        # sprowadzenie pkt na prosta
        x1, x2, y1, y2 = (XS_base[num].get_far())
        for pkt in XS_base[num].point_data:
            pkt.xp = (Points2Line(x1,x2,y1,y2, pkt.x, pkt.y).yp)
            pkt.yp = (Points2Line(x1, x2, y1, y2, pkt.x, pkt.y).xp)
        # pomiar odleglosci (station), i przypisanie pkt
        XS_base[num].distance()
        # przypisanie danych odpowiadajacych za culvert
        XS_base[num].get_culvert()
        XS_base[num].get_culver_len()
        XS_base[num].get_km_bridge(nwk)
        XS_base[num].excel_print(workbook, path)
        # print(XS_base[num].point_data[-1].xp)
workbook.close()