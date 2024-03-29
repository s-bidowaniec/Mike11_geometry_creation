# -*- coding: utf-8 -*-
import shelve
import math, collections
from operator import itemgetter
from rdp import rdp
import time
import numpy as np
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
        self.station, self.z, self.manning, self.kod = float(line.split()[0]), float(line.split()[1]),line.split()[2],line.split()[3]
        #return '{} {}'.format(self.station, self.z)

class Xs(object):
    def __init__(self):
        self.dane = []
        self.points = []
        self.cs = 0
        self.mann = 0.04
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
            file.write(str('RESISTANCE NUMBERS\r\n   2  1     {}     1.000     1.000    1.000    1.000\r\n').format(self.mann))
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
    '''object hold on data for one point from *.nwk file:
    point = 2489, 317086.86, 368728.92, 0, 24686.81917468862, 0'''

    def __init__(self, no, x, y, val1, val2, val3, z=None):
        self.no = no        # number of point
        self.x = x          # x coordinate
        self.y = y          # y coordinate
        self.val1 = val1    # value1
        self.val2 = val2    # value2
        self.val3 = val3    # value3
        self.z = z          # z level
        self.end = None     # final part from *.nwk file, not used in processing

    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''
        dataDict = self.__dict__        # return dictionary {'variable1' : 'value1', 'variable2' : 'value2'...} from object variables
        for i in dataDict:
            if type(dataDict[i]) == int or type(dataDict[i]) == float:
                dataDict[i] = str(dataDict[i])


class Elevation(object):
    '''object hold on data for elevation in ReservoirData object'''

    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Elevation"
        self.parent = parent

    def add_paramaters(self, string_list, name, line):
        '''load parameters to object as list'''
        self.data.append(string_list[1:])

    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''
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
    '''object hold on data for ReservoirData in Weir and Culvert object
    data stored as dictionary {"CoordyXY" : [0, 0]...}'''

    def __init__(self, parent=None):
        self.data = {}
        self.elevation = None
        self.end = "EndSect  // ReservoirData"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        '''load parameters to object as dictionary, from "CoordXY = 0, 0" to {"CoordyXY" : [0, 0]}'''
        self.data[name] = string_list[1:]

    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''
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
    '''object hold on data for Level_Width in Geometry object
        data stored as lists in list [[128.09, 20], [129, 40], [130, 40]...]'''

    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Level_Width"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        '''load parameters to object as list, from "Data = 128.09, 20" to [[128.09, 20]...]'''

        self.data.append(string_list[1:])

    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''

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
    '''object hold on data for Irregular in Geometry object
    data stored as lists in list [[128.09, 20], [129, 40], [130, 40]...]'''

    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Irregular"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        '''load parameters to object as list'''
        self.data.append(string_list[1:])

    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''
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
    '''object hold on data for Geometry in Weir and Culvert objects
    have reference to Irregular and LevelWidth objects
    data stored as dictionary {"Rectangular" : [0, 0]...}'''
    def __init__(self, parent=None):
        self.irregular = None
        self.levelWidth = None
        self.data = {}
        self.end = "EndSect  // Geometry"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        '''load parameters to object as dictionary, from "Rectangular = 0, 0" to {"Rectangular" : [0, 0]}'''
        self.data[name] = string_list[1:]

    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''
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
    '''object hold on data for Weir in Nwk object,
    have reference to ReservoirData and Geometry object,
    weirParams stored as dictionary {"HeadLossFactors" : [0.5, 1, 1, 0.5, 1, 1]...}'''

    def __init__(self, parent=None):
        self.reservoir = None
        self.geometry = None
        self.weirParams = {}
        self.end = "EndSect  // weir_data"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        '''load parameters like riverName, km, topoID, ID to object,
        remaining parameters load to weirParams as dictionary,
        from "HeadLossFactors = 0.5, 1, 1, 0.5, 1, 1" to {"HeadLossFactors" : [0.5, 1, 1, 0.5, 1, 1]}
        missing [QH_Relations] parameters'''

        # add basic parameters for Wier
        if "Location" in line:
            self.riverName = string_list[1]
            self.km = float(string_list[2])
            self.topoID = string_list[3]
            self.ID = string_list[4]  # sprawdzic wartosci

        # add remaining parameters to weirParams
        elif name in ["HorizOffset", "Attributes", "HeadLossFactors",
                      "WeirFormulaParam", "WeirFormula2Param", "WeirFormula3Param"]:
            self.weirParams[name] = string_list[1:]


    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''
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
    '''object hold on data for Culvert in Nwk object,
    have reference to ReservoirData and Geometry object,
    culvertParams stored as dictionary {"Attributes" : [108.28, 108.32, 9, 0.031, 1, 0, 0]...}'''

    def __init__(self, parent=None):
        self.reservoir = None
        self.geometry = None
        self.culvertParams = {}
        self.end = "EndSect  // culvert_data"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        '''load parameters like riverName, km, topoID, ID to object,
        remaining parameters load to culvertParams as dictionary,
        from "Attributes = 108.28, 108.32, 9, 0.031, 1, 0, 0" to {"Attributes" : [108.28, 108.32, 9, 0.031, 1, 0, 0]}
        missing Flow_Conditions parameters'''

        # add basic parameters for Culvert
        if "Location" in line:
            self.riverName = string_list[1]
            self.km = float(string_list[2])
            self.ID = string_list[3]
            self.topoID = string_list[4]

        # add remaining parameters to culvertParams
        elif name in ["HorizOffset", "Attributes", "HeadLossFactors"]:
            self.culvertParams[name] = string_list[1:]


    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''
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

