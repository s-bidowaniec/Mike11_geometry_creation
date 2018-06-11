# -*- coding: utf-8 -*-

############################################## SB ##########################################################
from functions import read_XSraw, printowanie
from classes import *
import time

# plik wsadowy rawdata,
inputXS = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\Budkowiczanka_Qn.txt"
# plik wsadowy nwk, pobierane sa poloaczenia link do generacji nazw dla branch
inputNWK = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\BUDKOWICZANKA_S01_Qn.nwk11"

# -----------------------------------------------------------------------------------------------------------

# plik wynikowy przekroje z nazwami
outputXS = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\Budkowiczanka_Qn3.txt"
# plik wynikowy NWK z nazwami
outputNWK = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\BUDKOWICZANKA_S01_Qn3.nwk11"

if outputXS == inputXS or outputNWK == inputNWK or inputNWK == outputXS or inputXS == outputNWK:
    raise 'Error: ten sam plik na wejsciu i wyjsciu'
else:
    f = open(outputXS, 'w')
    fileWynik = open(outputNWK, "w")
    fileWejscieXS = open(inputXS, 'r')
    fileWejscieNWK = open(inputNWK, 'r')
XS_dat, XS_order = read_XSraw(fileWejscieXS)

# ------------------------------------------------------------------------------------------------------------------- #

#print(printowanie(linki, 14923))

print("Raw data zaczytane")


############################################## KP ##########################################################

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

