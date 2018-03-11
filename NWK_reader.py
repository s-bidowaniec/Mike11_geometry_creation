# -*- coding: utf-8 -*-

from NWK_reader_classes import *

def lineToList(line):
    name = line.split()[0]
    line2 = line.replace(" =", ",")
    line2 = line2.replace("'", "")
    line2 = line2.replace("\n", "")
    stringList = line2.split(", ")
    return stringList, name

file = open("przykladowy_NWK", 'r')
readline = file.readlines()

nwk = nwkFile()
i = 0

### zaczytywanie początku pliku
while i < len(readline) and "POINTS" not in readline[i]:
    nwk.addStart(readline[i])
    i += 1
i += 1

### zaczytywanie punktów do klasy nwkFile
while i < len(readline) and "EndSect  // POINTS" not in readline[i]:
    line = readline[i]
    stringList, name = lineToList(line)
    nwk.addPoint(stringList, name)
    i += 1
    
### przejście do pierwszego "brancha"
while "[branch]" not in readline[i]:
    i += 1

### zaczytywanie poszczególnych klas
while i < len(readline):
    line = readline[i]
    
    if line.split() == []:
        i += 1
        continue

    stringList, name = lineToList(line)

    
    if "[branch]" in line:
        nwk.branchList.append(branch())
        cl = nwk.branchList[-1]

    
    elif "[linkchannel]" in line:
        cl.linkChannel = linkChannel(cl)
        cl = cl.linkChannel
    
    elif "[Cross_Section]" in line:
        cl.crossSection = CrossSection(cl)
        cl = cl.crossSection

    elif "[weir_data]" in line:
        nwk.weirList.append(weir())
        cl = nwk.weirList[-1]
        wr = True

    elif "[ReservoirData]" in line:
        cl.reservoir = reservoirData(cl)
        cl = cl.reservoir

    elif "[Elevation]" in line:
        cl.elevation = elevation(cl)
        cl = cl.elevation

    elif "[Geometry]" in line:
        cl.geometry = geometry(cl)
        cl = cl.geometry

    elif "[Level_Width]" in line:
        cl.levelWidth = levelWidth(cl)
        cl = cl.levelWidth

    elif "[culvert_data]" in line:
        nwk.culvertList.append(culvert())
        cl = nwk.culvertList[-1]
        cr = True

    elif "[Irregular]" in line:
        cl.irregular = irregular(cl)
        cl = cl.irregular
    
    elif cl.end in line and cl.parent == None:
        i += 1
        continue

    elif cl.end in line:
        cl = cl.parent

    else:
        cl.addParameters(stringList, name, line)
    i += 1

print("zaczytano dane")

### Przetwarzanie typow danych
changeType(nwk)

print("All done")
print(nwk.branchList[8].linkChannel.crossSection.data)


        
        
        

