# -*- coding: utf-8 -*-

############################################## SB ##########################################################

from classes import XS, Link, printowanie

#file = open("D:\Skrypty\Mike_NWK\linik_gen\link_gen_test_xns.txt", 'r')

import os
#from classes import XS, link, printowanie
file = open(r"D:\Skrypty\Mike_NWK\Dane_przykladowe\Krynka_v2_raw.txt",'r')

lines = file.readlines()
row = 0
XSnum = 0
XS_dat = []
for line in lines:
    if row == 0:
        if '**' in line:
            row = -1
        else:
            XS_dat.append(XS())
            XS_dat[XSnum].reach_code = line.replace("\n", "")
    elif row == 1:
        XS_dat[XSnum].river_code = line.replace("\n", "")
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
        # print(line)
    elif 'LEVEL PARAMS' in line:
        row_num = row
        row = -100
    elif row == -100 and 'LEVEL PARAMS' not in line:
        XS_dat[XSnum].lp = line
        row = int(row_num)
    elif '**' in line:
        row = -1
        XSnum += 1
    else:
        pass
    row += 1

# przypisanie przekrojom wspolrzednych left i right oraz max z na krancach
list_km = []
for i in range(len(XS_dat)):
    XS_dat[i].kordy()
    for x in range(len(XS_dat)):
        if XS_dat[i].reach_code == XS_dat[x].reach_code and XS_dat[i].river_code == XS_dat[x].river_code:
            if float(XS_dat[x].km) not in list_km:
                list_km.append(float(XS_dat[x].km))
    list_km.sort()
    index = list_km.index(float(XS_dat[i].km))
    if index == 0:
        XS_dat[i].len = int(abs(list_km[index] / 2 + (list_km[index] - list_km[index + 1]) / 2))
    elif index >= len(list_km) - 1:
        XS_dat[i].len = int(abs((list_km[index - 1] - list_km[index])) / 2)
    elif 0 < index < len(list_km) - 1:
        XS_dat[i].len = int(abs((list_km[index - 1] - list_km[index + 1]) / 2))
    if XS_dat[i].len == 0:
        XS_dat[i].len = 1
    list_km = []
# wykrycie polaczen przekroii od lewej do prawej, stworzenie listy obiektow typu link
linki = []
for object1 in XS_dat:
    lewa = object1.left
    for object2 in XS_dat:
        if abs(float(lewa[0]) - float(object2.right[0])) < 2 and abs(
                float(lewa[1]) - float(object2.right[1])) < 2 and object1.river_code != object2.river_code:
            if "LTZ" in object1.river_code and "PTZ" in object2.river_code:
                print("blad: LTZ polaczony z PTZ")
            elif "PTZ" in object1.river_code and "LTZ" in object2.river_code:
                print("blad: PTZ polaczony z LTZ")
            else:
                linki.append(Link(object1, object2))
licz_lin = len(linki)
defined = 0
# Nadanie parametrow przekroja
# do refaktoryzacji - 4 krotne wywolanie tego samego
for element in linki:
    if "TZ_" not in element.river1 and "TZ_" in element.river2:
        # print(element.river1, element.chain1, element.river2, element.chain2)
        element.rzad = 1
        element.kolej = 1
        element.main_chan = str.upper(element.object1.river_code[:3])
        element.main_km = element.object1.km
        element.topo = element.object1.reach_code
        defined += 1
    elif "TZ_" in element.river1 and "TZ_" not in element.river2:
        element.rzad = 1
        element.kolej = 2
        element.main_chan = str.upper(element.object2.river_code[:3])
        element.main_km = element.object2.km
        element.topo = element.object2.reach_code
        defined += 1
    elif "TZ_" not in element.river1 and "TZ_" not in element.river2:
        # print(element.river1,element.chain1, element.river2, element.chain2)
        if element.object1.mean_left > element.object2.mean_right:
            element.rzad = 1
            element.kolej = 1
            element.main_chan = str.upper(element.object1.river_code[:3])
            element.main_km = element.object1.km
            element.topo = element.object1.reach_code
            defined += 1
        else:
            element.rzad = 1
            element.kolej = 2
            element.main_chan = str.upper(element.object2.river_code[:3])
            element.main_km = element.object2.km
            element.topo = element.object2.reach_code
            defined += 1

