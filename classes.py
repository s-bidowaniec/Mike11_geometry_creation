# -*- coding: utf-8 -*-
import shelve
import math, collections
from operator import itemgetter
from rdp import rdp
import time
# clas func
def distance(x1, x2, y1, y2):
    """
    Function calculates distance betwean two points
    :param x1: float
    :param x2: float
    :param y1: float
    :param y2: float
    :return: float
    """
    try:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    except:
        return 0
# counts height (z) distance betwean p point and z interpolated on a-b line in p station
def distanceZ(a, b, p):
    return p[1] - np.interp([p[0]], [a[0], b[0]], [a[1], b[1]])

def is_between(x1, y1, x, y, x2, y2):
    return round((distance(x1, x, y1, y)) + (distance(x, x2, y, y2))) == round(distance(x1, x2, y1, y2))

def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    line1 = [[x1, y1], [x2, y2]]
    line2 = [[x3, y3], [x4, y4]]
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    #print(div)
    if div == 0:
        x, y, b, c = None, None, None, None
    else:
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        b = (is_between(x3, y3, x, y, x4, y4))
        c = (is_between(x1, y1, x, y, x2, y2))

    return x, y, b, c

# UNIVERSAL -----------------------------------------------------------------------------------------------------------
class Points2Line(object):
    """klasa zawierająca w sobie współrzędne dwóch punktów określających prostą, oraz
    jednego punktu który będzie na nią rzutowany"""

    def __init__(self, x1, y1, x2, y2, x = None, y = None):
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        self.x = float(x)
        self.y = float(y)

        # def computePoints(self):
        licznik = ((self.x - self.x1) * (self.x2 - self.x1)) + ((self.y - self.y1) * (self.y2 - self.y1))
        mianownik = ((self.x1 - self.x2) ** 2) + ((self.y1 - self.y2) ** 2)
        try:
            u = licznik / mianownik
        except:
            u = 0
        self.xp = ((self.x2 - self.x1) * u) + self.x1
        self.yp = ((self.y2 - self.y1) * u) + self.y1

# XS rawdata classes --------------------------------------------------------------------------------------------------

class Pkt(object):
    def __init__(self, line="0, 0, 0, <#0>"):
        if line is str and len(line.split()) != 7:
            print(len(line.split()))
            print(line,'\n','-----------')
        #self.station, self.z, self.manning.py, self.kod = zip(*line.split()[:-3])
        self.station, self.z, self.manning, self.kod = line.split()[0], line.split()[1],line.split()[2],line.split()[3]
        #return '{} {}'.format(self.station, self.z)

class Xs(object):
    def __init__(self):
        self.dane = []
        self.points = []
        self.cs = 0
    def kordy(self):
        self.left = self.cords.split()[1:3]
        self.right = self.cords.split()[3:5]
        elev_points = []
        print('dane')
        print(len(self.points))
        for point in self.points:
            try:
                h = point.z
                elev_points.append(h)
            except:
                print(point)
        self.max_left = max(elev_points[0:1])
        self.min_left = min(elev_points[0:3])
        self.mean_left = float(self.max_left) / 1
        self.max_right = max(elev_points[-2:-1])
        self.min_right = min(elev_points[-4:-1])
        self.mean_right = float(self.max_right) / 1
    pass
    def rdp_pkt(self, epsilon):
        self.pointsRdp=[]
        set = [[float(i.station), float(i.z)] for i in self.points]
        set2 = rdp(set, epsilon=epsilon)
        set3 = [i[0] for i in set2]
        print('Redukcja RDP o {} punktów z {}, river: {} km: {}.'.format(len(set)-len(set2), len(set), self.riverCode, self.km))
        manningOld = 0
        for pkt in self.points:
            if str(float(pkt.station)) in str(set3):
                self.pointsRdp.append(pkt)
            elif pkt.manning != manningOld or pkt.kod != '<#0>':
                self.pointsRdp.append(pkt)
                print('Zachowano punkt zmiany manninga z {} na {} w station: {}.'.format(manningOld, pkt.manning, pkt.station))
            manningOld = pkt.manning
        if len(self.pointsRdp)>3:
            self.points = self.pointsRdp
    def print_txt(self, file, zaok, rr):
        #print(self.km)
        file.write('{}\r\n'.format(self.reachCode))
        file.write('{}\r\n'.format(self.riverCode))
        file.write('               {}\r\n'.format(round(float(self.km), zaok)))
        file.write('COORDINATES\r\n')
        file.write('{}'.format(self.cords))
        file.write('FLOW DIRECTION\r\n{}'.format(self.fd))
        file.write('PROTECT DATA\r\n{}'.format(self.pd))
        file.write('DATUM\r\n{}'.format(self.datum))
        try:
            if self.cs == 1:
                file.write('CLOSED SECTION\r\n    {}\r\n'.format(self.cs))
            else:
                pass
        except:
            pass
        file.write('RADIUS TYPE\r\n{}'.format(self.rt))
        file.write('DIVIDE X-Section\r\n{}'.format(self.dx))
        file.write('SECTION ID\r\n    {}'.format(self.id))
        file.write('INTERPOLATED\r\n{}'.format(self.inter))
        file.write('ANGLE\r\n{}'.format(self.angle))
        try:
            rr = self.rr
        except:
            pass
        if rr == None:
            file.write('RESISTANCE NUMBERS\r\n   2  1     1.000     1.000     1.000    1.000    1.000\r\n')
        else:
            file.write('RESISTANCE NUMBERS\r\n   2  0     1.000     1.000     1.000    1.000    1.000\r\n')
        file.write('PROFILE        {}\r\n'.format(self.profile))
        for pkt in self.points:
            #if rr == None:
            file.write('  {}   {}   {}     {}     0     0.000     0\r\n'.format(pkt.station, pkt.z, pkt.manning, pkt.kod))
            """
            elif rr != None:
                file.write(
                    '  {}   {}   {}     {}     0     0.000     0\r\n'.format(pkt.station, pkt.z, float(pkt.manning)/rr, pkt.kod))
            """
        file.write('LEVEL PARAMS\r\n{}'.format(self.lp))
        file.write('*******************************\r\n')

