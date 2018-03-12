import codecs

import glob

from classes import XSt, Points2Line

path = r"/home/ciurski/PycharmProjects/dane/rawxs/"

XS_txt = glob.glob(path + "*.txt")
XS_base = []
for XS_raw in XS_txt:
    with codecs.open(XS_raw, 'r', encoding='cp1250', errors='ignore') as f:
        # with open(XS_raw, 'r') as f:
        XS_base.append(XSt(f))

path = r"E:\!!Modele_IsokII\Pielgrzymowka_11468\Geodezja\txt"

XS_txt = glob.glob(path+"\*.txt")
XS_base = []
for XS_raw in XS_txt:
    #with codecs.open(XS_raw, 'r', encoding='cp1250', errors='ignore') as f:
    with open(XS_raw, 'r') as f:
        XS_base.append(XS_t(f))

    f.close()

print(len(XS_base))
for num in range(len(XS_base)):

    if "most" in XS_base[num].type:
        print(XS_base[num].type, print(XS_base[num].lp))
        x1, x2, y1, y2 = (XS_base[num].get_far())
        for pkt in XS_base[num].point_data:
            pkt.xp = Points2Line(x1, x2, y1, y2, pkt.x, pkt.y).yp
            pkt.yp = Points2Line(x1, x2, y1, y2, pkt.x, pkt.y).xp
        print(XS_base[num].point_data[-1].xp)
        XS_base[num].distance()
        XS_base[num].get_culvert()
        print(XS_base[num].point_data[-1].xp)