rzad = 1
safety = 0
while len(linki) > defined and safety < 10:
    for element in linki:
        if element.rzad == rzad:
            if element.kolej == 1:
                for element2 in linki:
                    if element.river2 == element2.river1 and element.chain2 == element2.chain1 and element2.rzad == 0:
                        element2.rzad = rzad + 1
                        element2.kolej = 1
                        element2.main_chan = element.main_chan
                        element2.main_km = element.main_km
                        element2.topo = element.topo
                        defined += 1
                        # print(element2.river1, element2.chain1, element2.river2, element2.chain2)
                    elif element.river2 == element2.river1 and \
                            element.chain2 == element2.chain1 and element2.rzad == rzad:
                        if element2.object1.mean_left > element2.object2.mean_right:
                            element2.rzad = rzad + 1
                            element2.kolej = 1
                        else:
                            element2.rzad = rzad + 1
                            element2.kolej = 2
                            element2.main_chan = element.main_chan
                            element2.main_km = element.main_km
                            element2.topo = element.topo

            elif element.kolej == 2:
                for element2 in linki:
                    if element.river1 == element2.river2 and element.chain1 == element2.chain2 and element2.rzad == 0:
                        element2.rzad = rzad + 1
                        element2.kolej = 2
                        element2.main_chan = element.main_chan
                        element2.main_km = element.main_km
                        element2.topo = element.topo
                        defined += 1
                        # print(element2.river1, element2.chain1, element2.river2, element2.chain2)
                    elif element.river1 == element2.river2 and \
                            element.chain1 == element2.chain2 and element2.rzad == rzad:
                        if element2.object1.mean_left > element2.object2.mean_right:
                            element2.rzad = rzad + 1
                            element2.kolej = 1
                        else:
                            element2.rzad = rzad + 1
                            element2.main_chan = element.main_chan
                            element2.main_km = element.main_km
                            element2.topo = element.topo
                            element2.kolej = 2

    rzad += 1
    safety += 1

for element in linki:
    # self.definitions = ["KP_"+str(self.main_chan)+"_"+str(self.main_km)+"_"+self.main_site, self.topo,0,5,0,10000,1]
    # musi dziedziczyc razem z rzedem, narazie tylko stale domyslne
    # main_chan, main_km, main_site ---- do nazewnictwa z cieku glownego
    # topo bezposrednio z cieku glownego
    element.data_definition()

#print(len(linki))

#print(printowanie(linki, 14923))

print("Raw data zaczytane")


############################################## KP ##########################################################


from NWK_reader_classes import *


def line_to_list(line):
    name = line.split()[0]
    line2 = line.replace(" =", ",")
    line2 = line2.replace("'", "")
    line2 = line2.replace("\n", "")
    data_list = line2.split(", ")
    for i in range(len(data_list)):
        try:
            if "." in data_list[i]:
                data_list[i] = float(data_list[i])
            else:
                data_list[i] = int(data_list[i])
        except:
            pass

    return data_list, name


file = open("D:\\Skrypty\\Mike_NWK\\Dane_przykladowe\\Krynka_v2.nwk11", 'r')
readline = file.readlines()

nwk = NwkFile()
i = 0

# zaczytywanie początku pliku
while i < len(readline) and "POINTS" not in readline[i]:
    nwk.add_start(readline[i])
    i += 1
i += 1

# zaczytywanie punktów do klasy nwkFile
while i < len(readline) and "EndSect  // POINTS" not in readline[i]:
    line = readline[i]
    stringList, name = line_to_list(line)
    nwk.add_point(stringList, name)
    i += 1

