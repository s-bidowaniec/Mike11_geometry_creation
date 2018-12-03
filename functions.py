﻿import numpy as np
import collections
import xlsxwriter
import numpy
from classes import *
from dbfread import DBF
import copy
# UNIVERSAl -----------------------------------------------------------------------------------------------------------

def pointToLine(x1, y1, x2, y2, x=None, y=None):
    """
    Function calculates new (x,y) coordinates droped on line defined by points A, B.
    :param x1: float
    :param y1: float
    :param x2: float
    :param y2: float
    :param x: float
    :param y: float
    :return: touple of floats, new x and new y
    """

    # def computePoints(self):
    licznik = ((x - x1) * (x2 - x1)) + ((y - y1) * (y2 - y1))
    mianownik = ((x1 - x2) ** 2) + ((y1 - y2) ** 2)
    try:
        u = licznik / mianownik
    except ZeroDivisionError:
        u = 0

    xp = ((x2 - x1) * u) + x1
    yp = ((y2 - y1) * u) + y1
    return xp, yp


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
    for record in DBF(dbf, load=True):
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
    headings = ['Nazwa rzeki', 'Topo ID', 'KilometraÄąÄ˝', 'ID Przekroju', 'Typ przekroju']  # 'Radius Type', 'Datum'
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
            worksheet.write(i, 4, 'zamkniĂ„â„˘ty')
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

    # zaczytywanie poczﾹtku pliku
    while i < len(readline) and "POINTS" not in readline[i]:
        nwk.add_start(readline[i])
        i += 1
    i += 1
    
    # zaczytywanie punktÄ‚Ĺ‚w do klasy nwkFile
    while i < len(readline) and "EndSect  // POINTS" not in readline[i]:
        line = readline[i]
        stringList, name = line_to_list(line)
        nwk.add_point(stringList, name)
        i += 1

    # przejÄąâ€şcie do pierwszego "brancha"
    while "[branch]" not in readline[i]:
        i += 1

    while i < len(readline) and "EndSect  // BRIDGE" not in readline[i]:            # zmieniono CULVERT na BRIDGE
        line = readline[i]

        if not line.split():
            i += 1
            continue

        data_list, name = line_to_list(line)

        if "[branch]" in line:
            nwk.branchList.append(Branch()) 
            cl = nwk.branchList[-1]

        elif "[linkchannel]" in line:

            cl.linkChannel = LinkChannel(cl)    # utworzenie klasy, argumentem jest klasa powy﾿ej (parent)
            cl = cl.linkChannel                 # zmienna cl przechodzi do klasy "poni﾿ej"

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
            
        elif "[bridge_data]" in line:
            nwk.bridgeList.append(Bridge())
            cl = nwk.bridgeList[-1]


        elif cl.end in line and cl.parent is None:      # je﾿eli klasa siê koñczy, a nie ma klasy powy﾿ej (co to za przypadek?)
            i += 1
            continue

        elif cl.end in line:
            cl = cl.parent

        else:
            cl.add_parameters(data_list, name, line)    # tu prawdopodobnie wywali
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
        #print(str(s.cell(row=5, column=5).value).lower())
        if "tak" in str(s.cell(row=5, column=5).value).lower():
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
    print(div)
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

# dopasowanie przekroii Xs
def fit_xs(xs1, xs2):
    xs1 = copy.deepcopy(xs1)
    xs2 = copy.deepcopy(xs2)
    # pobranie punktow z markerow
    xs1StatElev = [[float(i.station), i.z, i.kod] for i in xs1.points if i.kod == '<#8>' or i.kod == '<#16>'or i.kod == '<#20>' or i.kod == '<#9>']
    xs2StatElev = [[float(i.station), i.z, i.kod] for i in xs2.points if i.kod == '<#8>' or i.kod == '<#16>'or i.kod == '<#20>' or i.kod == '<#9>']

    # obliczenie sredniego przesuniecia markerow
    dane = []
    for pkt in xs1StatElev:
        for pkt2 in xs2StatElev:
            if pkt[2] == pkt2[2]:
                delta = float(pkt[0])-float(pkt2[0])
                dane.append(delta)
    m = np.mean(dane)
    try:
        int(float(m))
    except:
        print('------------------------- shift 0 -------------------------')
        m = 0

    delta = float(m) #przes

    for i in xs2.points:
        i.station = float(i.station) + delta

    return xs1, xs2

