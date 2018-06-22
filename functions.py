import numpy as np
import collections
import xlsxwriter
from classes import *
from dbfread import DBF
# UNIVERSAl -----------------------------------------------------------------------------------------------------------

def get_xy_delta(self):
    if self.right[0] > self.left[0]:
        x1, x2 = 2, -2
    elif self.right[0] < self.left[0]:
        x1, x2 = -2, 2
    else:
        x1, x2 = 0, 0
    if self.right[1] > self.left[1]:
        y1, y2 = 2, -2
    elif self.right[1] < self.left[1]:
        y1, y2 = -2, 2
    else:
        y1, y2 = 0, 0

    deltaX = (x1-x2)/4
    deltaY = (y1-y2)/4


    return x1+deltaY, y1-deltaX, x2+deltaY, y2-deltaX
# LINKI ---------------------------------------------------------------------------------------------------------------
# drukuje link do pliku nwk
def printowanie(list_lin, num):
    point_list = []
    f = open('branche.txt', 'w')
    f.write("   [POINTS]\n")
    for element in list_lin:
        point1 = str(element.points[0:2])
        elem = [num + 1, point1]
        point_list.append(elem)
        f.write("      point = " + str(elem).replace("[", "").replace("]", "").replace("'", "") + ", 1, 0.00, 0" + "\n")
        point2 = str(element.points[2:4])
        elem2 = [num + 2, point2]
        point_list.append(elem2)
        f.write(
            "      point = " + str(elem2).replace("[", "").replace("]", "").replace("'", "") + ", 1, 5.00, 0" + "\n")
        num += 2
        element.points2 = [num - 1, num]
    f.write("-------------\n\n")
    for element in list_lin:
        f.write("      [branch]\n")
        f.write("         definitions = " + str(element.definitions).replace("[", "").replace("]", "") + "\n")
        f.write("         connections = " + str(element.connections).replace("[", "").replace("]", "") + "\n")
        f.write("         points = " + str(element.points2).replace("[", "").replace("]", "") + "\n")
        f.write("         [linkchannel]\n")
        f.write("            Geometry = " + str(element.geometry).replace("[", "").replace("]", "") + ", 0\n")
        f.write("            HeadLossFactors = 0.5, 1, 0, 1, 0.5, 1, 0, 1\n")
        f.write("            Bed_Resistance = 1, 0.03\n")
        f.write("            [Cross_Section]\n")
        for data in element.cross_section:
            f.write("               Data = " + str(data).replace("[", "").replace("]", "") + "\n")
        f.write("            EndSect  // Cross_Section\n\n")
        f.write("         EndSect  // linkchannel\n\n")
        f.write("      EndSect  // branch\n\n")
    return point_list

# XS rawdata functions ------------------------------------------------------------------------------------------------
def read_XSraw(file):
    lines = file.readlines()
    row = 0
    XSnum = 0
    XS_dat = []
    XsOrder = collections.OrderedDict()
    for line in lines:
        if len(line) > 2:
            if row == 0:
                if '**' in line:
                    row = -1
                else:

                    XS_dat.append(Xs())
                    XS_dat[XSnum].reachCode = line.replace("\n", "")
            elif row == 1:
                XS_dat[XSnum].riverCode = line.replace("\n", "")
                river = line.replace("\n", "")
            elif row == 2:
                XS_dat[XSnum].km = float(line)
                km = float(line)
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
            elif 'PROFILE' in line:
                XS_dat[XSnum].profile = str(line).split()[-1] # profile
            elif sum(c.isdigit() for c in line) > 12 and row > 5:
                XS_dat[XSnum].points.append(Pkt(line))
            elif 'LEVEL PARAMS' in line:
                row_num = row
                row = -100
            elif row == -99 and 'LEVEL PARAMS' not in line:
                XS_dat[XSnum].lp = line # level params
                row = int(row_num)
            elif '**' in line:
                row = -1
                XSnum += 1
                XsOrder['{} {}'.format(str.lower(river).replace(' ', ''), km)] = XS_dat[XSnum-1]
            else:
                pass
            row += 1
            old = line

    return XS_dat, XsOrder
