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
        XS_dat[XSnum].KM = float(line)
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
    elif row > 23 and 'LEVEL PARAMS' not in line and '*****' not in line:
        XS_dat[XSnum].dane.append(line)
        #print(line)
    elif 'LEVEL PARAMS' in line:
        row_num = row
        row=-100
    elif row == -100 and 'LEVEL PARAMS' not in line:
        XS_dat[XSnum].LP = line
        row=int(row_num)
    elif '*******************************' in line:

        row = -1
        XSnum += 1
    else:
        pass
    row +=1

for object in XS_dat:
    object.kordy()
    #print(object.KM)

for i in range(len(XS_dat)):
    print(i)
    if i == 0 or i == len(XS_dat)-1:
        XS_dat[i].len=XS_dat[i].KM

    elif i > 0 and i < len(XS_dat):
        XS_dat[i].len = abs((XS_dat[i-1].KM-XS_dat[i+1].KM)/2)

linki = []
for object in XS_dat:
    lewa = object.Left
    prawa = object.Right
    for object in XS_dat:
        if lewa == object.Right:
            linki.append(object.KM)
        if prawa == object.Left:
            linki.append(object.KM)

print(len(XS_dat))
print(XS_dat)
print(XS_dat[1].Left)
print(XS_dat[1].Right)
print(XS_dat[1].MaxLeft)
print(XS_dat[1].MaxRight)
print(XS_dat[1].len)
print(linki)