def fit_weir(xsWeir, weir, base_manning=0.04, bridgeType = False):
    weir = copy.deepcopy(weir)
    #przepMin = min([i[0] for i in weir.koryto])
    #przepMax = max([i[0] for i in weir.koryto])
    minim, przes = dopasowanie(xsWeir, weir.koryto, weir.przelew)
    startStat = min([i[0] for i in weir.koryto])
    print(przes, startStat, 'przes start stat')
    # przesuniecie obiektu (- start stat ?, nie wiem dla czego ale pomaga na dosuniecie)
    # if przes >= 0:

    if bridgeType:
        deltaStatBridge = bridgeType
    else:
        deltaStatBridge = przes - startStat
    # else:
    # deltaStatBridge = przes + startStat
    # przesuniecie calego koryta o delta stat
    for element in weir.koryto:
        element[0] = element[0] + deltaStatBridge
    przepMin = min([i[0] for i in weir.koryto]) # + deltaStatBridge
    przepMax = max([i[0] for i in weir.koryto]) # + deltaStatBridge

    # usuniecie z przekroju punktow w obrebie przepustu, oraz powielajacych sie
    list=[]
    statList=[]
    statElevList=[]
    excludedMarkerListXs1 = []
    print("----------")

    for pkt in xsWeir.points:
        # jesli w tym zakresie to pomijamy, else dodaje do nowej listy
        if przepMin + 0.1 < float(pkt.station) < przepMax - 0.1:
            # zapis stationow markerow

            if pkt.kod != '<#0>':
                excludedMarkerListXs1.append(pkt)

            #list pass - pomija punkty w przekroju
            pass
        #jesli station sie powtarza sprawdzamy delta z i jesli wieksze od 0.05 to dodajemy
        elif pkt.station in statList:
            index = statList.index(pkt.station)
            z=statElevList[index][1]
            if abs(float(z)-float(pkt.z)) > 0.05:
                list.append(pkt)
                #pass

        # else dodaje punkt, - poza culvertem
        else:
            list.append(pkt)
        # uzupelnienie list ze stattion do sprawdzenia
        statList.append(pkt.station)
        statElevList.append([pkt.station, pkt.z])
    xsWeir.points = list

    flagP = 0

    for element in weir.koryto:
        # dla punktow koryta w obrebie przepustu

        if przepMin <= float(element[0]) <= przepMax:
            # tworzy linnie do dodania punktu
            #if int(weir.rn.split()[1]) == 1:
            line = '{} {} {} {}'.format(element[0], element[1], weir.mann, 'P1')
            #else:
                #line = '{} {} {} {}'.format(element[0], element[1], weir.mann,
                                            #'P1')
            # dodawanie w miejscu stalego indexu, ma zachowac kolejnosc punktow a nie po station
            print(float(element[0]), " float element od 0")
            print(xsWeir.km)
            print([float(poi.station) for poi in xsWeir.points])
            if flagP == 0:
                try:
                    indesXsPk1 = min([float(poi.station) for poi in xsWeir.points if float(poi.station) >= float(element[0])])
                except:
                    import pdb
                    pdb.set_trace()
                for items in xsWeir.points:
                    if float(indesXsPk1) == float(items.station):
                        punkt = items
                indesXsPk1 = xsWeir.points.index(punkt)
                # del xs.points[indesXsPk1]
            elif flagP == 1:
                #pass
                indesXsPk1 += 1
                # zmienny index do obliczenia delta z

            indesXsPkz = min([float(poi.station) for poi in xsWeir.points if float(poi.station) >= float(element[0])])

            for items in xsWeir.points:
                if float(indesXsPkz) == float(items.station):
                    punkt = items
            indesXsPkz = xsWeir.points.index(punkt)
            z1 = xsWeir.points[indesXsPkz - 1]
            z2 = xsWeir.points[indesXsPkz]
            d = distanceZ([float(z1.station), float(z1.z)], [float(z2.station), float(z2.z)],
                          [float(element[0]), float(element[1])])
            # d = float(element[1]) - min([float(z1.z), float(z2.z)])
            print(indesXsPk1, "index")
            if d != 0.05:
                xsWeir.points.insert(indesXsPk1, Pkt(line))
            flagP = 1

    return xsWeir, excludedMarkerListXs1, deltaStatBridge

