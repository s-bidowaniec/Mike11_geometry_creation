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

# przypisanie przekroją wspolrzednych left i right oraz max z na krancach
for i in range(len(XS_dat)):
    XS_dat[i].kordy()
    if i == 0 or i == len(XS_dat)-1:
        XS_dat[i].len=XS_dat[i].km
    elif i > 0 and i < len(XS_dat):
        XS_dat[i].len = abs((XS_dat[i-1].km-XS_dat[i+1].km)/2)

# wykrycie polaczen przekroii od lewej do prawej, stworzenie listy obiektow typu link
linki = []
for object1 in XS_dat:
    lewa = object1.left
    for object2 in XS_dat:
        if abs(float(lewa[0]) - float(object2.right[0]))<10 and abs(float(lewa[1]) - float(object2.right[1]))<10 and object1.river_code != object2.river_code:
            linki.append(link(object1, object2))
licz_lin = len(linki)
defined = 0
#Nadanie parametrow przekroja
for element in linki:
    if "TZ_" not in element.river1 and "TZ_" in element.river2:
        #print(element.river1, element.chain1, element.river2, element.chain2)
        element.rzad = 1
        element.kolej = 1
        defined +=1
    elif "TZ_" in element.river1 and "TZ_" not in element.river2:
        element.rzad = 1
        element.kolej = 2
        defined += 1
    elif "TZ_" not in element.river1 and "TZ_" not in element.river2:
        #print(element.river1,element.chain1, element.river2, element.chain2)
        if element.object1.mean_left > element.object2.mean_right:
            element.rzad = 1
            element.kolej = 1
            defined += 1
        else:
            element.rzad = 1
            element.kolej = 2
            defined += 1
#print(len(linki))
#print(defined)
rzad = 1
safety = 0
while len(linki) > defined and safety < 10:
    for element in linki:
        if element.rzad == rzad:
            if element.kolej == 1:
                for element2 in linki:
                    if element.river2 == element2.river1 and element.chain2 == element2.chain1 and element2.rzad == 0:
                        element2.rzad = rzad+1
                        element2.kolej = 1
                        defined += 1
                        #print(element2.river1, element2.chain1, element2.river2, element2.chain2)
                    elif element.river2 == element2.river1 and element.chain2 == element2.chain1 and element2.rzad == rzad:

                        if element2.object1.mean_left > element2.object2.mean_right:
                            element2.rzad = rzad+1
                            element2.kolej = 1

                        else:
                            element2.rzad = rzad+1
                            element2.kolej = 2

            elif element.kolej == 2:
                for element2 in linki:
                    if element.river1 == element2.river2 and element.chain1 == element2.chain2 and element2.rzad == 0:
                        element2.rzad = rzad+1
                        element2.kolej = 2
                        defined += 1
                        #print(element2.river1, element2.chain1, element2.river2, element2.chain2)
                    elif element.river1 == element2.river2 and element.chain1 == element2.chain2 and element2.rzad == rzad:
                        if element2.object1.mean_left > element2.object2.mean_right:
                            element2.rzad = rzad+1
                            element2.kolej = 1

                        else:
                            element2.rzad = rzad+1
                            element2.kolej = 2

    rzad += 1
    safety += 1
    print(len(linki))
    print(defined)
for element in linki:
    # self.definitions = ["KP_"+str(self.main_chan)+"_"+str(self.main_km)+"_"+self.main_site, self.topo,0,5,0,10000,1]
    # musi dziedziczyc razem z rzedem, narazie tylko stale domyslne
    # main_chan, main_km, main_site ---- do nazewnictwa z cieku glownego
    # topo bezposrednio z cieku glownego
    element.data_definition()



print(len(XS_dat))
print(XS_dat)
print(XS_dat[1].left)
print(XS_dat[1].right)
print(XS_dat[1].max_left)
print(XS_dat[1].max_right)
print(XS_dat[1].len)
print(len(linki))
print(linki[0].definitions,"\n", linki[0].connections)
print(linki[0].points,"\n", linki[0].geometry)
print(linki[0].cross_section)


