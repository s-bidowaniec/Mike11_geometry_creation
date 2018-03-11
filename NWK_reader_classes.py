# -*- coding: utf-8 -*-

import time
class nwkPoint(object):
    def __init__(self, no, x, y, val1, val2, val3, z = None):
        self.no = no
        self.x = x
        self.y = y
        self.val1 = val1
        self.val2 = val2
        self.val3 = val3
        self.z = z
        self.end = None


######################
class elevation(object):
    def __init__(self, parent = None):
        self.data = []
        self.end = "EndSect  // Elevation"
        self.parent = parent

    def addParameters(self, stringList, name, line):
        self.data.append(stringList[1:])


######################
class reservoirData(object):
    def __init__(self, parent = None):
        self.data = {}
        self.elevation = None
        self.end = "EndSect  // ReservoirData"
        self.parent = parent

    def addParameters(self, stringList, name, line):
        self.data[name] = stringList[1:]


######################
class levelWidth(object):
    def __init__(self, parent = None):
        self.data = []
        self.end = "EndSect  // Level_Width"
        self.parent = parent

    def addParameters(self, stringList, name, line):
        self.data.append(stringList[1:])


######################
class irregular(object):
    def __init__(self, parent = None):
        self.data = []
        self.end = "EndSect  // Irregular"
        self.parent = parent

    def addParameters(self, stringList, name, line):
        self.data.append(stringList[1:])


######################
class geometry(object):
    def __init__(self, parent = None):
        self.irregular = None
        self.levelWidth = None
        self.data = {}
        self.end = "EndSect  // Geometry"
        self.parent = parent

    def addParameters(self, stringList, name, line):
        self.data[name] = stringList[1:]


######################
class weir(object):
    def __init__(self, parent = None):
        self.reservoir = None
        self.geometry = None
        self.weirParams = {}
        self.end = "EndSect  // weir_data"
        self.parent = parent

    def addParameters(self, stringList, name, line):
        
        if "Location" in line:
            self.riverName = stringList[1]
            self.km = float(stringList[2])
            self.topoID = stringList[3]
            self.ID = stringList[4]             # sprawdzic wartosci

        elif name in ["HorizOffset", "Attributes", "HeadLossFactors",
                      "WeirFormulaParam", "WeirFormula2Param", "WeirFormula3Param"]:
            self.weirParams[name] = stringList[1:]
            
        #else:
            #print(u"Blad funkcji addParameters klasy weir:")
            #print(line)

    
######################
class culvert(object):
    def __init__(self, parent = None):
        self.reservoir = None
        self.geometry = None
        self.culvertParams = {}
        self.end = "EndSect  // culvert_data"
        self.parent = parent

    def addParameters(self, stringList, name, line):

        if "Location" in line:
            self.riverName = stringList[1]
            self.km = float(stringList[2])
            self.ID = stringList[3]
            self.topoID = stringList[4]

        elif name in ["HorizOffset", "Attributes", "HeadLossFactors"]:
            self.culvertParams[name] = line[1:]
            
        #else:
            #print(u"Blad funkcji addParameters klasy weir:")
            #print(line)


######################
class CrossSection(object):
    def __init__(self, parent = None):
        self.data = []
        self.end = "EndSect  // Cross_Section"
        self.parent = parent

    def addParameters(self, stringList, name, line):
        self.data.append(str(stringList[1]))
        self.data.append(str(stringList[2]))


######################
class linkChannel(object):
    def __init__(self, parent = None):
        self.crossSection = None
        self.end = "EndSect  // linkchannel"
        self.parent = parent

    def addParameters(self, stringList, name, line):

        if "Geometry" in line:
            self.geometry = stringList[1:]

        elif "HeadLossFactors" in line:
            self.HeadLossFactors = stringList[1:]

        elif "Bed_Resistance" in line:
            self.BedResistance = stringList[1:]
            
        #else:
            #print(u"Blad funkcji addParameters klasy linkChannel:")
            #print(line)


######################
class branch(object):
    def __init__(self, parent = None):
        self.pointsNumbersList = []
        self.linkChannel = None
        self.end = "EndSect  // branch"
        self.parent = parent

    def addParameters(self, stringList, name, line):
      
        if "definitions" in line:
            self.riverName =  stringList[1]
            self.topoID = stringList[2]
            self.val1 = int(stringList[3])
            self.val2 = float(stringList[4])
            self.val3 = int(stringList[5])
            self.val4 = int(stringList[6])
            self.val5 = int(stringList[7])
            
        elif "connections" in line:
            if stringList[1] == '':
                self.connectRiver = None
                self.point = None
                self.connectTopoID = None
                self.point2 = None
            else:
                self.connectRiver = stringList[1]
                self.point = float(stringList[2])       # sprawdzić czy float czy int
                self.connectTopoID = stringList[3]
                self.point2 = float(stringList[4])      # sprawdzić czy float czy int

        elif "points" in line:
            self.pointsNumbersList.extend(stringList[1:])
        #else:
            #print(u"Blad funkcji addParameters klasy branch:")
            #print(line)


######################
class nwkFile(object):
    def __init__(self):
        self.pointList = []
        self.branchList = []
        self.weirList = []
        self.culvertList = []
        self.start = ''
        self.end = None
        

    def addStart(self, value):
        self.start = self.start + value

    def addPoint(self, stringList, name):    
        no = int(stringList[1])
        x = float(stringList[2])
        y = float(stringList[3])
        val1 = int(stringList[4])
        val2 = float(stringList[5])
        val3 = int(stringList[6])
        
        self.pointList.append(nwkPoint(no, x, y, val1, val2, val3))


def changeType(ob):
    attrDict = ob.__dict__

    for i in attrDict:
        try:
            print(attrDict[i].data)
        except:
            print(i)
        if type(attrDict[i]) == list:
            print("a")
            for j in range(len(attrDict[i])):
                if '__dict__' in dir(attrDict[i][j]):
                    changeType(attrDict[i][j])   
                        
                try:
                    if "." in attrDict[i][j]:
                        attrDict[i][j] = float(attrDict[i][j])
                    else:
                        attrDict[i][j] = int(attrDict[i][j])
                except:
                    pass
              
        elif type(attrDict[i]) == dict:
            print("b")
            for j in attrDict[i]:
                try:
                    if "." in attrDict[i][j]:
                        attrDict[i][j] = float(attrDict[i][j])
                    else:
                        attrDict[i][j] = int(attrDict[i][j])
                except:
                    pass
                   
        try:
            if "." in attrDict[i]:
                print("c")
                attrDict[i] = float(attrDict[i])
            else:
                attrDict[i] = int(attrDict[i])
        except:
            pass
        
        try:
            print("d")
            if '__dict__' in dir(attrDict[i]):
                print(attrDict[i].data)
                changeType(attrDict[i])
            else:
                pass
        except:
            pass

    return (True)