class PktN(object):
    def __init__(self, record):
        self.station = record['Fraction']*record['Shape_Leng']
        self.manning = round(record['N_Value'], 4)

class ManningXS(object):
    def __init__(self, record):
        self.punkty = collections.OrderedDict()
        self.riverCode, self.reachCode, self.km = record['RiverCode'], record['ReachCode'], record['ProfileM']
        station = record['Fraction'] * record['Shape_Leng']
        self.punkty[station] = PktN(record)
        self.typXS = str(record['TypXS'])+"\n"
    def dodaj(self, record):
        station = record['Fraction'] * record['Shape_Leng']
        self.punkty[station]=PktN(record)
# NWK ------------------------------------------------------------------------------------------------------------------
class NwkPoint(object):
    def __init__(self, no, x, y, val1, val2, val3, z=None):
        self.no = no
        self.x = x
        self.y = y
        self.val1 = val1
        self.val2 = val2
        self.val3 = val3
        self.z = z
        self.end = None

    def values_2_string(self):
        dataDict = self.__dict__
        for i in dataDict:
            if type(dataDict[i]) == int or type(dataDict[i]) == float:
                dataDict[i] = str(dataDict[i])


class Elevation(object):
    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Elevation"
        self.parent = parent

    def add_paramaters(self, string_list, name, line):
        self.data.append(string_list[1:])

    def values_2_string(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if type(self.data[i][j]) == int or type(self.data[i][j]) == float:
                    self.data[i][j] = str(self.data[i][j])

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("               [Elevation]\n")
        for i in self.data:
            file.write("                  Data = " + ", ".join(i) + "\n")
        file.write("               EndSect  // Elevation\n\n")


class ReservoirData(object):
    def __init__(self, parent=None):
        self.data = {}
        self.elevation = None
        self.end = "EndSect  // ReservoirData"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data[name] = string_list[1:]

    def values_2_string(self):
        for i in self.data:
            for j in range(len(self.data[i])):
                if type(self.data[i][j]) == int or type(self.data[i][j]) == float:
                    self.data[i][j] = str(self.data[i][j])

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("            [ReservoirData]\n")
        for i in self.data:
            file.write("               " + i + " = " + ", ".join(self.data[i]) + "\n")
        self.elevation.print_to_nwk(file)
        file.write("            EndSect  // ReservoirData\n\n")


class LevelWidth(object):
    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Level_Width"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data.append(string_list[1:])

    def values_2_string(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if type(self.data[i][j]) == int or type(self.data[i][j]) == float:
                    self.data[i][j] = str(self.data[i][j])

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("               [Level_Width]\n")
        for i in self.data:
            file.write("                  Data = " + ", ".join(i) + "\n")
        file.write("               EndSect  // Level_Width\n\n")


class Irregular(object):
    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Irregular"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data.append(string_list[1:])

    def values_2_string(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if type(self.data[i][j]) == int or type(self.data[i][j]) == float:
                    self.data[i][j] = str(self.data[i][j])

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("               [Irregular]\n")
        for i in self.data:
            file.write("                  Data = " + ", ".join(i) + "\n")
        file.write("               EndSect  // Irregular\n\n")


class Geometry(object):
    def __init__(self, parent=None):
        self.irregular = None
        self.levelWidth = None
        self.data = {}
        self.end = "EndSect  // Geometry"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data[name] = string_list[1:]

    def values_2_string(self):
        for i in self.data:
            for j in range(len(self.data[i])):
                if type(self.data[i][j]) == int or type(self.data[i][j]) == float:
                    self.data[i][j] = str(self.data[i][j])

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("            [Geometry]\n")
        for i in self.data:
            file.write("               " + i + " = " + ", ".join(self.data[i]) + "\n")
        if self.irregular:
            self.irregular.print_to_nwk(file)
        elif self.levelWidth:
            self.levelWidth.print_to_nwk(file)
        file.write("            EndSect  // Geometry\n\n")


class Weir(object):
    def __init__(self, parent=None):
        self.reservoir = None
        self.geometry = None
        self.weirParams = {}
        self.end = "EndSect  // weir_data"
        self.parent = parent

    def add_parameters(self, string_list, name, line):

        if "Location" in line:
            self.riverName = string_list[1]
            self.km = float(string_list[2])
            self.topoID = string_list[3]
            self.ID = string_list[4]  # sprawdzic wartosci

        elif name in ["HorizOffset", "Attributes", "HeadLossFactors",
                      "WeirFormulaParam", "WeirFormula2Param", "WeirFormula3Param"]:
            self.weirParams[name] = string_list[1:]

        # else:
        # print(u"Blad funkcji addParameters klasy weir:")
        # print(line)

    def values_2_string(self):
        for i in self.weirParams:
            for j in range(len(self.weirParams[i])):
                if type(self.weirParams[i][j]) == int or type(self.weirParams[i][j]) == float:
                    self.weirParams[i][j] = str(self.weirParams[i][j])

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("         [weir_data]\n")
        file.write("            Location = '{0}', {1}, '{2}', '{3}'\n".format(self.riverName, self.km,
                                                                              self.topoID, self.ID))
        self.reservoir.print_to_nwk(file)
        for i in self.weirParams:
            file.write("            " + i + " = " + ", ".join(self.weirParams[i]) + "\n")
        self.geometry.print_to_nwk(file)
        file.write("            [QH_Relations]\n            EndSect  // QH_Relations\n\n \
                            EndSect  // weir_data\n\n")


class Culvert(object):
    def __init__(self, parent=None):
        self.reservoir = None
        self.geometry = None
        self.culvertParams = {}
        self.end = "EndSect  // culvert_data"
        self.parent = parent

    def add_parameters(self, string_list, name, line):

        if "Location" in line:
            self.riverName = string_list[1]
            self.km = float(string_list[2])
            self.ID = string_list[3]
            self.topoID = string_list[4]

        elif name in ["HorizOffset", "Attributes", "HeadLossFactors"]:
            self.culvertParams[name] = string_list[1:]

        # else:
        # print(u"Blad funkcji addParameters klasy weir:")
        # print(line)

    def values_2_string(self):
        for i in self.culvertParams:
            for j in range(len(self.culvertParams[i])):
                if type(self.culvertParams[i][j]) == int or type(self.culvertParams[i][j]) == float:
                    self.culvertParams[i][j] = str(self.culvertParams[i][j])

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("         [culvert_data]\n")
        file.write("            Location = '{0}', {1}, '{2}', '{3}'\n".format(self.riverName, self.km,
                                                                              self.ID, self.topoID))
        self.reservoir.print_to_nwk(file)
        file.write("            HorizOffset = " + ", ".join(self.culvertParams["HorizOffset"]) + "\n")
        file.write("            Attributes = " + ", ".join(self.culvertParams["Attributes"]) + "\n")
        self.geometry.print_to_nwk(file)
        file.write("            HeadLossFactors = " + ", ".join(self.culvertParams["HeadLossFactors"]) + "\n")
        file.write("            [Flow_Conditions]\n               [QHRelations_Positive_Flow]\n \
              EndSect  // QHRelations_Positive_Flow\n\n \
              [QHRelations_Negative_Flow]\n \
              EndSect  // QHRelations_Negative_Flow\n\n \
              [Hydraulic_Parameters]\n \
              EndSect  // Hydraulic_Parameters\n\n \
              [OrificeCoef_Positive_Flow] \n \
              EndSect  // OrificeCoef_Positive_Flow\n\n \
              [OrificeCoef_Negative_Flow]\n \
              EndSect  // OrificeCoef_Negative_Flow\n\n \
           EndSect  // Flow_Conditions\n\n \
        EndSect  // culvert_data\n\n")


class CrossSection(object):
    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Cross_Section"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data.append([string_list[1], string_list[2]])

    def values_2_string(self):
        '''change data types from int or float to string'''
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if type(self.data[i][j]) == int or type(self.data[i][j]) == float:
                    self.data[i][j] = str(self.data[i][j])


    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("            [Cross_Section]\n")
        for i in self.data:
            file.write("               Data = " + ", ".join(i) + "\n")
        file.write("            EndSect  // Cross_Section\n\n")


class LinkChannel(object):
    def __init__(self, parent=None):
        self.crossSection = None
        self.end = "EndSect  // linkchannel"
        self.parent = parent

    def add_parameters(self, string_list, name, line):

        if "Geometry" in line:
            self.geometry = string_list[1:]

        elif "HeadLossFactors" in line:
            self.HeadLossFactors = string_list[1:]

        elif "Bed_Resistance" in line:
            self.BedResistance = string_list[1:]

        # else:
        # print(u"Blad funkcji addParameters klasy linkChannel:")
        # print(line)

    def values_2_string(self):
        for i in range(len(self.geometry)):
            if type(self.geometry[i]) == int or type(self.geometry[i]) == float:
                self.geometry[i] = str(self.geometry[i])

        for i in range(len(self.HeadLossFactors)):
            if type(self.HeadLossFactors[i]) == int or type(self.HeadLossFactors[i]) == float:
                self.HeadLossFactors[i] = str(self.HeadLossFactors[i])

        for i in range(len(self.BedResistance)):
            if type(self.BedResistance[i]) == int or type(self.BedResistance[i]) == float:
                self.BedResistance[i] = str(self.BedResistance[i])

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("         [linkchannel]\n")
        file.write("            Geometry = " + ", ".join(self.geometry) + "\n")
        file.write("            HeadLossFactors = " + ", ".join(self.HeadLossFactors) + "\n")
        file.write("            Bed_Resistance = " + ", ".join(self.BedResistance) + "\n")

        if self.crossSection:
            self.crossSection.print_to_nwk(file)

        file.write("            [QH_Relations]\n")
        file.write("""            EndSect  // QH_Relations\n\n         EndSect  // linkchannel\n\n""")


class Branch(object):
    def __init__(self, parent=None):
        self.pointList = []
        self.linkChannel = None
        self.end = "EndSect  // branch"
        self.parent = parent

    def add_parameters(self, string_list, name, line):

        if "definitions" in line:
            self.riverName = string_list[1]
            self.topoID = string_list[2]
            self.val1 = int(string_list[3])
            self.val2 = float(string_list[4])
            self.val3 = int(string_list[5])
            self.val4 = int(string_list[6])
            self.val5 = int(string_list[7])

        elif "connections" in line:
            if string_list[1] == '':
                self.connectRiver = " "
                self.point = "-1e-155"
                self.connectTopoID = " "
                self.point2 = "-1e-155"
            else:
                self.connectRiver = string_list[1]
                self.point = float(string_list[2])  # sprawdzić czy float czy int
                self.connectTopoID = string_list[3]
                self.point2 = float(string_list[4])  # sprawdzić czy float czy int

        elif "points" in line:
            self.pointList.extend(string_list[1:])
        # else:
        # print(u"Blad funkcji addParameters klasy branch:")
        # print(line)

    def values_2_string(self):
        dataDict = self.__dict__
        for i in dataDict:
            if type(dataDict[i]) == int or type(dataDict[i]) == float:
                dataDict[i] = str(dataDict[i])

        for i in range(len(self.pointList)):
            if type(self.pointList[i]) == int or type(self.pointList[i]) == float:
                self.pointList[i] = str(self.pointList[i])

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        file.write("      [branch]\n")
        file.write("        definitions = '{0}', '{1}', "
                   "{2}, {3}, {4}, {5}, {6}\n".format(self.riverName, self.topoID, self.val1,
                                                      self.val2, self.val3, self.val4, self.val5))

        file.write("        connections = '{0}', {1}, "
                   "'{2}', {3}\n".format(self.connectRiver, self.point,
                                         self.connectTopoID, self.point2))

        file.write("        points = " + ", ".join(self.pointList)+"\n")

        if self.linkChannel:
            self.linkChannel.print_to_nwk(file)

        file.write("      EndSect  // branch\n\n")


class NwkFile(object):
    def __init__(self):
        self.pointList = []
        self.branchList = []
        self.weirList = []
        self.culvertList = []
        self.start = ''
        self.finish = ''
        self.maxPoint = 0
        self.end = None

    def add_start(self, value):
        self.start = self.start + value

    def add_point(self, string_list, name):
        no = int(string_list[1])
        x = float(string_list[2])
        y = float(string_list[3])
        val1 = int(string_list[4])
        val2 = float(string_list[5])
        val3 = int(string_list[6])

        if no > self.maxPoint:
            self.maxPoint = no

        self.pointList.append(NwkPoint(no, x, y, val1, val2, val3))

    def check_points_numbers(self):
        self.recuredPointList = []
        for i in self.pointList:
            self.recuredPointList.append(i.no)
        for i in self.recuredPointList:
            if self.recuredPointList.count(i) > 1:
                print("Powtarzające się punkty: ", i, u"w liczbie ", self.recuredPointList.count(i))

    def values_2_string(self):
        pass

    def nwk_rdp(self, epsilon=0.08):
        '''
        self.pointsToRdp = []
        for i in self.pointList:
            self.pointsToRdp.append([float(i.x), float(i.y)])
        '''
        self.pointsToRdp = [[i.x, i.y] for i in self.pointList]
        try:
            from rdp import rdp
        except:
            print(u"nie można zaimportować modułu do RDP")
            pass

        self.rdpOutList = rdp(self.pointsToRdp, epsilon=epsilon)
        self.pointsToRemove = []
        i = 0

        while i < len(self.pointList):
            usunac = True
            for j in self.rdpOutList:
                if self.pointList[i].x == j[0] and self.pointList[i].y == j[1]:
                    usunac = False

            if usunac:
                self.pointsToRemove.append(self.pointList[i].no)
                del self.pointList[i]
                usunac = False
            else:
                i += 1

        for i in self.branchList:
            j = 0
            while j < len(i.pointList):
                if i.pointList[j] in self.pointsToRemove:

                    del i.pointList[j]
                else:
                    j += 1

    def sort_points(self):
        slownik = {}
        for j, i in enumerate(self.pointList):
            slownik[i.no] = j+1
            i.no = j+1

        for i in self.branchList:
            for j in range(len(i.pointList)):
                numer = i.pointList[j]
                i.pointList[j] = slownik[numer]

    def print_to_nwk(self, file):
        '''write parameters to *.nwk file'''
        file.write(self.start)
        file.write("   [POINTS]\n")
        for i in self.pointList:
            i.values_2_string()
            file.write("      point = {0}, {1}, "
                       "{2}, {3}, {4}, {5}\n".format(i.no, i.x, i.y, i.val1, i.val2, i.val3))
        file.write("   EndSect  // POINTS\n\n   [BRANCHES]\n")

        for i in self.branchList:
            i.print_to_nwk(file)
        if len(self.finish) > 2:
            file.write("""   EndSect  // BRANCHES\n\n   [STRUCTURE_MODULE]\n      \
            Structure_Version = 1, 1\n\n\n      [WEIR]\n""")

            for i in self.weirList:
                i.print_to_nwk(file)

            file.write("""      EndSect  // WEIR\n\n      [CULVERTS]\n""")

            for i in self.culvertList:
                i.print_to_nwk(file)

            file.write(self.finish)
        elif len(self.finish) < 2:
            file.write("""   EndSect  // BRANCHES

      [STRUCTURE_MODULE]
      Structure_Version = 1, 1
      [CROSSSECTIONS]
         CrossSectionDataBridge = 'xns11'
         CrossSectionFile = |.|
      EndSect  // CROSSSECTIONS
   EndSect  // STRUCTURE_MODULE

EndSect  // MIKE_11_Network_editor""")

# BRIDGES ----------------------------------------------------------------------------------------------------------------
class bridge_xs(object):
    def __init__(self, sheet):
        # zaczytanie pojedynczych wartosci
        self.rzeka = sheet.cell(row=1, column=2).value
        self.data = sheet.cell(row= 2, column=2).value
        self.typ = sheet.cell(row=3, column=2).value
        self.lp = sheet.cell(row=4, column=2).value
        self.dl = sheet.cell(row=5, column=2).value
        self.upS = sheet.cell(row=6, column=2).value
        self.downS = sheet.cell(row=7, column=2).value
        self.topoID = sheet.cell(row=8, column=2).value
        self.km = sheet.cell(row=9, column=2).value
        self.mann = sheet.cell(row=9, column=4).value
        self.koryto = []
        self.przepust = []
        self.przelew = []

        # zaczytanie serii danych
        # koryto
        i = 11
        stat = sheet.cell(row=i, column=1).value
        while stat != None:
            self.koryto.append([sheet.cell(row=i, column=1).value, sheet.cell(row=i, column=2).value])
            i += 1
            stat = sheet.cell(row=i, column=1).value
        # przepust
        i = 11
        stat = sheet.cell(row=i, column=3).value
        while stat != None:
            self.przepust.append([sheet.cell(row = i, column = 3).value, sheet.cell(row = i, column = 4).value])
            i+=1
            stat = sheet.cell(row=i, column=3).value
        # przelew
        i = 11
        stat = sheet.cell(row=i, column=5).value
        while stat != None:
            self.przelew.append([sheet.cell(row=i, column=5).value, sheet.cell(row=i, column=6).value])
            i += 1
            stat = sheet.cell(row=i, column=5).value

class point(object):
    def __init__(self, lp, x, y, z, kod="nul", cos="nul", ogon='nul'):
        self.lp = int(float(lp.replace("o","0").replace("O","0").replace("a","").replace("A","")))
        self.x = float(x.replace("o", "0").replace("O", "0"))
        self.y = float(y.replace("o", "0").replace("O", "0"))
        self.z = float(z.replace("o", "0").replace("O", "0"))
        self.kod = str(kod)
        self.cos = [cos]

class XS_t(object):
    def __init__(self, file):
        name = str(file).replace("\\", " ").split()[-3]
        name = name.replace(".", " ").replace("_", " ").split()
        for element in name:
            if element[0].isdigit():
                name = element
        self.name = name
        self.km = 0
        self.rzeka = "Riv"
        self.data = "01.01.1990"
        self.type = "none"
        self.dane = []
        self.point_data = []
        self.geom2 = []
        for line in file.read().split("\n"):
            napis = list(line.replace("\t", "  "))
            licznik = 0
            while licznik < len(napis):
                if napis[licznik] == ' ':
                    try:
                        while napis[licznik + 1] == ' ':
                            del napis[licznik]
                    except:
                        pass
                licznik += 1
            napis = "".join(napis).replace('*', '').replace('\r\n','')  # koniec usuwania powielonych znakow podzialu, zamiana listy na string
            line2 = napis.replace("\t"," ").replace("  "," ")
            numbers = sum(c.isdigit() for c in line2)
            if numbers < 14:
                self.dane.append(line2)

            else:
                line3 = line2.split(' ')
                if len(line3) > 6:
                    cos = line3[6:]
                    line3 = line3[:6]
                    line3.append(cos)
                #print(line3)
                try:
                    int(float(line3[0]))
                    self.point_data.append(point(*line3[:]))
                except:
                    #print('----')
                    #print(line3)
                    #print('----')
                    self.point_data.append(point(*line3[1:]))

        r = 0
        while sum(c.islower() for c in self.dane[r]) < 1:
            r+=1
        if "rzek" in str.lower(self.dane[r]) or "zeka" in str.lower(self.dane[0]):
            self.rzeka = self.dane[r].split(':')[1].replace(' ', '')
        else:
            print("Brak: river def", self.lp)
        if "przek" in str.lower(self.dane[r+1]) or "rzekr" in str.lower(self.dane[1]):
            self.lp = self.dane[r+1].split(':')[1]
        else:
            print("Brak: lp def", self.lp)
        if "dat" in str.lower(self.dane[r+2]) or "ata" in str.lower(self.dane[2]):
            self.data = self.dane[r+2].split(':')[1].replace(' ', '')
        else:
            print("Brak: data def", self.lp)
        if "typ" in str.lower(self.dane[r+3]) or "most" in str.lower(self.dane[3]):
            self.type = self.dane[r+3].split(':')[1].replace(' ', '')
        elif "typ" in str.lower(self.dane[r+4]) or "most" in str.lower(self.dane[4]):
            self.type = self.dane[r + 4].split(':')[1].replace(' ', '')
            #self.kat = self.dane[r + 3].split(':')[1]

        try:
            if "foto" in str.lower(self.dane[r+4]):
                self.foto = self.dane[r+4].split(':')[1]
        except:
            pass
        try:
            if "admin" in str.lower(self.dane[r+5]):
                self.admin = self.dane[r+5].split(':')[1]
        except:
            self.admin = "None"
        try:
            if "uwagi" in str.lower(self.dane[r+6]):
                self.uwagi = self.dane[r+6].split(':')[1]
        except:
            self.uwagi = "None"
        try:
            if "szer" in str.lower(self.dane[r+7]):
                self.szer = self.dane[r+7].split(':')[1]
        except:
            self.szer = "None"


        if self.type == "none" or self.type == '':
            #print("Brak: type def", self.lp)
            try:
                if "obie" in str(self.dane[-4:-1]).lower():
                    self.type = "obiekt"
                else:
                    kody = []
                    for k in self.point_data:
                        kody.append(k.kod)
                    napis = str(kody)
                    if '40' in napis:
                        self.type = "obiekt"
                    else:
                        pass
            except:
                pass
    def get_far(self):
        print(self.name)
        line = []
        for poi in self.point_data:
            #print(poi.cos, poi.x, poi.y)
            if "zww" in str(poi.cos).lower():
                line.append(poi.x)
                line.append(poi.y)
        return(line[0],line[1],line[2],line[3])

    def distance(self):
        self.pierwszy_punkt = self.point_data[0]
        self.pozost_punkty = self.point_data[1:]
        self.punkty_odleglosci = {}
        self.sortowane = []
        x1, y1, z1 = self.pierwszy_punkt.xp, self.pierwszy_punkt.yp, self.pierwszy_punkt.z
        for i in self.point_data:
            x2, y2, z2 = i.xp, i.yp, i.z
            dx = math.fabs(x2 - x1)
            dy = math.fabs(y2 - y1)
            dist = math.sqrt((dx**2) + (dy**2))
            i.dist = dist
    def dist_sort(self):
        self.point_data = sorted(self.point_data, key=operator.attrgetter('dist'))

    def get_avarage_manning(self):
        flag = 0
        n = l = 0
        dataBase = shelve.open(r'dane.dbm')
        dict = dataBase['dictKodManning']
        for pktNumber in range(len(self.point_data)-2):
            if 'zww' in str(self.point_data[pktNumber].cos).lower():
                flag += 1
            if flag != 1:
                continue
            odl = float(distance(self.point_data[pktNumber].x, self.point_data[pktNumber+1].x, self.point_data[pktNumber].y,
                     self.point_data[pktNumber + 1].y))
            manning = float(dict.get(self.point_data[pktNumber].kod, 0))
            if manning:
                n += odl * manning
                l += odl
        self.avManning = n/l

    def get_km(self, pkt):
        for pktNumber in range(len(self.point_data) - 2):
            for pktNwkNumber in range(len(pkt) - 2):
                x, y, line1, line2 = line_intersection(self.point_data[pktNumber].x, self.point_data[pktNumber + 1].x,
                                                       self.point_data[pktNumber].y, self.point_data[pktNumber + 1].y,
                                                       pkt[pktNwkNumber].x, pkt[pktNwkNumber].y, pkt[pktNwkNumber + 1].x,
                                                       pkt[pktNwkNumber+1].y)
                if line1 and line2:
                    km = pkt[pktNwkNumber].val2 + distance(pkt[pktNwkNumber].x, pkt[pktNwkNumber].y, x, y)
                    self.km = km
                    return km
        self.km = None
        return None
                ################################################################################################################
    """obliczanie dlugosci przekroju i dolnej pikiety"""
    def get_culver_len(self):

        for pkt in self.point_data:
            if "66" in pkt.kod or "7d" in pkt.kod or "7" in pkt.kod:
                print(pkt.y, pkt.xp, pkt.x, pkt.yp)
                self.culvert_len = math.sqrt((float(pkt.y) - float(pkt.xp)) ** 2 + (float(pkt.x) - float(pkt.yp)) ** 2)
                self.culvert_downS = pkt.z

    '''generuje punkty przeciecia'''
    def gen_pkt(self):
        if len(self.geom) == 0:
            print("geom error")
            time.sleep(5)
            self.geom = self.geom2
        '''jesli jeden pkt spodu konstrukcji dodanie pomocniczych'''
        if len(self.geom) == 1:
            self.geom.insert(0,[self.geom[0][0] - 0.5, self.geom[0][1]])
            self.geom.append([self.geom[0][0] + 0.5, self.geom[0][1]])
        '''jesli wiecej niz jeden punkt opisujacy zpod konstrukcji, tworzy liste punktow przeciecia prostych z konstrukcji na lini koryta'''
        if len(self.geom) > 1:
            pointLis = []
            for i in range(len(self.kor) - 1):
                for x in range(len(self.geom) - 1):
                    point = list(line_intersection(self.kor[i][0], self.kor[i][1], self.kor[i + 1][0],
                                              self.kor[i + 1][1], self.geom[x][0], self.geom[x][1],
                                              self.geom[x + 1][0], self.geom[x + 1][1]))
                    if point[-1] == True:
                        pointLis.append(point)
            print("line 312 point len: ", len(pointLis))
            '''obliczenie odleglosci wygenerowanych punktow od punktow skrajnych konstrukcji'''
            for pkt in pointLis:
                if self.geom[0] == self.geom[-1]:
                    raise ('kryzys 2')
                dis1 = distance(self.geom[0][0], pkt[0], self.geom[0][1], pkt[1])
                pkt.append(dis1)
                dis2 = distance(self.geom[-1][0], pkt[0], self.geom[-1][1], pkt[1])
                pkt.append(dis2)

            """wybor punktow najblizszych, z usunieciem prawa lewa"""  ##################################################
            """sredni station dla konstrukcji"""
            midle_station = []
            for i in range(len(self.geom)):
                midle_station.append(self.geom[i][0])
            midle_station = sum(midle_station) / float(len(midle_station))
            """dwie listy pkt sprzed i za sredniej"""
            left_l2 = []
            right_l2 = []
            for i in range(len(pointLis)):
                if pointLis[i][0] > midle_station:
                    right_l2.append(pointLis[i])
            for i in range(len(pointLis)):
                if pointLis[i][0] < midle_station:
                    left_l2.append(pointLis[i])
            """sortowanie po odleglosci od konca"""
            right_l = sorted(right_l2, key=itemgetter(-2))
            left_l = sorted(left_l2, key=itemgetter(-1))
            "sprawdzenie wystapienia przeciec po obu stronach"
            if len(left_l) < 1 or len(right_l) < 1:
                print("przeciecia po lewej: {}\nprzeciecia po prawej: {}".format(len(left_l), len(right_l)))
            if len(left_l) < 1:
                z = self.geom[0][1]
                stat = self.kor[0][0]
                print(z,stat)
                left_l.insert(0, [stat,z, False, False, 0,0])
            if len(right_l) < 1:
                z = self.geom[-1][1]
                stat = self.kor[-1][0]
                print(z, stat)
                right_l.append([stat, z, False, False, 0,0])
                #time.sleep(5)
            """przypisanie konkretnych punktow R i L"""
            pointR = right_l[0]
            pointL = left_l[0]
        return pointR, pointL

        ### funkcja tworzaca obiekt typu culvert z przekroju geodezyjnego
    def get_culvert(self):
        print(self.lp)
        self.geom = []
        self.deck = []
        self.kor = []
        self.kor_c = []
        '''podzial na pkt koryta i obiektu, pobranie najnizszego punktu z koryta'''
        self.culvert_upS = 1000
        for pkt in self.point_data:
            lista_geo = []
            if "40" not in str(pkt.kod) and "41" not in str(pkt.kod) and "42" not in str(pkt.kod) and "66" not in str(pkt.kod) and "7d" not in str(pkt.kod) and "50" not in str(pkt.kod) and "51" not in str(pkt.kod)and "52" not in str(pkt.kod)and "7" not in str(pkt.kod):
            #if "K" in str(pkt.kod) or "T" in str(pkt.kod) or pkt.kod == None:
                self.kor.append([float(pkt.dist), float(pkt.z)])
                if pkt.z < self.culvert_upS:
                    self.culvert_upS = pkt.z
            if "40" in str(pkt.kod):
                self.geom2.append([float(pkt.dist), float(pkt.z)])
            if "40" in str(pkt.kod): # and "None" in str(pkt.cos):
                self.geom.append([float(pkt.dist), float(pkt.z)])
            if "42" in str(pkt.kod):
                self.deck.append([float(pkt.dist), float(pkt.z)])
        '''algorytm do redukcji punktow, zmienia zageszczone zygzaki na prosta'''
        self.geom = rdp(self.geom, epsilon=0.8)
        self.deck = rdp(self.deck, epsilon=5)
        try:
            if self.geom[0][0] < self.geom[-1][0]:
                self.geom.reverse()
        except:
            pass
        pointR, pointL = self.gen_pkt()

        if pointR[-4] == True:
            dyst = pointR[0] - self.geom[0][0]
            new_elem=[]
            for element in self.geom:
                ele = element
                ele[0]=ele[0]+dyst
                new_elem.append(ele)
            self.geom = new_elem
            pointR, pointL = self.gen_pkt()
            print(pointR)
            print(dyst, 'R----')

        if pointL[-4] == True:
            dyst = pointL[0] - self.geom[-1][0]
            new_elem = []
            for element in self.geom:
                ele = element
                ele[0] = ele[0] + dyst
                new_elem.append(ele)
            self.geom = new_elem
            pointR, pointL = self.gen_pkt()
            print(pointL)
            print(dyst, 'L----')
        """jesli punkt lewy i prawy sa rowne error"""
        if pointL == pointR:
            print ('kryzys', pointL, pointR)
            print(self.geom)
            print(self.kor)
            print(pointLis)
        """dodanie punktow do geometri"""
        self.geom.append([pointL[0], pointL[1]])
        self.geom.insert(0, [pointR[0], pointR[1]])
        """uciecie koryta"""
        lewy = None
        prawy = None
        for i in range(len(self.kor)-1):
            if is_between(self.kor[i][0], self.kor[i][1], pointL[0], pointL[1], self.kor[i+1][0], self.kor[i+1][1]):
                lewy = i
        for i in range(len(self.kor)-1):
            if is_between(self.kor[i][0], self.kor[i][1], pointR[0], pointR[1], self.kor[i+1][0], self.kor[i+1][1]):
                prawy = i
        if lewy != None and prawy != None:
            self.kor_c = self.kor[lewy:prawy+1]
        elif lewy != None and prawy == None:
            self.kor_c = self.kor[lewy:]
        elif lewy == None and prawy != None:
            self.kor_c = self.kor[:prawy+1]
        """dodanie pkt tnacych do koryta"""
        self.kor_c.insert(0, [pointL[0], pointL[1]])
        self.kor_c.append([pointR[0], pointR[1]])
        wydruk_test = sorted(self.geom, key=itemgetter(-2))
        self.culvertXS = rdp(wydruk_test+self.kor_c, epsilon=0.0)#self.kor_c +
        print(self.get_culver_len(),"Len----")
        try:
            print("dlugosc obiektu: ",round(self.culvert_len, 2))
        except:
            pass

    def excel_print(self, workbook):
        worksheet = workbook.add_worksheet(str(self.name)+str(self.lp))
        bold = workbook.add_format({'bold': 1})
        headings = ['Koryto Stat','Koryto Elev', 'Przepust Stat', 'Przepust Elev', 'Przelew Stat', 'Przelew Elev']
        worksheet.write_row('A10', headings, bold)
        worksheet.write(0, 0, 'Rzeka:')
        worksheet.write(0, 1, str(self.rzeka))
        worksheet.write(1, 0, 'Data pom:')
        worksheet.write(1, 1, str(self.data))
        worksheet.write(2, 0, 'Typ:')
        worksheet.write(2, 1, str(self.type))
        worksheet.write(3, 0, 'Lp:')
        worksheet.write(3, 1, str(self.lp))
        try:
            worksheet.write(4, 0, 'Długość:')
            worksheet.write(4, 1, str(self.culvert_len))
            worksheet.write(5, 0, 'Upstream:')
            worksheet.write(5, 1, str(self.culvert_upS))
            worksheet.write(6, 0, 'Downstream:')
            worksheet.write(6, 1, str(self.culvert_downS))
        except:
            pass
        try:
            worksheet.write(0, 3, 'Foto:')
            worksheet.write(0, 4, str(self.foto))
        except:
            pass
        try:
            worksheet.write(1, 3, 'Admin:')
            worksheet.write(1, 4, str(self.admin))
        except:
            pass
        try:
            worksheet.write(2, 3, 'Uwagi:')
            worksheet.write(2, 4, str(self.uwagi))
        except:
            pass
        try:
            worksheet.write(3, 3, 'Szer:')
            worksheet.write(3, 4, str(self.szer))
        except:
            pass

        chart1 = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
        for row, line in enumerate(self.kor):
            for col, cell in enumerate(line):
                worksheet.write(row+10, col, cell)

        chart1.add_series({
            'name': 'Koryto',
            'categories': [self.name+str(self.lp), 10, 0, row+10, 0],
            'values': [self.name+str(self.lp), 10, 1, row+10, 1],
        })

        for row, line in enumerate(self.culvertXS):
            for col, cell in enumerate(line):
                worksheet.write(row+10, col+2, cell)

        chart1.add_series({
            'name': 'Przepust',
            'categories': [self.name+str(self.lp), 10, 2, row + 10, 2],
            'values': [self.name+str(self.lp), 10, 3, row + 10, 3],
        })
        for row, line in enumerate(self.deck):
            for col, cell in enumerate(line):
                worksheet.write(row+10, col+4, cell)
        chart1.add_series({
            'name': 'Przelew',
            'categories': [self.name+str(self.lp), 10, 4, row + 10, 4],
            'values': [self.name+str(self.lp), 10, 5, row + 10, 5],
        })
        chart1.set_style(10)
        chart1.set_size({'width': 720, 'height': 576})
        worksheet.insert_chart('G1', chart1, {'x_offset': 25, 'y_offset': 15})
        #workbook.close()


# LINKI ---------------------------------------------------------------------------------------------------------------
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

class Link(object):
    def __init__(self, object1, object2):
        self.object1 = object1
        self.object2 = object2
        self.pkt = []
        self.river1 = object1.riverCode
        self.chain1 = object1.km
        self.river2 = object2.riverCode
        self.chain2 = object2.km
        self.rzad = 0
        self.kolej = 0
        self.main_chan = "Riv"
        self.main_km = 0
        self.main_site = "C"
        self.topo = "Topo"

    def data_definition(self, minDeltaH=0.51):
        self.main_km = int(self.main_km)
        if self.rzad == 0:
            print("brak przypisania")
            print(self.river1, self.chain1, self.river2, self.chain2)
        else:
            #if "LTZ" in self.object1.river_code or "LTZ" in self.object2.river_code:
                #self.main_site = "L"
            #elif "PTZ" in self.object1.river_code or "PTZ" in self.object2.river_code:
                #self.main_site = "P"
            if self.kolej == 1:
                self.main_site = "L"
                self.connections = [self.object1.riverCode, self.object1.km, self.object2.riverCode, self.object2.km]
                x1, y1, x2, y2 = get_xy_delta(self.object1)

            elif self.kolej == 2:
                self.main_site = "P"
                self.connections = [self.object2.riverCode, self.object2.km, self.object1.riverCode, self.object1.km]
                x2, y2, x1, y1 = get_xy_delta(self.object1)
            self.definitions = [
                "KP_" + str(self.rzad) + "_" + str(self.main_chan) + "_" + str(self.main_km) + "_" + self.main_site,
                self.topo, 0, 5, 0, 10000, 1]
            h_elev = float(max(self.object1.max_left, self.object2.max_right))
            h2_elev = float(self.object2.min_right)
            if h_elev-h2_elev < minDeltaH:
                h2_elev -= (minDeltaH-(h2_elev-h_elev))
            self.geometry = [h_elev, h2_elev]
            self.cross_section = [[0, 0], [0.1, float(self.object1.len)], [3, float(self.object1.len)]]
            self.points = [float(self.object1.left[0]) + x1, float(self.object1.left[1]) + y1,
                           float(self.object1.left[0]) + x2, float(self.object1.left[1]) + y2]