def fit_bridge_v2(xsDown, xsUp, bridge, base_manning=0.04):
    """ dopasowanie przy pomocy matplot lib i recznego dosunięcia przekroi """
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Button
    from matplotlib.widgets import TextBox
    import copy

    koryto, przepust, downS, upS = bridge.koryto, bridge.przepust, bridge.downS, bridge.upS
    minim, przes = dopasowanie(xsDown, koryto, przepust)
    startStat = min([i[0] for i in przepust])
    deltaStatBridge = przes - startStat
    delta1 = deltaStatBridge
    min_culvert = min([y[1] for y in przepust])

    y1 = [pkt.z for pkt in xsUp.points]
    y2 = [pkt.z for pkt in xsDown.points]
    x1 = [pkt.station for pkt in xsUp.points]
    x2 = [pkt.station for pkt in xsDown.points]
    y1_origin, y2_origin, x1_origin, x2_origin = copy.copy(y1), copy.copy(y2), copy.copy(x1), copy.copy(x2)
    xsUp_origin = copy.deepcopy(xsUp)
    xsDown_origin = copy.deepcopy(xsDown)
    xc = [x[0]+deltaStatBridge for x in przepust]
    yc = [y[1] for y in przepust]
    ycD = copy.deepcopy(yc)
    deltaUp = float(upS) - min(yc)
    deltaDo = float(downS) - min(yc)

    for i in range(len(yc)):
        yc[i] += deltaUp
        ycD[i] += deltaDo

    class Buttons(object):
        spacing = 0.5

        def submit(self, text):
            data = eval(text)
            self.spacing = data
            plt.draw()

        def prawo(self, event):
            nonlocal x1
            for i in range(len(x1)):
                x1[i] += self.spacing
            a.set_xdata(x1)
            plt.draw()

        def lewo(self, event):
            nonlocal x1
            for i in range(len(x1)):
                x1[i] -= self.spacing
            a.set_xdata(x1)
            plt.draw()

        def doGory(self, event):
            nonlocal y1
            for i in range(len(y1)):
                y1[i] += self.spacing
            a.set_ydata(y1)
            plt.draw()

        def wDol(self, event):
            nonlocal y1
            for i in range(len(y1)):
                y1[i] -= self.spacing
            a.set_ydata(y1)
            plt.draw()

        def save(self, event):
            nonlocal x1
            nonlocal y1
            nonlocal xsUp
            for i in range(len(x1)):
                xsUp.points[i].station = x1[i]
                xsUp.points[i].z = y1[i]

        def refresh(self, event):
            nonlocal x1
            nonlocal x1_origin
            nonlocal y1
            nonlocal y1_origin
            nonlocal xsUp
            xsUp = copy.copy(xsUp_origin)
            y1 = copy.copy(y1_origin)
            x1 = copy.copy(x1_origin)
            a.set_ydata(y1)
            a.set_xdata(x1)
            plt.draw()

        def burn(self, event):
            nonlocal x1
            nonlocal y1
            nonlocal xsUp
            nonlocal bridge
            delta1 = x1_origin[0] - x1[0]
            start = min(xc)
            end = max(xc)
            index_s = x1.index(max([x if x <= start else x1[0] for x in x1]))
            index_e = x1.index(min([x if x >= end else x1[-1] for x in x1]))
            kor = list(filter(lambda x: start <= x[0]+deltaStatBridge <= end, koryto))
            x_midle = [x[0]+deltaStatBridge for x in kor]
            y_middle = [x[1]+deltaUp for x in kor]
            pkt_middle = []
            for i in range(len(x_midle)):
                pkt_middle.append(Pkt("{} {} {} <#0>".format(x_midle[i], y_middle[i], bridge.mann)))
            x_left = x1[:index_s]
            y_left = y1[:index_s]
            pkt_left = xsUp.points[:index_s]
            x_right = x1[index_e:]
            y_right = y1[index_e:]
            pkt_right = xsUp.points[index_e:]
            x = x_left+x_midle+x_right
            y = y_left+y_middle+y_right
            x1,y1 = x,y
            a.set_ydata(y)
            a.set_xdata(x)
            xsUp.points = pkt_left+pkt_middle+pkt_right
            plt.draw()


        def prawo2(self, event):
            nonlocal x2
            for i in range(len(x2)):
                x2[i] += self.spacing
            b.set_xdata(x2)
            plt.draw()

        def lewo2(self, event):
            nonlocal x2
            for i in range(len(x2)):
                x2[i] -= self.spacing
            b.set_xdata(x2)
            plt.draw()

        def doGory2(self, event):
            nonlocal y2
            for i in range(len(y2)):
                y2[i] += self.spacing
            b.set_ydata(y2)
            plt.draw()

        def wDol2(self, event):
            nonlocal y2
            for i in range(len(y2)):
                y2[i] -= self.spacing
            b.set_ydata(y2)
            plt.draw()

        def save2(self, event):
            nonlocal x2
            nonlocal y2
            nonlocal xsDown
            for i in range(len(x2)):
                xsDown.points[i].station = x2[i]
                xsDown.points[i].z = y2[i]


        def refresh2(self, event):
            nonlocal x2
            nonlocal x2_origin
            nonlocal y2
            nonlocal y2_origin
            nonlocal xsDown

            xsDown = copy.copy(xsDown_origin)
            y2 = copy.copy(y2_origin)
            x2 = copy.copy(x2_origin)
            b.set_ydata(y2)
            b.set_xdata(x2)
            plt.draw()

        def burn2(self, event):
            nonlocal x2
            nonlocal y2
            nonlocal xsDown
            nonlocal bridge
            delta = x2_origin[0] - x2[0]
            start = min(xc)
            end = max(xc)
            index_s = x2.index(max([x if x <= start else x2[0] for x in x2]))
            index_e = x2.index(min([x if x >= end else x2[-1] for x in x2]))
            kor = list(filter(lambda x: start <= x[0]+deltaStatBridge <= end, koryto))
            x_midle = [x[0]+deltaStatBridge for x in kor]
            y_middle = [x[1]+deltaDo for x in kor]
            pkt_middle = []
            for i in range(len(x_midle)):
                pkt_middle.append(Pkt("{} {} {} <#0>".format(x_midle[i], y_middle[i], bridge.mann)))
            x_left = x2[:index_s]
            y_left = y2[:index_s]
            pkt_left = xsDown.points[:index_s]
            x_right = x2[index_e:]
            y_right = y2[index_e:]
            pkt_right = xsDown.points[index_e:]
            x = x_left+x_midle+x_right
            y = y_left+y_middle+y_right
            x2, y2 = x, y
            b.set_ydata(y2)
            b.set_xdata(x2)
            xsDown.points = pkt_left+pkt_middle+pkt_right
            plt.draw()

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    plt.subplot(2, 1, 1)
    a, = plt.plot(x1, y1, 'g')
    plt.plot(xc, yc, 'r')
    ax.set_xticks(numpy.arange(0, 1, 0.1))
    ax.set_yticks(numpy.arange(0, 1., 0.1))
    plt.grid(True)
    plt.title('Obiekt: nr{} - km {} - typ {}'.format(bridge.lp, bridge.km, bridge.typ))
    plt.ylabel('MikeDownstream(powyżej)\n{}\n{}'.format(xsUp.id, xsUp.km))

    callback = Buttons()

    axbox = plt.axes([0.05, 0.04, 0.04, 0.055])
    text_box = TextBox(axbox, '', initial=str(Buttons.spacing))
    text_box.on_submit(callback.submit)

    axright = plt.axes([0.26, 0.04, 0.07, 0.055])
    bright = Button(axright, 'Prawo', color='#9fcc51', hovercolor='#d3f29b')
    bright.on_clicked(callback.prawo)

    axleft = plt.axes([0.1, 0.04, 0.07, 0.055])
    bleft = Button(axleft, 'Lewo', color='#9fcc51', hovercolor='#d3f29b')
    bleft.on_clicked(callback.lewo)

    axup = plt.axes([0.18, 0.07, 0.07, 0.055])
    bup = Button(axup, 'Góra', color='#9fcc51', hovercolor='#d3f29b')
    bup.on_clicked(callback.doGory)

    axdown = plt.axes([0.18, 0.01, 0.07, 0.055])
    bdown = Button(axdown, 'Dół', color='#9fcc51', hovercolor='#d3f29b')
    bdown.on_clicked(callback.wDol)

    axrefresh = plt.axes([0.34, 0.11, 0.095, 0.04])
    brefresh = Button(axrefresh, 'Odśwież', color='#86a385', hovercolor='#b1d4af')
    brefresh.on_clicked(callback.refresh)

    axburn = plt.axes([0.34, 0.06, 0.095, 0.04])
    bburn = Button(axburn, 'Wypal', color='#86a385', hovercolor='#b1d4af')
    bburn.on_clicked(callback.burn)

    axsave = plt.axes([0.34, 0.01, 0.095, 0.04])
    bsave = Button(axsave, 'Zapisz', color='#86a385', hovercolor='#b1d4af')
    bsave.on_clicked(callback.save)

    plt.subplot(2, 1, 2)
    b, = plt.plot(x2, y2, 'b')
    plt.plot(xc, ycD, 'r')
    ax.set_xticks(numpy.arange(0, 1, 0.1))
    ax.set_yticks(numpy.arange(0, 1., 0.1))
    plt.grid(True)
    plt.ylabel('MikeUpstream(Poniżej)\n{}\n{}'.format(xsDown.id, xsDown.km))

    axright2 = plt.axes([0.71, 0.04, 0.07, 0.055])
    bright2 = Button(axright2, 'Prawo', color='#9bb7f2', hovercolor='#587ed0')
    bright2.on_clicked(callback.prawo2)

    axleft2 = plt.axes([0.55, 0.04, 0.07, 0.055])
    bleft2 = Button(axleft2, 'Lewo', color='#9bb7f2', hovercolor='#587ed0')
    bleft2.on_clicked(callback.lewo2)

    axup2 = plt.axes([0.63, 0.07, 0.07, 0.055])
    bup2 = Button(axup2, 'Góra', color='#9bb7f2', hovercolor='#587ed0')
    bup2.on_clicked(callback.doGory2)

    axdown2 = plt.axes([0.63, 0.01, 0.07, 0.055])
    bdown2 = Button(axdown2, 'Dół', color='#9bb7f2', hovercolor='#587ed0')
    bdown2.on_clicked(callback.wDol2)

    axrefresh2 = plt.axes([0.79, 0.11, 0.095, 0.04])
    brefresh2 = Button(axrefresh2, 'Odśwież', color='#6188bd', hovercolor='#8bb9f9')
    brefresh2.on_clicked(callback.refresh2)

    axburn2 = plt.axes([0.79, 0.06, 0.095, 0.04])
    bburn2 = Button(axburn2, 'Wypal', color='#6188bd', hovercolor='#8bb9f9')
    bburn2.on_clicked(callback.burn2)

    axsave2 = plt.axes([0.79, 0.01, 0.095, 0.04])
    bsave2 = Button(axsave2, 'Zapisz', color='#6188bd', hovercolor='#8bb9f9')
    bsave2.on_clicked(callback.save2)


    plt.show()

    return xsDown, xsUp, deltaStatBridge, [], []

