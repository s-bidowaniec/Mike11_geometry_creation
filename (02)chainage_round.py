# -*- coding: utf-8 -*-

from functions import *
from classes import *

# plik wsadowy nwk, pobierana jest lista punktow oraz branchy do ktorych dopisywane sa dane z nowych linkow
inputNwkDir = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\BUDKOWICZANKA_S01_Qn.nwk11"

# nowy plik NWK z naniesionymi linkami
outputNwkDir = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\BUDKOWICZANKA_S01_Qn5.nwk11"
if inputNwkDir != outputNwkDir:
    fileWejscieNWK = open(inputNwkDir, 'r')
    fileWynik = open(outputNwkDir, "w")
else:
    raise 'Error: input == output'

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



readline = fileWejscieNWK.readlines()

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

listaPunktowDoZmiany = []

for i in nwk.branchList:
    listaPunktowDoZmiany.extend([i.pointList[0], i.pointList[-1]])
    if "'" in i.connectRiver:
        i.connectRiver = ''

    if "'" in i.connectTopoID:
        i.connectTopoID = ''
    
for i in nwk.pointList:
    if i.no in listaPunktowDoZmiany:
        i.val1 = 1
        i.val2 = int(round(i.val2,0))


nwk.print_to_nwk(fileWynik)
fileWynik.close()

print("done")
