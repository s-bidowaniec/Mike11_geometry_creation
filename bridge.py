
import glob
from classes import XS_t
import codecs
path = r"/home/ciurski/PycharmProjects/dane/rawxs/"

XS_txt = glob.glob(path+"*.txt")
XS_base = []
for XS_raw in XS_txt:
    with codecs.open(XS_raw, 'r', encoding='cp1250', errors='ignore') as f:
        XS_base.append(XS_t(f))
    f.close()
print(XS_base[2].dane)
print(XS_base[2].point_data)