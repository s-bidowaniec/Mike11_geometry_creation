from classes import raport_XS, XS, Link, printowanie
import xlsxwriter
file = open(r'E:\!!Modele_IsokII\Zlotna_161152\Mike\V0\link_gen_test_xns.txt', 'r')


#file = open(r'link_gen_test_xns.txt','r')

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
    elif 'COORDINATES' in old:
        XS_dat[XSnum].cords = line
    elif 'FLOW DIRECTION' in old:
        XS_dat[XSnum].fd = line #flow direction
    elif 'PROTECT DATA' in old:
        XS_dat[XSnum].pd = line #protect data
    elif 'DATUM' in old:
        XS_dat[XSnum].datum = line #datum
    elif 'CLOSED SECTION' in old:
        XS_dat[XSnum].cs = line #closed
    elif 'RADIUS TYPE' in old:
        XS_dat[XSnum].rt = line # radius type
    elif 'DIVIDE X-Section' in old:
        XS_dat[XSnum].dx = line # divide xs
    elif 'SECTION ID' in old:
        XS_dat[XSnum].id = str(line).replace(" ","") # section id
    elif 'INTERPOLATED' in old:
        XS_dat[XSnum].inter = line # interpolated
    elif 'ANGLE' in old:
        XS_dat[XSnum].angle = line # angle
    elif 'RESISTANCE NUMBERS' in old:
        XS_dat[XSnum].rn = line # resistance number
    elif 'PROFILE        25' in old:
        XS_dat[XSnum].Profile = str(line).split()[-1] # profile
    elif sum(c.isdigit() for c in line) > 13 and row > 5:
        XS_dat[XSnum].dane.append(line)
    elif 'LEVEL PARAMS' in line:
        row_num = row
        row = -100
    elif row == -100 and 'LEVEL PARAMS' not in line:
        XS_dat[XSnum].lp = line # level params
        row = int(row_num)
    elif '**' in line:
        row = -1
        XSnum += 1
    else:
        pass
    row += 1
    old = line
# przypisanie przekroją wspolrzednych left i right oraz max z na krancach
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

raport_XS(XS_dat)
print(len(linki))

print(printowanie(linki, 12374))
