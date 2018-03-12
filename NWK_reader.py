# -*- coding: utf-8 -*-

from NWK_reader_classes import *


def line_to_list(line):
    name = line.split()[0]
    line2 = line.replace(" =", ",")
    line2 = line2.replace("'", "")
    line2 = line2.replace("\n", "")
    string_list = line2.split(", ")
    return string_list, name


file = open("przykladowy_NWK", 'r')
readline = file.readlines()

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
while i < len(readline):
    line = readline[i]

    if not line.split():
        i += 1
        continue

    stringList, name = line_to_list(line)

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
        cl.add_paramaters(stringList, name, line)
    i += 1


print("zaczytano dane")

# Przetwarzanie typow danych
change_type(nwk)

print("All done")
print(nwk.branchList[8].linkChannel.crossSection.data)

print("All done")