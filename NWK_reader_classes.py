# -*- coding: utf-8 -*-


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


######################
class Elevation(object):
    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Elevation"
        self.parent = parent

    def add_paramaters(self, string_list, name, line):
        self.data.append(string_list[1:])


######################
class ReservoirData(object):
    def __init__(self, parent=None):
        self.data = {}
        self.elevation = None
        self.end = "EndSect  // ReservoirData"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data[name] = string_list[1:]


######################
class LevelWidth(object):
    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Level_Width"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data.append(string_list[1:])


######################
class Irregular(object):
    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Irregular"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data.append(string_list[1:])


######################
class Geometry(object):
    def __init__(self, parent=None):
        self.irregular = None
        self.levelWidth = None
        self.data = {}
        self.end = "EndSect  // Geometry"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data[name] = string_list[1:]


######################
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


######################
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
            self.culvertParams[name] = line[1:]

        # else:
        # print(u"Blad funkcji addParameters klasy weir:")
        # print(line)

######################
class CrossSection(object):
    def __init__(self, parent=None):
        self.data = []
        self.end = "EndSect  // Cross_Section"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        self.data.append(str(string_list[1]))
        self.data.append(str(string_list[2]))


######################
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


######################
class Branch(object):
    def __init__(self, parent=None):
        self.pointsNumbersList = []
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
                self.connectRiver = None
                self.point = None
                self.connectTopoID = None
                self.point2 = None
            else:
                self.connectRiver = string_list[1]
                self.point = float(string_list[2])  # sprawdzić czy float czy int
                self.connectTopoID = string_list[3]
                self.point2 = float(string_list[4])  # sprawdzić czy float czy int

        elif "points" in line:
            self.pointsNumbersList.extend(string_list[1:])
        # else:
        # print(u"Blad funkcji addParameters klasy branch:")
        # print(line)


######################
class NwkFile(object):
    def __init__(self):
        self.pointList = []
        self.branchList = []
        self.weirList = []
        self.culvertList = []
        self.start = ''
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

        self.pointList.append(NwkPoint(no, x, y, val1, val2, val3))


def change_type(ob):
    attr_dict = ob.__dict__

    for i in attr_dict:
        if type(attr_dict[i]) == list:
            for j in range(len(attr_dict[i])):
                if '__dict__' in dir(attr_dict[i][j]):
                    change_type(attr_dict[i][j])

                try:
                    if "." in attr_dict[i][j]:
                        attr_dict[i][j] = float(attr_dict[i][j])
                    else:
                        attr_dict[i][j] = int(attr_dict[i][j])
                except:
                    pass

        elif type(attr_dict[i]) == dict:
            for j in attr_dict[i]:
                try:
                    if "." in attr_dict[i][j]:
                        attr_dict[i][j] = float(attr_dict[i][j])
                    else:
                        attr_dict[i][j] = int(attr_dict[i][j])
                except:
                    pass

        try:
            if "." in attr_dict[i]:
                attr_dict[i] = float(attr_dict[i])
            else:
                attr_dict[i] = int(attr_dict[i])
        except:
            pass

        try:
            if '__dict__' in dir(attr_dict[i]):
                print(attr_dict[i].par)
                change_type(attr_dict[i])
            else:
                pass
        except:
            pass

    return True