def read_manning_dbf(dbf):
    base = {}
    for record in DBF(dbf):
        kod = '{} {} {}'.format(str(record['RiverCode']).title(), record['ReachCode'], round(float("{0:.1f}".format(record['ProfileM'])),0))
        if kod in base.keys():
            base[kod].dodaj(record)
        else:
            base[kod] = ManningXS(record)
    return base
def raport_XS(XS_list, output):
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('raport_XS')
    bold = workbook.add_format({'bold': 1})
    headings = ['Nazwa rzeki', 'Topo ID', 'Kilometraż', 'ID Przekroju', 'Typ przekroju']  # 'Radius Type', 'Datum'
    worksheet.write_row('A1', headings, bold)
    i = 1
    for XS in XS_list:
        worksheet.write(i, 0, XS.riverCode)  # row col
        worksheet.write(i, 1, XS.reachCode)
        worksheet.write(i, 2, XS.km)

        if len(XS.id) > 2:
            worksheet.write(i, 3, XS.id)
        else:
            worksheet.write(i, 3, 'Pomiar geodezyjny')
        if XS.cs == 0:
            worksheet.write(i, 4, 'otwarty')
        else:
            worksheet.write(i, 4, 'zamknięty')
        # worksheet.write(i, 5, XS.rt)
        # worksheet.write(i, 6, XS.datum)
        i += 1
    workbook.close()
# NWK functions -------------------------------------------------------------------------------------------------------
def read_NWK(file):

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
    return nwk
# BRIDGES functions --------------------------------------------------------------------------------------------------
def read_bridge_xlsx(wb):
    bridgeXsBase = []
    for s in wb.worksheets:
        bridgeXsBase.append(bridge_xs(s))
    return bridgeXsBase

def distance(x1, x2, y1, y2):
    try:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    except:
        return 0
# counts height (z) distance betwean p point and z interpolated on a-b line in p station
def distanceZ(a, b, p):
    return p[1] - np.interp([p[0]], [a[0], b[0]], [a[1], b[1]])

def is_between(x1, y1, x, y, x2, y2):
    return round(distance(x1, x, y1, y)) + round(distance(x, x2, y, y2)) == round(distance(x1, x2, y1, y2))

def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    line1 = [[x1, y1], [x2, y2]]
    line2 = [[x3, y3], [x4, y4]]
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        x, y, b, c = None, None, None, None
    else:
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        b = (is_between(x3, y3, x, y, x4, y4))
        c = (is_between(x1, y1, x, y, x2, y2))

    return x, y, b, c

# fits cross section of objkect (koryto) to regular cross section
# xs - Xs objecty, koryto - list of list (station, elevation), przepust - list of list (station, elevation)
def dopasowanie(xs, koryto, przepust = None):
    #--- metoda marker
    if przepust != None:
        xsMarkStatElev = [float(i.station) for i in xs.points if i.kod == '<#8>' or i.kod == '<#16>' or i.kod == '<#20>' or i.kod == '<#9>']

        xsMark = sum(xsMarkStatElev) / len(xsMarkStatElev)
        maxPrzepStat = max(float(i[0]) for i in przepust)
        minPrzepStat = min(float(i[0]) for i in przepust)
        przepMark = (maxPrzepStat-minPrzepStat) / 2
        deltaPrzep = xsMark-przepMark
    return 0, deltaPrzep