def fit_bridge(xs, xsUp2, bridge, base_manning=0.04):
    """ dopasowanie automatyczne na podstawie markerów 4 i 5 """
    koryto, przepust, downS, upS = bridge.koryto, bridge.przepust, bridge.downS, bridge.upS
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
    print(przes, startStat, 'przes start stat')
    # przesuniecie obiektu (- start stat ?, nie wiem dla czego ale pomaga na dosuniecie)
    #if przes >= 0:
    deltaStatBridge = przes - startStat
    #else:
        #deltaStatBridge = przes + startStat
    # przesuniecie calego koryta o delta stat
    for element in koryto:
        element[0] = element[0]+deltaStatBridge
    przepMin = min([i[0] for i in przepust]) + deltaStatBridge
    przepMax = max([i[0] for i in przepust]) + deltaStatBridge
    korytoPrzep = []
    # append river points to xs if xs is to short
    import copy
    xs_appending = copy.deepcopy(xs)
    xsUp2_appending = copy.deepcopy(xsUp2)
    insert_index1 = 0
    insert_index2 = 0
    for element in koryto:
        # tutaj zmienic zakres jesli wewnatrz
        index_1 = [float(poi.station) for poi in xs_appending.points if float(poi.station) > float(element[0])]
        index_1b = [float(poi.station) for poi in xs_appending.points if float(poi.station) < float(element[0])]
        if len(index_1) == 0 or len(index_1b) == 0:
            if int(xs.rn.split()[1]) == 1:
                line = '{} {} {} {}'.format(element[0], element[1]-0.01-float(downS), bridge.mann, 'P1')
            else:
                line = '{} {} {} {}'.format(element[0], element[1] - 0.01 - float(downS), bridge.mann/base_manning, 'P1')
            if len(index_1) == 0:
                xs.points.append(Pkt(line))
            elif len(index_1b) == 0:
                xs.points.insert(insert_index1, Pkt(line))
                insert_index1 += 1

        index_2 = [float(poi.station) for poi in xsUp2_appending.points if float(poi.station) > float(element[0])]
        index_2b = [float(poi.station) for poi in xsUp2_appending.points if float(poi.station) < float(element[0])]
        if len(index_2) == 0 or len(index_2b) == 0:
            if int(xsUp2.rn.split()[1]) == 1:
                line = '{} {} {} {}'.format(element[0], element[1] - 0.01 - float(upS), bridge.mann, 'P1')
            else:
                line = '{} {} {} {}'.format(element[0], element[1] - 0.01 - float(upS), bridge.mann/base_manning, 'P1')
            if len(index_2) == 0:
                xsUp2.points.append(Pkt(line))
            elif len(index_2b) == 0:
                xsUp2.points.insert(insert_index2, Pkt(line))


    # usuniecie z przekroju punktow w obrebie przepustu, oraz powielajacych sie
    list=[]
    statList=[]
    statElevList=[]
    excludedMarkerListXs1 = []
    excludedMarkerListXs2 = []
    print("----------")
    for pkt in xs.points:
        # jesli w tym zakresie to pomijamy, else dodaje do nowej listy
        if przepMin + 0.1 < float(pkt.station) < przepMax - 0.1:
            # zapis stationow markerow
            if pkt.kod != '<#0>':
                excludedMarkerListXs1.append(pkt)

            #list pass - pomija punkty w przekroju
            pass
        #jesli station sie powtarza sprawdzamy delta z i jesli wieksze od 0.05 to dodajemy
        elif pkt.station in statList:
            index = statList.index(pkt.station)
            z=statElevList[index][1]
            if abs(float(z)-float(pkt.z)) > 0.05:
                list.append(pkt)

        # else dodaje punkt, - poza culvertem
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
        if przepMin-0.1 <= float(pkt.station) <= przepMax+0.1:
            # zapis stationow markerow
            if pkt.kod != '<#0>':
                excludedMarkerListXs2.append(pkt)
            pass

        elif pkt.station in statList:
            index = statList.index(pkt.station)
            z = statElevList[index][1]
            if abs(float(z) - float(pkt.z)) > 0.01:
                list.append(pkt)
        else:
            list.append(pkt)

        statList.append(pkt.station)
        statElevList.append([pkt.station, pkt.z])
    xsUp2.points = list

    # dodanie punktow z koryta w obrebie culvert na przekroje (oba)


    flagP = 0
    for element in koryto:
        # dla punktow koryta w obrebie przepustu

        if przepMin <= float(element[0]) <= przepMax:
            #tworzy linnie do dodania punktu
            if int(xs.rn.split()[1]) == 1:
                line = '{} {} {} {}'.format(element[0], element[1]-0.01-float(downS), bridge.mann, 'P1')
            else:
                line = '{} {} {} {}'.format(element[0], element[1] - 0.01 - float(downS), bridge.mann/base_manning, 'P1')
            #dodawanie w miejscu stalego indexu, ma zachowac kolejnosc punktow a nie po station
            print(float(element[0]), " float element od 0")
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
            d = distanceZ([float(z1.station), float(z1.z)], [float(z2.station), float(z2.z)], [float(element[0]), float(element[1])])
            #d = float(element[1]) - min([float(z1.z), float(z2.z)])
            print(indesXsPk1, "index")
            if d != 0.0:
                xs.points.insert(indesXsPk1, Pkt(line))
                pass
            # insert in proper place second XS
            if int(xsUp2.rn.split()[1]) == 1:
                line = '{} {} {} {}'.format(element[0], element[1] - 0.01 - float(upS), bridge.mann, 'P1')
            else:
                line = '{} {} {} {}'.format(element[0], element[1] - 0.01 - float(upS), bridge.mann/base_manning, 'P1')
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
            d = distanceZ([float(z1.station), float(z1.z)], [float(z2.station), float(z2.z)], [float(element[0]), float(element[1])])
            #d = float(element[1]) - min([float(z1.z), float(z2.z)])
            if d != 0.0:
                xsUp2.points.insert(indesXsPk, Pkt(line))
                pass
            print(przepMin, przepMax)
            flagP = 1
    min_xs_stat = min([float(poi.station) for poi in xs.points])
    max_xs_stat = max([float(poi.station) for poi in xs.points])
    min_xsUp_stat = min([float(poi.station) for poi in xsUp2.points])
    max_xsUp_stat = max([float(poi.station) for poi in xsUp2.points])
    delta_xs = abs(min_xs_stat - max_xs_stat)
    delta_xsUp = abs(min_xsUp_stat-max_xsUp_stat)
    bridge.weir_width = min(delta_xs, delta_xsUp)
    print(przes+startStat," bridge shift")
    return xs, xsUp2, deltaStatBridge, excludedMarkerListXs1, excludedMarkerListXs2


