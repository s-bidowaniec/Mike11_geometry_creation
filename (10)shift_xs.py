import openpyxl, time
import dbm
import pickle
import copy
from classes import Bridge
from functions import *
# -------------------------------- PARAMETRY --------------------------------------------
river = 'BUDKOWICZANKA'
# -------------------------------- PLIKI WSADOWE --------------------------------------------------------------
"""plik wsadowy rawdata"""
xsInputDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v3.01_13.12\testy\rawdata_marker.txt"
fileWejscieXS = open(xsInputDir,'r')
bazaXsRawData, XsOrder = read_XSraw(fileWejscieXS)

# --------------------------------- PLIKI WYNIKOWE -----------------------------------------------------------
# nowy plik XSrawData
xsOutputDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v3.01_13.12\testy\rawdata_marker_shift.txt"
if xsInputDir == xsOutputDir:
    raise ValueError('XS input file equals XS output file', 'foo', 'bar', 'baz')
fileWynikXS = open(xsOutputDir,'w')

"""skrypt zmienia polozenie "station" punktow, tak zeby wyswietlajac przekroje polaczone link channelem,
    punktem styku byly ich markery 1 i 3"""
ustawione = {}
doUstawienia = []
xsDict = {}
nodes = []
LtoR = {}
RtoL = {}

for element in bazaXsRawData:

    LtoR[str(element.cords.split()[1:3])] = element.cords.split()[3:]
    RtoL[str(element.cords.split()[3:])] = element.cords.split()[1:3]
    if river in element.riverCode and 'S01' in element.reachCode:
        element.status = 1

        nodes.append([element.cords.split()[1:3], element.points[0].station, 'L'])
        nodes.append([element.cords.split()[3:], element.points[-1].station, 'R'])
    else:
        element.status = 0
        xsDict[str(element.cords.split()[1:])] = element
while len(nodes)>0:
    newnodes=[]
    for node in nodes:
        if node[-1] == 'L':
            try:
                xyL = RtoL[str(node[0])]
                xyR = node[0]
            except: continue
        else:
            try:
                xyR = LtoR[str(node[0])]
                xyL = node[0]
            except: continue
        try:

            xs = xsDict[str(xyL+xyR)]

            if 'L' in node[-1]:
                zero = xs.points[-1].station
                newnodes.append(xyL+[zero])
            else:
                zero = xs.points[0].station
                newnodes.append(xyL + [zero])
            for pkt in xs.points:
                pkt.station += node[1]-zero
        except:
            print(str(xyL+xyR))
    nodes=copy.deepcopy(newnodes)

for element in bazaXsRawData:
    element.print_txt(fileWynikXS, None, 1)