# dopasowanie przekroii Xs, dopasowywyany krotszy przekroj
def fit_xs(xs1, xs2):
    flag=0 # domysle, jesli xs2 jes mniejsze,
    # pobranie punktow z markerow
    xs1StatElev = [[float(i.station), i.z, i.kod] for i in xs1.points if i.kod == '<#8>' or i.kod == '<#16>'or i.kod == '<#20>' or i.kod == '<#9>']
    xs2StatElev = [[float(i.station), i.z, i.kod] for i in xs2.points if i.kod == '<#8>' or i.kod == '<#16>'or i.kod == '<#20>' or i.kod == '<#9>']

    # sprawdzenie ktory przekroj jest dluzszy
    # ZMIENIC NA DELTE PO STATION
    xs1StatElevAll = [[float(i.station), i.z, i.kod] for i in xs1.points]
    xs2StatElevAll = [[float(i.station), i.z, i.kod] for i in xs2.points]

    # selekcja przekroju do dopasowania, powinien isc ten o korycie w mniejszym station, i byc przesuwany na prawo czyli coraz wiekszy station
    #if xs2StatElevAll[-1][0]-xs2StatElevAll[0][0] > xs1StatElevAll[-1][0]-xs1StatElevAll[0][0]:
    if xs2StatElevAll[-1][0] > xs1StatElevAll[-1][0]:
        xs1StatElev, xs2StatElev = xs2StatElev, xs1StatElev
        xs1, xs2 = xs2, xs1
        flag = 2 # xs2 jest wieksze i zamiana miejsc

    #stat = min([xs2StatElev[-1][0], xs2StatElev[0][0]])
    #statMax = max([xs2StatElev[-1][0], xs2StatElev[0][0]])

    # obliczenie sredniego przesuniecia markerow
    #if xs2StatElevAll[-1][0]-xs2StatElevAll[0][0] <= xs1StatElevAll[-1][0]-xs1StatElevAll[0][0]:
    i = 0
    dane = []
    for pkt in xs1StatElev:
        if pkt[2] == xs2StatElev[i][2]:
            delta = float(pkt[0])-float(xs2StatElev[i][0])
        dane.append(delta)
    m = np.mean(dane)

    #xs2ToFit = [[float(i.station), i.z] for i in xs2.points if float(stat)-(3*statMax-stat) < float(i.station) < float(statMax)+(3*statMax-stat)]
    #print(xs2ToFit)
    #print(stat,'--- ---')
    #dop, przes = dopasowanie(xs1,xs2ToFit)
    #print(m, flag)
    print('flag', flag)
    delta = m # przes



    for i in xs2.points:
        i.station = float(i.station)+delta

    if flag == 0:
        return xs1, xs2
    elif flag == 2:
        return xs2, xs1