def add_markers(xs, markers):
    """
    :param xs:
    :param markers:
    :return:
    """

    # dla kazdego markera
    for point in markers:
        insertPoint = point
        # pobrac station
        station = float(point.station)
        # pobrac puntkty przed i za stationem
        minimal = []
        maximal = []
        for i in xs.points:
            if float(i.station) > station:
                minimal.append(i)
            elif float(i.station) < station:
                maximal.append(i)
        startPoint = min(minimal, key = lambda x: float(x.station))
        startIndex = xs.points.index(startPoint)
        endPoint = max(maximal, key = lambda x: x.station)
        # wyinterpolowac z value w station
        # ys = y1 +(xs-x1)*((y2-y1)/(x2-x1))
        insertPoint.z = startPoint.z + (station - startPoint.station) * ((endPoint.z - startPoint.z) / (endPoint.station - startPoint.station))
        # dodac punkt z oznaczeniem markera na przekroj
        xs.points.insert(startIndex, insertPoint)
        print(len(xs.points), " ilosc pkt na przekroju")


def linear_equation(array):
    a = np.array([
         [(array[0][0]) ** 2, array[0][0], 1],
         [(array[1][0]) ** 2, array[1][0], 1],
         [(array[2][0]) ** 2, array[2][0], 1]
         ])
    b = np.array([
        array[0][1],
        array[1][1],
        array[2][1]
        ])
    x = np.linalg.solve(a,b)
    return lambda y: x[0]*y**2 + x[1]*y + x[2]

