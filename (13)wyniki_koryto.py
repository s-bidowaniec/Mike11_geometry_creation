import openpyxl, time
import dbm
import pickle
import copy
from classes import Bridge
import pandas as pd
from functions import *
from datetime import datetime
from func_convert_sim11 import convert_res11
# -------------------------------- PARAMETRY --------------------------------------------
RIVER = 'CZARNY_POTOK'
# -------------------------------- PLIKI WSADOWE --------------------------------------------------------------


inputNwkDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v3.01_13.12\01_MIKE11\02_S01_Czarny_Potok_NWK\S01_Czarny_Potok.nwk11"
fileWejscieNWK = open(inputNwkDir, 'r')

res11_lok = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v3.01_13.12\01_MIKE11\07_S01_Czarny_Potok_WYNIKI\S01_Czarny_Potok_kalibracja.res11"
dane = convert_res11(res11_lok)

"""skrypt interpoluje wartości Q na punktach H, następnie sumuje przepływ z przekroi spiętych linkami"""
ustawione = {}
doUstawienia = []
xsDict = {}
nodes = []
LtoR = {}
RtoL = {}
qPoints = []
hPoints = []
nwk = read_NWK(fileWejscieNWK)

class qPoint:
    def __init__(self, river, km, q):
        self.river = river
        self.km = km
        self.q = q

class hPoint:
    def __init__(self, river, km, h):
        self.river = river
        self.km = km
        self.h = h


for line in dane:
    if line[0] == 'Flood Watch':

        time = list(line[2:])

    if 'Water Level' in line[0]:
        river = line[1].split('(')[0]
        km = float(line[1].split('(')[-1].replace(')',''))
        h = line[2:]
        hPoints.append(hPoint(river, km, h))
    elif 'Discharge' in line[0]:
        river = line[1].split('(')[0]
        km = float(line[1].split('(')[-1].replace(')', ''))
        q = line[2:]
        qPoints.append(qPoint(river, km, q))
time2=[]
for date in time:
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    time2.append(date)
qDict = {}
for hPkt in hPoints:
    river = hPkt.river
    km = hPkt.km

    q1 = max([x if x.river == river and x.km < km else qPoint(0,0,0) for x in qPoints], key=lambda x: x.km)
    q2 = min([x if x.river == river and x.km > km else qPoint(0,1000000,0) for x in qPoints], key=lambda x: x.km)
    if q1.river == 0:
        q = list(map(float, list(q2.q)))

    elif q2.river == 0:
        q = list(map(float, list(q1.q)))

    elif q1.river == river == q2.river:
        q=[]
        for index in range(len(q1.q)):
            qF = q1.q[index]
            qL = q2.q[index]

            deltaL = q2.km - q1.km
            deltaQ = float(qL) - float(qF)
            deltaLPrz = q2.km - km
            q.append(deltaLPrz*deltaQ/deltaL)

    else:
        import pdb
        pdb.set_trace()
    hPkt.q = q
    qDict[hPkt.river+str(hPkt.km)] = q

listaKP = []
for branch in nwk.branchList:
    if 'KP' in branch.riverName:
        listaKP.append(branch)
        if branch.riverName[-1] == 'P':
            LtoR[branch.connectTopoID + str(branch.point2)] = branch.connectRiver + str(branch.point)
        elif branch.riverName[-1] == 'L':
            RtoL[branch.connectTopoID + str(branch.point2)] = branch.connectRiver + str(branch.point)

mainRiverPkt = []
for pkt in hPoints:
    if RIVER in pkt.river:
        if pkt.km not in [km.km for km in mainRiverPkt]:
            mainRiverPkt.append(pkt)
dataframe = {}
dataframe['time'] = time
sumaQ = []
for pkt in mainRiverPkt:
    sumaQ.append(pkt.q)
    key = pkt.river+str(pkt.km)
    while True:
        try:
            print(LtoR[key])
            sumaQ.append(qDict[LtoR[key]])
            key = LtoR[key]
        except:
            break
    key = pkt.river + str(pkt.km)
    while True:
        try:
            print(RtoL[key])
            sumaQ.append(qDict[RtoL[key]])
            key = RtoL[key]
        except:
            break
    if len(sumaQ)>1:
        pkt.Q = list(map(sum, list(zip(*sumaQ))))
    else:
        pkt.Q = sumaQ[0]


    dataframe[pkt.river+' '+str(pkt.km)] = pkt.Q


df = pd.DataFrame(data=dataframe)
writer = pd.ExcelWriter(res11_lok.replace('.res11', '.xlsx'))
df.to_excel(writer, 'Sheet1')
writer.save()
writer.close()