def fit_bridge(xs, xsUp2, koryto, przepust, downS, upS):
    print(koryto, "koryto")
    minKor = min([i[1] for i in koryto])
    maxKor = max([i[1] for i in koryto])
    deltaKor = maxKor - minKor
    minXs = min(float(pkt.station) for pkt in xs.points)
    maxXs = max(float(pkt.station) for pkt in xs.points)
    deltaXs = maxXs - minXs
    minXsUp = min(float(pkt.station) for pkt in xsUp2.points)
    maxXsUp = max(float(pkt.station) for pkt in xsUp2.points)
    deltaXsUp = maxXsUp - minXsUp
    print(deltaXs, deltaXsUp, deltaKor)


    downS = minKor - float(downS)
    upS = minKor - float(upS)
    #print(koryto)
    # obliczenie przesuniecia koryta wzgledem xs
    minim, przes = dopasowanie(xs, koryto, przepust)
    # poczatkowy station przepustu
    startStat = min([i[0] for i in przepust])
    print(przes,startStat,'przes start stat')
    # przesuniecie obiektu (- start stat ?, nie wiem dla czego ale pomaga na dosuniecie)
    #if przes >= 0:
    deltaStatBridge = przes - startStat
    #else:
        #deltaStatBridge = przes + startStat
    # przesuniecie calego koryta o delta stat
    for element in koryto:
        element[0] = element[0]+deltaStatBridge
    przepMin = min([i[0] for i in przepust])+deltaStatBridge
    przepMax = max([i[0] for i in przepust])+deltaStatBridge
    korytoPrzep=[]
    # append culvert points to xs


    # usuniecie z przekroju punktow w obrebie przepustu, oraz powielajacych sie
    list=[]
    statList=[]
    statElevList=[]
    print("----------")
    for pkt in xs.points:
        # jesli w tym zakresie to pomijamy, else dodaje do nowej listy
        if przepMin-0.2 <= float(pkt.station) <= przepMax+0.2:
            # get previous and next koryto points
            #list.append(pkt)
            pass
        #jesli station sie powtarza sprawdzamy delta z i jesli wieksze od 0.05 to dodajemy
        elif pkt.station in statList:
            index = statList.index(pkt.station)
            z=statElevList[index][1]
            if abs(float(z)-float(pkt.z)) > 0.05:
                list.append(pkt)

        # else dodaje punkt
        else:

            list.append(pkt)
        # uzupelnienie list ze stattion do sprawdzenia
        statList.append(pkt.station)
        statElevList.append([pkt.station, pkt.z])
    xs.points = list

    # powielenie 2 przekroj
    list = []
    statList=[]
    statElevList=[]
    for pkt in xsUp2.points:
        if przepMin-0.2 <= float(pkt.station) <= przepMax+0.2:
            # get previous and next koryto points
            # list.append(pkt)
            pass

        elif pkt.station in statList:
            index = statList.index(pkt.station)
            z = statElevList[index][1]
            if abs(float(z) - float(pkt.z)) > 0.05:
                list.append(pkt)
        else:
            list.append(pkt)

        statList.append(pkt.station)
        statElevList.append([pkt.station, pkt.z])
    xsUp2.points = list

    # dodanie punktow z koryta w obrebie culvert na przekroje (oba)
    flagP = 0
    for element in koryto:
        # tutaj zmienic zakres jesli wewnatrz

        # dla punktow koryta w obrebie przepustu
        if przepMin < float(element[0]) < przepMax:
            #tworzy linnie do dodania punktu
            line = '{} {} {} {}'.format(element[0], element[1]-0.1-float(downS), 0.03, 'P1')
            #dodawanie w miejscu stalego indexu, ma zachowac kolejnosc punktow a nie po station
            print(float(element[0])," float element od 0")
            print(xs.km)
            print([float(poi.station) for poi in xs.points])
            if flagP == 0:
                indesXsPk1 = min([float(poi.station) for poi in xs.points if float(poi.station) >= float(element[0])])
                for items in xs.points:
                    if float(indesXsPk1) == float(items.station):
                        punkt = items
                indesXsPk1 = xs.points.index(punkt)
                #del xs.points[indesXsPk1]
            elif flagP == 1:
                indesXsPk1 += 1
                # zmienny index do obliczenia delta z
            indesXsPkz = min([float(poi.station) for poi in xs.points if float(poi.station) >= float(element[0])])
            for items in xs.points:
                if float(indesXsPkz) == float(items.station):
                    punkt = items
            indesXsPkz = xs.points.index(punkt)
            z1 = xs.points[indesXsPkz-1]
            z2 = xs.points[indesXsPkz]
            d = distanceZ([float(z1.station), float(z1.z)],[float(z2.station), float(z2.z)],[float(element[0]),float(element[1])])
            #d = float(element[1]) - min([float(z1.z), float(z2.z)])
            print(indesXsPk1, "index")
            if d != 0.0:
                xs.points.insert(indesXsPk1, Pkt(line))
                pass
            # insert in proper place second XS
            line = '{} {} {} {}'.format(element[0], element[1] - 0.1 - float(upS), 0.03, 'P1')
            if flagP == 0:
                indesXsPk = min([float(poi.station) for poi in xsUp2.points if float(poi.station) >= float(element[0])])
                for items in xsUp2.points:
                    if float(indesXsPk) == float(items.station):
                        punkt = items
                indesXsPk = xsUp2.points.index(punkt)
            elif flagP == 1:
                indesXsPk += 1
                print(indesXsPk, "index")
            indesXsPkz = min([float(poi.station) for poi in xsUp2.points if float(poi.station) >= float(element[0])])
            for items in xsUp2.points:
                if float(indesXsPkz) == float(items.station):
                    punkt = items
            indesXsPkz = xsUp2.points.index(punkt)
            z1 = xsUp2.points[indesXsPkz-1]
            z2 = xsUp2.points[indesXsPkz]
            d = distanceZ([float(z1.station), float(z1.z)], [float(z2.station), float(z2.z)],[float(element[0]), float(element[1])])
            #d = float(element[1]) - min([float(z1.z), float(z2.z)])
            if d != 0.0:
                xsUp2.points.insert(indesXsPk, Pkt(line))
                pass
            print(przepMin, przepMax)
            flagP = 1
    print(przes+startStat," bridge shift")
    return xs, xsUp2, deltaStatBridge