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

    def values_2_string(self):
        dataDict = self.__dict__
        for i in dataDict:
            if type(dataDict[i]) == int or type(dataDict[i]) == float:
                dataDict[i] = str(dataDict[i])



######################
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


######################
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



######################
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


######################
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


######################
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


######################
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
                self.connectRiver = "''"
                self.point = "-1e-155"
                self.connectTopoID = "''"
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


######################
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

        file.write("""   EndSect  // BRANCHES\n\n   [STRUCTURE_MODULE]\n      \
        Structure_Version = 1, 1\n\n\n      [WEIR]\n""")

        for i in self.weirList:
            i.print_to_nwk(file)

        file.write("""      EndSect  // WEIR\n\n      [CULVERTS]\n""")

        for i in self.culvertList:
            i.print_to_nwk(file)

        file.write(self.finish)

    def nwk_rdp(self):
        self.pointsToRdp = []
        for i in self.pointList:
            self.pointsToRdp.extend([i.x, i.y])

        try:
            from rdp import rdp
        except:
            print u"nie można zaimportować modułu do RDP"
            pass

        self.rdpOutList = rdp(self.pointsToRdp, epsilon = 0.08)
        self.pointsToRemove = []
        i = 0

        while i < len(self.pointList):
            usunac = True
            for j in self.rdpOutList:
                if i.x == j[0] and i.y == j[1]:
                    usunac = False

            if usunac:
                self.pointsToRemove.append(i.no)
                del self.pointList[i]
                usunac = False
            else:
                i += 1

        for i in self.branchList:
            while j < range(len(i.pointList)):
                if i.pointList[j] in self.pointsToRemove:
                    del i.pointList[j]
                else:
                    i += 1










