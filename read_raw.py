import os
from xs_class import XS
file = open(r'/home/asus/PycharmProjects/linki/linik_gen/MIKE2_uzup_raw.txt','r')
lines = file.readlines()
row = 0
XSnum = 0
XS_dat = []
for line in lines:
    if row == 0:
        XS_dat.append(XS())
        XS_dat[XSnum].RiverCode = line
    elif row == 1:
        XS_dat[XSnum].ReachCode = line
    elif row == 2:
        XS_dat[XSnum].KM = line
    elif row == 4:
        XS_dat[XSnum].cords = line
    elif row == 6:
        XS_dat[XSnum].FD = line
    elif row == 8:
        XS_dat[XSnum].PD = line
    elif row == 10:
        XS_dat[XSnum].DATUM = line
    elif row == 12:
        XS_dat[XSnum].RT = line
    elif row == 14:
        XS_dat[XSnum].DX = line
    elif row == 16:
        XS_dat[XSnum].ID = line
    elif row == 18:
        XS_dat[XSnum].INTER = line
    elif row == 20:
        XS_dat[XSnum].ANGLE = line
    elif row == 22:
        XS_dat[XSnum].RN = line
    elif row == 23:
        XS_dat[XSnum].Profile = line
    elif row > 23 and line != 'LEVEL PARAMS':
        XS_dat[XSnum].dane.append(line)
    elif line == 'LEVEL PARAMS':
        row='LP'
    elif row == 'LP':
        XS_dat[XSnum].LP = line
    elif '*******************************' in line:
        row = 0
        XSnum += 1
    row+=1
print(len(XS_dat))
print(XS_dat)

