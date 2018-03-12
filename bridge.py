import glob
from classes import XS_t, points2Line
import codecs
path = r"E:\!!Modele_IsokII\Zlotna_161152\Geodezja\txt"

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
        #print(XS_base[num].type, print(XS_base[num].lp))
        x1, x2, y1, y2 = (XS_base[num].get_far())
        for pkt in XS_base[num].point_data:
            pkt.xp = (points2Line(x1,x2,y1,y2, pkt.x, pkt.y).yp)
            pkt.yp = (points2Line(x1, x2, y1, y2, pkt.x, pkt.y).xp)
        #print(XS_base[num].point_data[-1].xp)
        XS_base[num].distance()
        XS_base[num].get_culvert()
        #print(XS_base[num].point_data[-1].xp)
