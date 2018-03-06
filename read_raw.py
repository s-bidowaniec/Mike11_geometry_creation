import os
from classes_lib import XS, link
file = open(r'/home/ciurski/PycharmProjects/linik_gen/XS_Raw.txt','r')
lines = file.readlines()
row = 0
XSnum = 0
XS_dat = []
for line in lines:
    if row == 0:
        XS_dat.append(XS())
        XS_dat[XSnum].river_code = line
    elif row == 1:
        XS_dat[XSnum].reach_code = line
    elif row == 2:
        XS_dat[XSnum].km = float(line)
    elif row == 4:
        XS_dat[XSnum].cords = line
    elif row == 6:
        XS_dat[XSnum].fd = line
    elif row == 8:
        XS_dat[XSnum].pd = line
    elif row == 10:
        XS_dat[XSnum].datum = line
    elif row == 12:
        XS_dat[XSnum].rt = line
    elif row == 14:
        XS_dat[XSnum].dx = line
    elif row == 16:
        XS_dat[XSnum].id = line
    elif row == 18:
        XS_dat[XSnum].inter = line
    elif row == 20:
        XS_dat[XSnum].angle = line
    elif row == 22:
        XS_dat[XSnum].rn = line
    elif row == 23:
        XS_dat[XSnum].Profile = line
    elif row > 23 and 'LEVEL PARAMS' not in line and '*****' not in line:
        XS_dat[XSnum].dane.append(line)
        #print(line)
    elif 'LEVEL PARAMS' in line:
        row_num = row
        row=-100
    elif row == -100 and 'LEVEL PARAMS' not in line:
        XS_dat[XSnum].lp = line
        row=int(row_num)
    elif '*******************************' in line:

        row = -1
        XSnum += 1
    else:
        pass
    row +=1

# przypisacie left right kordynaty i max
for i in range(len(XS_dat)):
    XS_dat[i].kordy()
    if i == 0 or i == len(XS_dat)-1:
        XS_dat[i].len=XS_dat[i].km
    elif i > 0 and i < len(XS_dat):
        XS_dat[i].len = abs((XS_dat[i-1].km-XS_dat[i+1].km)/2)

linki = []
for object1 in XS_dat:
    lewa = object1.left
    for object2 in XS_dat:
        if abs(float(lewa[0]) - float(object2.right[0]))<10 and abs(float(lewa[1]) - float(object2.right[1]))<10:
            linki.append(link(object1, object2))


print(len(XS_dat))
print(XS_dat)
print(XS_dat[1].left)
print(XS_dat[1].right)
print(XS_dat[1].max_left)
print(XS_dat[1].max_right)
print(XS_dat[1].len)
print(len(linki))
print(linki[0].river1," ", linki[0].river2)