# przejście do pierwszego "brancha"
while "[branch]" not in readline[i]:
    i += 1

# zaczytywanie poszczególnych klas
while i < len(readline) and "EndSect  // CULVERTS" not in readline[i]:
    line = readline[i]

    if not line.split():
        i += 1
        continue

    data_list, name = line_to_list(line)

    if "[branch]" in line:
        nwk.branchList.append(Branch())
        cl = nwk.branchList[-1]

    elif "[linkchannel]" in line:
        cl.linkChannel = LinkChannel(cl)
        cl = cl.linkChannel

    elif "[Cross_Section]" in line:
        cl.crossSection = CrossSection(cl)
        cl = cl.crossSection

    elif "[weir_data]" in line:
        nwk.weirList.append(Weir())
        cl = nwk.weirList[-1]
        wr = True

    elif "[ReservoirData]" in line:
        cl.reservoir = ReservoirData(cl)
        cl = cl.reservoir

    elif "[Elevation]" in line:
        cl.elevation = Elevation(cl)
        cl = cl.elevation

    elif "[Geometry]" in line:
        cl.geometry = Geometry(cl)
        cl = cl.geometry

    elif "[Level_Width]" in line:
        cl.levelWidth = LevelWidth(cl)
        cl = cl.levelWidth

    elif "[culvert_data]" in line:
        nwk.culvertList.append(Culvert())
        cl = nwk.culvertList[-1]
        cr = True

    elif "[Irregular]" in line:
        cl.irregular = Irregular(cl)
        cl = cl.irregular

    elif cl.end in line and cl.parent is None:
        i += 1
        continue

    elif cl.end in line:
        cl = cl.parent

    else:
        cl.add_parameters(data_list, name, line)
    i += 1

while i < len(readline):
    nwk.finish = nwk.finish + readline[i]
    i += 1

print("NWK zaczytane")


### iterowanie listy zawierającej klasy nowych link channeli
for i in linki:                         #   iterowanie listy zawierającej klasy nowych link channeli

    '''
    print("definiotnions", i.definitions)
    print("connections", i.connections)
    print("geometry", i.geometry)
    print("XS", i.cross_section)
    print("points", i.points)
    '''

    ## dodawanie parametów do klasy NwkFile
    newPoint1 = nwk.maxPoint+1                          #   numer nowego punktu
    newPoint2 = nwk.maxPoint+2
    nwk.pointList.append(NwkPoint(newPoint1, i.points[0], i.points[1], 0, 0, 0))        #   add point to list
    nwk.pointList.append(NwkPoint(newPoint2, i.points[2], i.points[3], 0, 0, 0))
    nwk.maxPoint += 2

    ## dodawanie parametów do klasy branch
    nwk.branchList.append(Branch(nwk))
    cl = nwk.branchList[-1]
    cl.riverName, cl.topoID, cl.val1, cl.val2, cl.val3, cl.val4, cl.val5 = tuple(i.definitions)
    cl.connectRiver, cl.point, cl.connectTopoID, cl.point2 = tuple(i.connections)
    cl.pointList.extend([newPoint1, newPoint2])

    ## dodawanie parametów do klasy LinkChannel
    cl.linkChannel = LinkChannel(cl)
    cl = cl.linkChannel
    cl.geometry = i.geometry[:]
    cl.geometry.append(0)
    cl.HeadLossFactors = [0.5, 1, 0, 1, 0.5, 1, 0, 1]
    cl.BedResistance = [1, 0.04]

    ## dodawanie parametrów do klasy CrossSection
    cl.crossSection = CrossSection(cl)
    cl = cl.crossSection
    cl.data.extend(i.cross_section)

nwk.nwk_rdp()

### Drukowanie utworzonej struktury do pliku *.nwk
file = open("wyniki_NWK.nwk11", "w")
nwk.print_to_nwk(file)
file.close()

print("done")
