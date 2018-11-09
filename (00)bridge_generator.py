import glob
from classes import *
from functions import read_NWK
import xlsxwriter

PIETRZENIA = ["próg", "stopień", "jaz"]
MOSTY = ["przepust", "most", "kładka"]

path = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Geodezja\rzeka_CZARNY_POTOK_16632"
inputNwkDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v1\S01_Czarny_Potok.nwk11"
workbook = xlsxwriter.Workbook(r'C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v1\Czarny_Potok_budowle.xlsx')

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

    if XS_base[num].type in MOSTY:
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

    if XS_base[num].type in PIETRZENIA:
        x1, x2, y1, y2 = (XS_base[num].get_far())
        for pkt in XS_base[num].point_data:
            pkt.xp = (Points2Line(x1, x2, y1, y2, pkt.x, pkt.y).yp)
            pkt.yp = (Points2Line(x1, x2, y1, y2, pkt.x, pkt.y).xp)
        XS_base[num].distance()
        XS_base[num].get_weir()
        XS_base[num].get_km_bridge(nwk)
        XS_base[num].excel_print(workbook, path)
workbook.close()