branchDictNames = {}
### iterowanie po branchach
linklist = []
riverNamesDrop = []
nazwaOld = '-'
for branch in nwk.branchList:
    if "PTZ_" in branch.riverName or "LTZ_" in branch.riverName:
        for linkB in nwk.branchList:
            #print(linkB.riverName, linkB.connectRiver, branch.riverName, linkB.connectTopoID)

            if "kp_" in str(linkB.riverName).lower() and str(branch.riverName).lower() == str(linkB.connectTopoID).lower():
                linklist.append(linkB)
                print(linkB.riverName, linkB.connectRiver, branch.riverName, linkB.connectTopoID)

        riverNames1 = [[i.connectRiver, i.point, i.point2, 1, str(i.riverName).split("_")[1:4]] for i in linklist if str(i.connectRiver).lower() != str(branch.riverName).lower()]
        linklist = []
        #riverNames2 = [[i.connectTopoID, i.point2, i.point, 2, str(i.riverName).split("_")[1:4]] for i in linklist if str(i.connectTopoID).lower() != str(branch.riverName).lower()]
        riverNames = riverNames1 #+ riverNames2
        riverNames1 = []
        print(branch.riverName)
        print(riverNames)

        minimalKm = min([float(i[2]) for i in riverNames])
        maximalKm = max([float(i[2]) for i in riverNames])
        for element in riverNames:
            if element[2] == minimalKm or element[2] == maximalKm:
                riverNamesDrop.append(element)

        for element in riverNamesDrop:
            wyrazy = str(element[-1][1]).split()
            if len(wyrazy)==1:
                nazwaIn=str(wyrazy[0][0:4]).upper()
            elif len(wyrazy)>1:
                nazwaIn = [str(i[0]).upper() for i in wyrazy]
                nazwaIn = ''.join(nazwaIn)
            element[-1][1] = nazwaIn
        connectedBranchNamesKm = [str(i[-1][1:3]) for i in riverNamesDrop]
        #countAllNamesKm = len(connectedBranchNamesKm)
        countIndividualNamesKm = len(list(set(connectedBranchNamesKm)))
        connectedBranchNames = [str(i[-1][1]) for i in riverNamesDrop]
        #countAllNames = len(connectedBranchNames)
        countIndividualNames = len(list(set(connectedBranchNames)))
        #print(countIndividualNamesKm, countIndividualNames)

        if countIndividualNamesKm == 2 and countIndividualNames == 1:
            connectedBranchName = riverNamesDrop[1][-1][1]
            for element in riverNamesDrop:
                if element[2] == minimalKm:
                    startKm = element[-1][-1]
                if element[2] == maximalKm:
                    endKm = element[-1][-1]
            nazwa = "{}_{}_{}-{}".format(branch.riverName.split("_")[0], connectedBranchName,startKm,endKm)
            #print("{}_{}_{}-{}".format(branch.riverName.split("_")[0], connectedBranchName,startKm,endKm))

        elif countIndividualNamesKm == 1 and countIndividualNames == 1:

            connectedBranchName = riverNamesDrop[0][-1][1]
            for element in riverNamesDrop:
                if element[2] == minimalKm:
                    startKm = element[-1][-1]
                if element[2] == maximalKm:
                    endKm = element[-1][-1]

            nazwa = "{}_{}_{}".format(branch.riverName.split("_")[0], connectedBranchName,startKm)
            #except:
                #nazwa = "{}_{}-{}".format(branch.riverName.split("_")[0], connectedBranchName, endKm)
            #print("{}_{}_{}-{}".format(branch.riverName.split("_")[0], connectedBranchName,startKm,endKm))


        elif countIndividualNamesKm == 2 and countIndividualNames == 2:
            #connectedBranchName = riverNamesDrop[1][-1][1]

            for element in riverNamesDrop:
                if element[2] == minimalKm:
                    startKm = element[-1][-2:]
                if element[2] == maximalKm:
                    endKm = element[-1][-2:]
            nazwa = "{}_{}_{}-{}_{}".format(branch.riverName.split("_")[0],startKm[0],startKm[1],endKm[0],endKm[1])

            #print("{}_{}_{}-{}_{}".format(branch.riverName.split("_")[0],startKm[0],startKm[1],endKm[0],endKm[1]))

        elif countIndividualNamesKm == 3 and countIndividualNames == 2:
            #connectedBranchName = riverNamesDrop[1][-1][1]
            startKm=[]
            endKm=[]
            for element in riverNamesDrop:
                if element[2] == minimalKm and element[-1][-2:] not in startKm:
                    startKm.append(element[-1][-2:])
                if element[2] == maximalKm and element[-1][-2:] not in endKm:
                    endKm.append(element[-1][-2:])
            print(startKm, endKm)
            if len(startKm) == 1 and len(endKm) == 2:
                index = 0
                for element in endKm:
                    if element[0] == startKm[0][0]:
                        endKm2 = element[1]
                        endKm.pop(index)
                    index+=1
                nazwa = "{}_{}_{}_{}-{}_{}".format(branch.riverName.split("_")[0], startKm[0][0], startKm[0][1],
                                                   endKm2[0], endKm2[1], endKm[0][1])
                #print(nazwa)

            elif len(startKm) == 2 and len(endKm) == 1:
                index = 0
                for element in startKm:
                    if element[0] == endKm[0][0]:
                        startKm2 = element
                        startKm.pop(index)
                    index+=1

                nazwa = "{}_{}_{}_{}_{}-{}".format(branch.riverName.split("_")[0], startKm[0][0], startKm[0][1], startKm2[0],startKm2[1],endKm[0][1])
                #print(nazwa)

        elif countIndividualNamesKm == 3 and countIndividualNames == 3:
            #connectedBranchName = riverNamesDrop[1][-1][1]
            startKm=[]
            endKm=[]
            for element in riverNamesDrop:
                if element[2] == minimalKm:
                    startKm.append(element[-1][-2:])
                if element[2] == maximalKm:
                    endKm.append(element[-1][-2:])
            if len(startKm) == 1 and len(endKm) == 2:
                nazwa = "{}_{}_{}-{}_{}_{}_{}".format(branch.riverName.split("_")[0], startKm[0][0], startKm[0][1],
                                                   endKm[0][0], endKm[0][1],endKm[1][0],endKm[1][1])
            elif len(startKm) == 2 and len(endKm) == 1:
                nazwa = "{}_{}_{}_{}_{}-{}_{}".format(branch.riverName.split("_")[0], startKm[0][0], startKm[0][1],
                                                      startKm[1][0], startKm[1][1],endKm[0][0],endKm[0][1])


        elif countIndividualNamesKm == 4 and countIndividualNames == 2:
            print('4 na 2')
            startKm = []
            endKm = []
            for element in riverNamesDrop:
                if element[2] == minimalKm:
                    startKm.append(element[-1][-2:])
                if element[2] == maximalKm:
                    endKm.append(element[-1][-2:])
            #print(endKm, startKm)
            #time.sleep(1)

            index = 0
            for element in endKm:
                if element[0] == startKm[0][0]:
                    endKm2 = element[1]
                    endKm.pop(index)
                    river1 = [element[0], startKm[0][1], endKm2]
                    index+=1

            index = 0
            for element in startKm:
                if len(endKm)==0:
                    endKm=[['-','-']]
                if element[0] != river1[0]:
                    startKm2 = element[1]
                    startKm.pop(index)
                    river2 = [element[0], element[1], endKm[0][1]]
                    index+=1
            nazwa = "{}_{}_{}-{}_{}_{}-{}".format(branch.riverName.split("_")[0], river1[0], river1[1],
                                                  river1[2], river2[0], river2[1], river2[2])
            print(nazwa)

        elif countIndividualNamesKm == 4 and countIndividualNames == 3:
            print('4 na 3')
            startKm = []
            endKm = []
            for element in riverNamesDrop:
                if element[2] == minimalKm:
                    startKm.append(element[-1][-2:])
                if element[2] == maximalKm:
                    endKm.append(element[-1][-2:])
            print(startKm)
            start = ['_'.join(item) for item in startKm]
            start = '_'.join(start)
            end = ['_'.join(item) for item in endKm]
            end = '_'.join(end)
            nazwa = branch.riverName.split("_")[0] + '_' + start + '-' + end



        elif countIndividualNamesKm == 4 and countIndividualNames == 4:
            print('4 na 4')
            startKm = []
            endKm = []
            for element in riverNamesDrop:
                if element[2] == minimalKm:
                    startKm.append(element[-1][-2:])
                if element[2] == maximalKm:
                    endKm.append(element[-1][-2:])
            start = ['_'.join(item) for item in startKm]
            start = '_'.join(start)
            end = ['_'.join(item) for item in endKm]
            end = '_'.join(end)
            nazwa = branch.riverName.split("_")[0] + '_' + start + '-' + end

        else:
            print(countIndividualNamesKm, countIndividualNames)
            raise 'nie nadpisano nazwa'
        if nazwaOld == nazwa:
            print(countIndividualNamesKm, countIndividualNames)
            raise 'nie nadpisano nazwa'
        linklist = []
        riverNamesDrop = []
        nazwaOld=nazwa
        print(" ------------------------ ")

        branchDictNames[str(branch.riverName).upper()] = nazwa

print(branchDictNames)

for xs in XS_dat:
    name = str(xs.riverCode).upper()
    print(name)
    if str(name).upper() in branchDictNames.keys():
        xs.riverCode = branchDictNames[name]
        print(xs.riverCode)
    xs.print_txt(f, zaok=None, rr=None)
f.close()

for branch in nwk.branchList:
    name = str(branch.riverName).upper()
    if 'PTZ_6' in name:
        print('ptz 6')
        print(name, branchDictNames[name])
    if str(name).upper() in branchDictNames.keys():
        print('Zmiana nazwy z {} na {}'.format(name, branchDictNames[name]))
        branch.riverName = branchDictNames[name]
    name = str(branch.connectRiver).upper()
    if str(name).upper() in branchDictNames.keys():
        branch.connectRiver = branchDictNames[name]
    name = str(branch.connectTopoID).upper()
    if str(name).upper() in branchDictNames.keys():
        branch.connectTopoID = branchDictNames[name]
nwk.print_to_nwk(fileWynik)
fileWynik.close()

print("done")