############################      TU SKONCZYLEM      ####################################################

class Bridge(object):
    '''hold on data for bridge'''        #   do poprawki
    def __init__(self, parent = None):
        self.parent = parent
        self.data = ''
        self.spaceName = []
        self.end = "EndSect  // bridge_data"

    def add_parameters(self, string_list, name, line):
        '''add parameter to class'''
        wordsList = line.split()
        if u"BranchName" in line:
            self.branchName = string_list[-1]
        elif "Chainage" in line:
            self.chainage = string_list[-1]
        elif " ID" in line:
            self.ID = string_list[-1]
        elif "TopoID" in line:
            self.topoID = string_list[-1]
        elif " Type" in line:
            self.type = string_list[-1]
        elif "ChannelWidth" in line:
            self.channelWidth = string_list[-1]
        elif "SectionArea" in line:
            self.sectionArea = string_list[-1]
        elif "DragCoef" in line:
            self.dragCoef = string_list[-1]
        elif "CConst" in line:
            self.cConst = string_list[-1]
        elif "UpstreamWidth" in line:
            self.upstreamWidth = string_list[-1]
        elif "TotalWidth" in line:
            self.totalWidth = string_list[-1]
        elif "BridgeID" in line:
            self.bridgeID = string_list[-1]
        elif "CulvertRow" in line:
            self.culvertRow = string_list[-1]
        elif "WeirRow" in line:
            self.weirRow = string_list[-1]
        elif "HorizOffset" in line:
            self.horizonOffset = string_list[-1]
        elif "[" in line:                               # jeżeli występuje nazwa w nawiasie kwadratowym jest to początek nowej "sekcji" w pliku *.nwk
            self.data += line
            self.spaceName.append(name[1:-1])           # dodanie nazwy do listy
        elif wordsList[-1] in self.spaceName:         # jeżeli kończy się sekcja
            self.data += line
            self.data += '\n'                           # do napisu z danymi dokłada się jedną wolną linijkę
            del self.spaceName[self.spaceName.index(wordsList[-1])]     # usunięcie nazwy z listy
        else:
            self.data += line

    def values_2_string(self):
        for i in self.__dict__:
            if type(self.__dict__[i]) == int or type(self.__dict__[i]) == float:
                self.__dict__[i] == str(self.__dict__[i])

    def print_to_nwk(self, fil):
        '''write parameters to *.nwk file'''
        self.values_2_string()
        fil.write("         [bridge_data]\n")
        for i in self.__dict__:
            if i not in 'data parent end, spaceName':                  # tych atrybutów nie drukujemy
                upperName = i[0].upper() + i[1:]
                if i in 'branchName, ID, topoID':           # te atrybuty posiadają cudzysłowy w wydruku
                    fil.write("            {0} = '{1}'\n".format(upperName, self.__dict__[i]))
                else:
                    fil.write("            {0} = {1}\n".format(upperName, self.__dict__[i]))
        fil.write(self.data)
        fil.write('         ' + self.end + '\n\n')

    def new_bridge(self, branch, chainage, ID, tID, bID, culvertRow, weirRow, fil):
        self.branchName = branch
        self.chainage = chainage
        self.ID = ID
        self.topoID = tID
        self.type = 8
        self.channelWidth = 0
        self.sectionArea = 0
        self.dragCoef = 0
        self.cConst = 0
        self.upstreamWidth = 0
        self.totalWidth = 0
        self.bridgeID = bID
        self.culvertRow = culvertRow
        self.weirRow = weirRow
        self.horizonOffset = 0
        op = open(fil, 'r')
        rd = op.read()
        self.data = rd
        

