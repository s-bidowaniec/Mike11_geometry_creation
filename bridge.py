import glob
from classes import XS_t

path = r"/home/ciurski/PycharmProjects/dane/rawxs/"

XS_txt = glob.glob(path+"*.txt")
XS_base = []
for XS_raw in XS_txt:
    with open(XS_raw, 'r') as f:
        XS_base.append(XS_t(f))
    f.close()
print(XS_base)