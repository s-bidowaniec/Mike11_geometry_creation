# -*- coding: utf-8 -*-

############################################## SB ##########################################################
from functions import *
from classes import *
import multiprocessing
# plik wsadowy rawdata, pobierane sa punkty wspolne na przekrojach oraz inne dane do generacji linku
fileWejscieXS = open(r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v2_20.11\S01_Czarny_Potok_man.txt",'r')

# plik wsadowy nwk, pobierana jest lista punktow oraz branchy do ktorych dopisywane sa dane z nowych linkow
inputNwkDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v2_20.11\S01_Czarny_Potok.nwk11"

# nowy plik NWK z naniesionymi linkami
outputNwkDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v2_20.11\S01_Czarny_Potok_link.nwk11"
if inputNwkDir == outputNwkDir:
    raise 'Error: input == output'
# Otwarcie plikow
if inputNwkDir != outputNwkDir:
    fileWejscieNWK = open(inputNwkDir, 'r')
    fileWynik = open(outputNwkDir, "w")

XS_dat, XS_order = read_XSraw(fileWejscieXS)
print("Raw data zaczytane")
# minimalna roznica rzednych dla link channeli
minDeltaH = 0.51
""" czy ma zrobic redukcje pkt w branch (True, False) """
robicRDP = True
# ------------------------------------------------------------------------------------------------------------------- #
# przypisanie przekrojom wspolrzednych left i right oraz max z na krancach
list_km = []
for i in range(len(XS_dat)):
    XS_dat[i].kordy()
    for x in range(len(XS_dat)):
        if XS_dat[i].reachCode == XS_dat[x].reachCode and XS_dat[i].riverCode == XS_dat[x].riverCode:
            if float(XS_dat[x].km) not in list_km:
                list_km.append(float(XS_dat[x].km))
    list_km.sort()
    index = list_km.index(float(XS_dat[i].km))
    if index == 0:
        print("Tutaj jest blad jesli branch nie zaczyna sie od 0, nie rozwiazane")
        #import pdb
        #pdb.set_trace()
        XS_dat[i].len = int(abs(list_km[index] - (list_km[index + 1])))
    elif index >= len(list_km)-1:
        XS_dat[i].len = int(abs((list_km[index - 1] - list_km[index])) / 2)
    else: #if 0 < index < len(list_km) - 1:
        XS_dat[i].len = int(abs((list_km[index - 1] - list_km[index + 1]) / 2))
    if XS_dat[i].len == 0:
        XS_dat[i].len = 1
    list_km = []
# wykrycie polaczen przekroii od lewej do prawej, stworzenie listy obiektow typu link
linki = []
for object1 in XS_dat:
    lewa = object1.left
    for object2 in XS_dat:
        if len(lewa) < 2 or len(object2.right) < 2:
            continue
        if abs(float(lewa[0]) - float(object2.right[0])) < 2 and abs(
                float(lewa[1]) - float(object2.right[1])) < 2 and object1.riverCode != object2.riverCode:
            if "LTZ" in object1.riverCode and "PTZ" in object2.riverCode:
                print("blad: LTZ polaczony z PTZ")
            elif "PTZ" in object1.riverCode and "LTZ" in object2.riverCode:
                print("blad: PTZ polaczony z LTZ")
            else:
                linki.append(Link(object1, object2))
licz_lin = len(linki)
defined = 0
# Nadanie parametrow przekroja ----------------------------------------------------------------------------------------
# do refaktoryzacji - 4 krotne wywolanie tego samego
for element in linki:
    if "TZ_" not in element.river1 and "TZ_" in element.river2:
        #print(element.river1, element.chain1, element.river2, element.chain2)
        element.rzad = 1
        element.kolej = 1
        element.main_chan = str.upper(element.object1.riverCode[:3])
        # switch
        element.object1.len, element.object2.len = element.object2.len, element.object1.len
        element.main_km = element.object1.km
        element.topo = element.object1.reachCode
        defined += 1
    elif "TZ_" in element.river1 and "TZ_" not in element.river2:
        #print(element.river1, element.chain1, element.river2, element.chain2)
        element.rzad = 1
        element.kolej = 2
        element.main_chan = str.upper(element.object2.riverCode[:3])
        element.main_km = element.object2.km
        element.topo = element.object2.reachCode
        defined += 1
    elif "TZ_" not in element.river1 and "TZ_" not in element.river2:
        #print(element.river1,element.chain1, element.river2, element.chain2)
        if element.object1.mean_left > element.object2.mean_right:
            element.rzad = 1
            element.kolej = 1
            element.main_chan = str.upper(element.object1.riverCode[:3])
            #switch
            element.object1.len, element.object2.len = element.object2.len, element.object1.len
            element.main_km = element.object1.km
            element.topo = element.object1.reachCode
            defined += 1
        else:
            element.rzad = 1
            element.kolej = 2
            element.main_chan = str.upper(element.object2.riverCode[:3])
            element.main_km = element.object2.km
            element.topo = element.object2.reachCode
            defined += 1
# # # RZĄD i NAZWA ---------------------------------------------------------------------------------------------------
rzad = 1
safety = 0
while len(linki) > defined and safety < 10:
    # Przeniesc do funkcji i multiprocessingu
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
                    elif element.river2 == element2.river1 and element.chain2 == element2.chain1 and element2.rzad == rzad and element2.rzad != 1:
                        if element2.object1.mean_left > element2.object2.mean_right:
                            element2.rzad = rzad + 1
                            element2.kolej = 1
                            element2.main_chan = element.main_chan
                            element2.main_km = element.main_km
                            element2.topo = element.topo
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
                    elif element.river1 == element2.river2 and element.chain1 == element2.chain2 and element2.rzad == rzad and element2.rzad != 1:
                        if element2.object1.mean_left > element2.object2.mean_right:
                            element2.rzad = rzad + 1
                            element2.kolej = 1
                            element2.main_chan = element.main_chan
                            element2.main_km = element.main_km
                            element2.topo = element.topo
                        else:
                            element2.rzad = rzad + 1
                            element2.main_chan = element.main_chan
                            element2.main_km = element.main_km
                            element2.topo = element.topo
                            element2.kolej = 2
    rzad += 1
    safety += 1
# # # -----------------------------------------------------------------------------------------------------------------
# przejscie na multiprocessing

for element in linki:
    # self.definitions = ["KP_"+str(self.main_chan)+"_"+str(self.main_km)+"_"+self.main_site, self.topo,0,5,0,10000,1]
    # musi dziedziczyc razem z rzedem, narazie tylko stale domyslne
    # main_chan, main_km, main_site ---- do nazewnictwa z cieku glownego
    # topo bezposrednio z cieku glownego
    element.data_definition(minDeltaH)

#multiprocessing.Pool().map(lambda x: x.data_definition(minDeltaH), linki)

linki2 = []
for element in linki:
    if element.rzad != 0:
        linki2.append(element)

linki = linki2
#print(len(linki))

#print(printowanie(linki, 14923))
print('polaczenia link wykryte')



############################################## KP ##########################################################

nwk = read_NWK(fileWejscieNWK)
print("NWK zaczytane")


### iterowanie listy zawierającej klasy nowych link channeli
for i in linki:                         #   iterowanie listy zawierającej klasy nowych link channeli

    
    print("definiotnions", i.definitions)
    print("connections", i.connections)
    print("geometry", i.geometry)
    print("XS", i.cross_section)
    print("points", i.points)
    

    ## dodawanie parametów do klasy NwkFile
    newPoint1 = nwk.maxPoint+1                          #   numer nowego punktu
    newPoint2 = nwk.maxPoint+2
    nwk.pointList.append(NwkPoint(newPoint1, i.points[0], i.points[1], 1, 0, 0))        #   add point to list
    nwk.pointList.append(NwkPoint(newPoint2, i.points[2], i.points[3], 1, 5, 0))
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

### Drukowanie utworzonej struktury do pliku *.nwk
if robicRDP == True:
    nwk.nwk_rdp()
nwk.sort_points()
nwk.print_to_nwk(fileWynik)
fileWynik.close()

print("done")