class CrossSection(object):
    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Cross_Section"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data.append([string_list[1], string_list[2]])

    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''
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
        # print(linek)

    def values_2_string(self):
        '''change values from integer or float to string, useful to write to *.nwk file'''
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
        '''change values from integer or float to string, useful to write to *.nwk file'''
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
        self.bridgeList = []
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
            # dodano napis poniżej oraz pętlę
            file.write("""      EndSect  // CULVERTS	    

      [PUMPS]
      EndSect  // PUMPS

      [REGULATING_STR]
      EndSect  // REGULATING_STR

      [CONTROL_STR]
      EndSect  // CONTROL_STR

      [DAMBREAK_STR]
      EndSect  // DAMBREAK_STR

      [BRIDGE]\n""")

            for i in self.bridgeList:
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
        self.km = float(sheet.cell(row=9, column=2).value)
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
    def __init__(self, lp, x, y, z, odlRed=0, kod=0,  cos=0,znacznik=0,  ogon='nul'):
        self.lp = int(float(lp.replace("o","0").replace("O","0").replace("a","").replace("A","")))
        self.x = float(x.replace("o", "0").replace("O", "0"))
        self.y = float(y.replace("o", "0").replace("O", "0"))
        self.z = float(z.replace("o", "0").replace("O", "0"))
        self.odlRed = odlRed
        self.kod = str(kod)
        self.cos = cos
        self.znacznik = znacznik

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
            if numbers < 14 or '.jpg' in napis.lower():
                self.dane.append(line2)

            else:
                line3 = line2.split(' ')
                if len(line3) > 8:
                    cos = line3[8:]
                    line3 = line3[:8]
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
            print(poi.cos, poi.x, poi.y)
            if "zww" in str(poi.kod).lower():
                line.append(poi.x)
                line.append(poi.y)

        if len(line) < 2:
            line = [self.point_data[0].x, self.point_data[0].y, self.point_data[-1].x, self.point_data[-1].y]
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
            if "66" in pkt.kod or "7d" in pkt.kod or "7" in pkt.kod or "9" in str(pkt.znacznik):
                #print(pkt.y, pkt.xp, pkt.x, pkt.yp)
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
        self.manning = []
        self.geom = []
        self.deck = []
        self.kor = []
        self.culver_bottom = []
        self.culvert_top = []
        self.culvert_common = []
        self.culvert_special = []
        self.zww = []
        self.zwwDoKM = []
        '''podzial na pkt koryta i obiektu, pobranie najnizszego punktu z koryta'''
        self.culvert_upS = 1000
        # pobranie koryta w zakresie budowli
        flag = 0
        for pkt in self.point_data:
            print(pkt.kod, pkt.znacznik)
            if "10" in str(pkt.znacznik) and not '1' == str(pkt.kod) and not '12' == str(pkt.kod) and not '41' == str(pkt.kod):
                flag += 1
                # dodanie do zestawu pkt wspolnych koyto przepust
                self.culvert_common.append([float(pkt.dist), float(pkt.z)])

            if 0 == int(float(pkt.znacznik)) or 10 == int(float(pkt.znacznik)):
                self.culver_bottom.append([float(pkt.dist), float(pkt.z)])

                # sprawdzenie przyrastającego x
                if len(self.kor) > 1:
                    if self.kor[-1][0] < float(pkt.dist):
                        self.kor.append([float(pkt.dist), float(pkt.z)])
                    elif self.kor[-1][0] == float(pkt.dist):
                        self.kor.append([float(pkt.dist)+0.01, float(pkt.z)])
                    else: #if self.kor[-1][0] > float(pkt.dist):
                        delta = self.kor[-1][0] - float(pkt.dist)
                        odl_ostatnich_pkt = self.kor[-1][0] - self.kor[-2][0]
                        if delta/2 < odl_ostatnich_pkt:
                            self.kor[-1][0] -= delta/2
                            self.kor.append([float(pkt.dist)+delta/2, float(pkt.z)])
                        else: #if delta/2 >= odl_ostatnich_pkt:
                            self.kor[-1][0] -= odl_ostatnich_pkt / 2
                            self.kor.append([float(pkt.dist) + delta - odl_ostatnich_pkt / 2, float(pkt.z)])
                else:
                    self.kor.append([float(pkt.dist), float(pkt.z)])
                if "K" in pkt.cos:
                    self.manning.append(pkt.cos)
                if pkt.z < self.culvert_upS:
                    self.culvert_upS = pkt.z

            # pobranie spodu konstrukcji
            if "40" in str(pkt.kod) and 1 == int(float(pkt.znacznik)):
                self.culvert_top.append([float(pkt.dist), float(pkt.z)])
            # markery specjalne
            if "43" in str(pkt.kod) and 1 == int(float(pkt.znacznik)):
                self.culvert_special.append([float(pkt.dist), float(pkt.z)])
            # pobranie gory konstrukcji
            if "41" in str(pkt.kod):
                self.deck.append([float(pkt.dist), float(pkt.z)])
            if "zww" in str(pkt.kod).lower():
                self.zww.append([float(pkt.dist), float(pkt.z)])
                self.zwwDoKM.append(pkt)
        #self.kor = self.culver_bottom

        if len(self.culvert_top) == 1 and len(self.culvert_special) == 0:
            if len(self.culvert_common) < 2:
                self.culvert_special = self.zww
            else:
                self.culvert_special = self.culvert_common

        if len(self.culvert_top) <= 3 and len(self.culvert_special) > 0:
            szczyt = max(self.culvert_top, key=lambda x: x[1])
            left = self.culvert_special[0]
            right = self.culvert_special[-1]
            array = [left, szczyt, right]
            funkcja_kwadratowa = linear_equation(array)
            dist = (right[0]-left[0])/7
            stat = left[0]+dist
            print("---", stat, dist, "---")
            for station in range(6):
                self.culvert_top.append([stat, funkcja_kwadratowa(stat)])
                stat += dist
            self.culvertXS = list(sorted(self.culvert_top+self.culvert_special))+list(reversed(self.culver_bottom[1:-1]))
        # wersja dla pojedynczego filara
        elif len(self.culvert_top) <= 2 and len(self.culvert_special) == 0:
            if len(self.culvert_common) <= 2:
                self.culvertXS = self.culvert_top+list(reversed(self.culver_bottom[:]))

            elif len(self.culvert_common) > 2:
                flag = 0
                print(len(self.culvert_top))
                while len(self.culvert_common) > 0 and len(self.culvert_top) > 0:
                    if flag == 0:
                        self.geom.append(self.culvert_common[0])
                        #self.geom.append(self.culvert_top[0])
                        flag = 1
                        continue
                    if flag == 1:
                        pkt_first = self.culvert_top[0]
                        print(pkt_first)
                        index = self.culvert_common.index(min(self.culvert_common, key=lambda x: abs(x[0] - pkt_first[0])))
                        print(str(self.culvert_common[index])+"---lower---")
                        pkt_dol_first = self.culvert_common[index]
                        try:
                            if self.geom[-1] != pkt_first:
                                self.geom.append(self.culvert_top.pop(0))
                        except:
                            self.geom.append(self.culvert_top.pop(0))
                        print('---')
                        print(abs(pkt_dol_first[0] - pkt_first[0]))
                        if abs(pkt_dol_first[0] - pkt_first[0]) < 0.5:
                            self.geom.append(pkt_dol_first)
                            print(self.culvert_common.pop(index))
                        flag = 2
                        continue
                    if flag == 2:
                        pkt_first = self.culvert_top.pop(0)
                        index = self.culvert_common.index(min(self.culvert_common, key=lambda x: abs(x[0] - pkt_first[0])))
                        pkt_dol_first = self.culvert_common[index]
                        if abs(pkt_dol_first[0] - pkt_first[0]) < 0.5:
                            self.geom.append(pkt_dol_first)
                            print(self.culvert_common.pop(index))
                        self.geom.append(pkt_first)
                        flag = 3
                        continue
                    if flag == 3:
                        pkt_first = self.culvert_top[0]
                        self.geom.append(pkt_first)
                        flag = 1
                self.culvertXS = list(self.geom) + list(reversed(self.culver_bottom[1:-1]))

        elif len(self.culvert_top) == 0:
            self.culvertXS = self.culvert_common

        ### dla wiekszej liczby filarow
        elif len(self.culvert_top) > 2:
            flag = 0
            print(len(self.culvert_top))
            while len(self.culvert_common) > 0 and len(self.culvert_top) > 0:
                if flag == 0:
                    pkt1 = self.culvert_common[0]
                    pkt2 = self.culvert_top[0]
                    if abs(pkt1[0] - pkt2[0]) < 1.5:
                        self.geom.append(self.culvert_common.pop(0))
                        self.geom.append(self.culvert_top.pop(0))
                    else:
                        self.geom.append(self.culvert_top.pop(0))

                    flag = 1
                    continue
                if flag == 1:
                    pkt_first = self.culvert_top.pop(0)
                    index = self.culvert_common.index(min(self.culvert_common, key=lambda x: abs(x[0]-pkt_first[0])))
                    pkt_dol_first = self.culvert_common[index]
                    if self.geom[-1] != pkt_first:
                        self.geom.append(pkt_first)
                    print('---')
                    print(abs(pkt_dol_first[0]-pkt_first[0]))
                    if abs(pkt_dol_first[0]-pkt_first[0]) < 0.5:
                        self.geom.append(pkt_dol_first)
                        print(self.culvert_common.pop(index))
                    flag = 2
                    continue
                if flag == 2:
                    pkt_first = self.culvert_top.pop(0)
                    index = self.culvert_common.index(min(self.culvert_common, key=lambda x: abs(x[0]-pkt_first[0])))
                    pkt_dol_first = self.culvert_common[index]
                    if abs(pkt_dol_first[0]-pkt_first[0]) < 0.5:
                        self.geom.append(pkt_dol_first)
                        print(self.culvert_common.pop(index))
                    self.geom.append(pkt_first)
                    flag = 3
                    continue
                if flag == 3:
                    pkt_first = self.culvert_top[0]
                    self.geom.append(pkt_first)
                    flag = 1
            self.culvertXS = list(self.geom) + list(reversed(self.culver_bottom[1:-1]))
            #self.culvertXS = reversed(self.culvertXS)
        #if self.culvertXS[0] != self.culvertXS[-1]:
            #self.culvertXS.append(self.culvertXS[0])

        if len(self.deck) == 0:
            lista = self.culvert_common+self.culvert_top+self.culver_bottom
            self.deck.append(max(lista, key = lambda x: x[1]))

    def get_km_bridge(self,nwk):
        """znajduje km mostu z punktow nwk """
        self.topoID = 0
        zww = []
        if len(self.zwwDoKM) >= 2:
            zww = [[point.x, point.y] for point in self.zwwDoKM]
            print(zww)

        kilometry = []
        old_x, old_y, old_km = None, None, None


        if len(self.zwwDoKM) < 2:
            zww.append([self.point_data[0].x, self.point_data[0].y])
            zww.append([self.point_data[-2].x, self.point_data[-2].y])
        else:
            pass
        # tu oblicza przeciecie z zww
        for pkt in nwk.pointList:
            xB, yB, kmB = pkt.y, pkt.x, pkt.val2
            if old_x != None:
                x,y,b,c = line_intersection(zww[0][0], zww[0][1], zww[-1][0], zww[-1][1], old_x, old_y, xB, yB)
                if b == True and c == True:
                    odl1 = distance(x, xB, y, yB)
                    if kmB < old_km:
                        kilometr = kmB + odl1
                    else:
                        kilometr = kmB - odl1
                    kilometry.append([kilometr, odl1])

                    for branch in nwk.branchList:
                        if pkt.no in branch.pointList:
                            topoID = branch.topoID
            old_x, old_y, old_km = xB, yB, kmB
        try:
            self.km = min(kilometry, key=lambda x: x[1])[0]
            self.topoID = topoID
            # jak nic nie wyliczy z zww to probuje z granicznych
        except:
            zww = self.point_data
            zww = list(filter(lambda x: x.odlRed != 'None', zww))
            print(zww)
            zww.sort(key = lambda x: float(x.odlRed))
            kilometry = []
            old_x, old_y, old_km = None, None, None
            for pkt in nwk.pointList:
                xB, yB, kmB = pkt.y, pkt.x, pkt.val2
                if old_x != None:
                    x, y, b, c = line_intersection(zww[0].x, zww[0].y, zww[-1].x, zww[-1].y, old_x, old_y, xB, yB)
                    #if b == True or c == True: print(x,y,b,c)
                    if b == True and c == True:
                        odl1 = distance(x, xB, y, yB)
                        if kmB < old_km:
                            kilometr = kmB + odl1
                        else:
                            kilometr = kmB - odl1
                        kilometry.append([kilometr, odl1])
                        for branch in nwk.branchList:
                            if pkt.no in branch.pointList:
                                topoID = branch.topoID

                old_x, old_y, old_km = xB, yB, kmB
            try:
                self.km = min(kilometry, key=lambda x: x[1])[0]
                self.topoID = topoID
            except:
                self.km = 0
                self.topoID = 0

            print("km v2: " + str(kilometry))
        replacements1 = {
            "K01": 0.035,
            "K02": 0.032,
            "K03": 0.035,
            "K04": 0.038,
            "K05": 0.04,
            "K06": 0.02,
            "K07": 0.05,
            "K09": 0.07,
            "K10": 0.1,
            "T01": 0.025,
            "T03": 0.12,
            "T04": 0.08,
            "T06": 0.12,
            "T07": 0.045,
            "T08": 0.09,
            "T09": 0.2,
            "T10": 0.035,
            "T11": 0.2,
            "T12": 0.05,
            "T14": 0.02,
            "T15": 0.09,
            "T16": 0.1,
            "T17": 0.3
        }
        manningVal = []
        for element in self.manning:
            manningVal.append(replacements1[element])
        try:
            self.manning = sum(manningVal)/len(manningVal)
        except:
            self.manning = 0.035

    def get_weir(self):
        print(self.lp)
        self.manning = []
        self.geom = []
        self.deck = []
        self.kor = []
        self.culver_bottom = []
        self.culvert_top = []
        self.culvert_common = []
        self.culvert_special = []
        self.culvertXS = []
        self.zww = []
        self.zwwDoKM = []
        '''podzial na pkt koryta i obiektu, pobranie najnizszego punktu z koryta'''
        self.culvert_upS = 1000
        # pobranie koryta w zakresie budowli
        flag = 0
        laczenie = []
        for pkt in self.point_data:
            print(pkt.kod, pkt.znacznik)
            if "t" in str(pkt.cos).lower() or "k" in str(pkt.cos).lower():
                self.kor.append([float(pkt.dist), float(pkt.z)])
                if "K" in pkt.cos:
                    self.manning.append(pkt.cos)
            if 2 == int(float(pkt.znacznik)):
                self.deck.append([float(pkt.dist), float(pkt.z)])
            if 20 == int(float(pkt.znacznik)):
                laczenie.append([float(pkt.dist), float(pkt.z)])
            if "zww" in str(pkt.kod).lower():
                self.zww.append([float(pkt.dist), float(pkt.z)])
                self.zwwDoKM.append(pkt)
            if pkt.kod != 'None' and str(pkt.kod).lower() != 'zww' and 7.0 == float(pkt.kod):
                self.culvert_upS = float(pkt.z)
            if 9.0 == float(pkt.znacznik):
                self.culvert_downS = float(pkt.z)
        #self.culvertXS = self.kor
        self.deck = self.deck[:-1]
        if laczenie:
            self.deck.insert(0, laczenie[0])
            self.deck.append(laczenie[-1])

    def excel_print(self, workbook, path='C:\\'):
        worksheet = workbook.add_worksheet(str(self.lp))
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

        worksheet.write(7, 0, 'Topo ID:')
        worksheet.write(8, 0, 'km:')
        worksheet.write(8, 2, 'Manning:')
        try:
            worksheet.write(7, 1, str(self.topoID))
            worksheet.write(8, 1, str(round(self.km,0)))
            worksheet.write(8, 3, str(round(self.manning, 2)))
        except:
            worksheet.write(7, 1, "None")
            worksheet.write(8, 1, "None")
            worksheet.write(8, 3, "None")
        try:
            worksheet.write(4, 0, 'Odl. pikiety 7 od linii zww:')
            worksheet.write(4, 1, str(round(self.culvert_len, 2)))
        except:
            pass
        try:
            szer = float(max(self.culvertXS, key=lambda x: float(x[0]))[0]) - float(min(self.culvertXS, key=lambda x: float(x[0]))[0])
            worksheet.write(5, 3, 'Max_światło:')
            worksheet.write(5, 4, str(round(szer,2)))

        except:
            pass
        try:
            worksheet.write(5, 0, 'Upst.(faktyczny, do mike samo się zamieni):')
            worksheet.write(5, 1, str(self.culvert_upS))
            worksheet.write(6, 0, 'Downst.(faktyczny, do mike samo się zamieni):')
            worksheet.write(6, 1, str(self.culvert_downS))
            worksheet.write(5, 2, 'Delta_h:')
            worksheet.write(6, 2, str("=B6-B7"))
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
            worksheet.write(3, 3, 'Szer jezdni pom geod. (nasza długość):')
            worksheet.write(3, 4, str(self.szer))
        except:
            pass
        worksheet.write(4, 3, 'Wprowadzić:')
        worksheet.write(4, 4, 'tak')
        chart1 = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
        for row, line in enumerate(self.kor):
            for col, cell in enumerate(line):
                worksheet.write(row+10, col, cell)

        chart1.add_series({
            'name': 'Koryto',
            'categories': [str(self.lp), 10, 0, row+10, 0],
            'values': [str(self.lp), 10, 1, row+10, 1],
        })

        for row, line in enumerate(self.culvertXS):
            for col, cell in enumerate(line):
                worksheet.write(row+10, col+2, cell)

        chart1.add_series({
            'name': 'Przepust',
            'categories': [str(self.lp), 10, 2, row + 10, 2],
            'values': [str(self.lp), 10, 3, row + 10, 3],
        })
        if len(self.deck) == 2:
            point = [(self.deck[0][0]+self.deck[-1][0])/2, (self.deck[0][1]+self.deck[-1][1])/2]
            self.deck.insert(1, point)

        for row, line in enumerate(self.deck):
            for col, cell in enumerate(line):
                worksheet.write(row+10, col+4, cell)
        chart1.add_series({
            'name': 'Przelew',
            'categories': [str(self.lp), 10, 4, row + 10, 4],
            'values': [str(self.lp), 10, 5, row + 10, 5],
        })
        chart1.set_style(10)
        chart1.set_size({'width': 720, 'height': 576})
        worksheet.insert_chart('G1', chart1, {'x_offset': 25, 'y_offset': 15})
        # skalowanie
        from PIL import Image
        def calculate_scale(file_path, bound_size):
            # check the image size without loading it into memory
            im = Image.open(file_path)
            original_width, original_height = im.size

            # calculate the resize factor, keeping original aspect and staying within boundary
            bound_width, bound_height = bound_size
            ratios = (float(bound_width) / original_width, float(bound_height) / original_height)
            return min(ratios)


        #worksheet.write('A12', 'Insert an image with an offset:')
        import os
        n = 1
        for foto in self.foto.replace(' ', '').split(','):
            for root, dirs, files in os.walk(path):
                for name in files:
                    if name.replace(' ', '') == foto:
                        image_path = os.path.abspath(os.path.join(root, name))
                        bound_width_height = (900, 400)
                        resize_scale = calculate_scale(image_path, bound_width_height)
                        #print(os.path.abspath(os.path.join(root, name)))
                        worksheet.insert_image('S'+ str(n), os.path.abspath(os.path.join(root, name)), {'x_scale': resize_scale, 'y_scale': resize_scale})
                        n += 25
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

