# -*- coding: utf-8 -*-

############################################## SB ##########################################################
from functions import read_XSraw, printowanie, read_NWK
from classes import *
import time

# plik wsadowy rawdata,
inputXS = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v3_26.11\S01_Czarny_Potok_man.txt"
# plik wsadowy nwk, pobierane sa poloaczenia link do generacji nazw dla branch
inputNWK = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v3_26.11\S01_Czarny_Potok_round.nwk11"

# -----------------------------------------------------------------------------------------------------------

# plik wynikowy przekroje z nazwami
outputXS = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v3_26.11\S01_Czarny_Potok_renamed.txt"
# plik wynikowy NWK z nazwami
outputNWK = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v3_26.11\S01_Czarny_Potok_renamed.nwk11"

if outputXS == inputXS or outputNWK == inputNWK or inputNWK == outputXS or inputXS == outputNWK:
    raise 'Error: ten sam plik na wejsciu i wyjsciu'
else:
    f = open(outputXS, 'w')
    fileWynik = open(outputNWK, "w")
    fileWejscieXS = open(inputXS, 'r')
    fileWejscieNWK = open(inputNWK, 'r')
XS_dat, XS_order = read_XSraw(fileWejscieXS)
print("Raw data zaczytane")

# ------------------------------------------------------------------------------------------------------------------- #


nwk = read_NWK(fileWejscieNWK)
print("NWK zaczytane")

branchDictNames = {}
### iterowanie po branchach
linklist = []
riverNamesDrop = []
nazwaOld = '-'
for branch in nwk.branchList:
    if "PTZ_" in branch.riverName or "LTZ_" in branch.riverName:
        for linkB in nwk.branchList:
            print('a', linkB.riverName) #, linkB.connectRiver, branch.riverName, linkB.connectTopoID)
            #print('b', branch.riverName, linkB.connectRiver)


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
        try:
            minimalKm = min([float(i[2]) for i in riverNames])
        except:
            import pdb
            pdb.set_trace()
        maximalKm = max([float(i[2]) for i in riverNames])
        for element in riverNames:
            if element[2] == minimalKm or element[2] == maximalKm:
                riverNamesDrop.append(element)

        for element in riverNamesDrop:
            rzad_brnacha = int(element[-1][0])
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
            nazwa = "{}-{}_{}_{}-{}".format(branch.riverName.split("_")[0], rzad_brnacha, connectedBranchName, startKm, endKm)
            #print("{}_{}_{}-{}".format(branch.riverName.split("_")[0], connectedBranchName,startKm,endKm))

        elif countIndividualNamesKm == 1 and countIndividualNames == 1:

            connectedBranchName = riverNamesDrop[0][-1][1]
            for element in riverNamesDrop:
                if element[2] == minimalKm:
                    startKm = element[-1][-1]
                if element[2] == maximalKm:
                    endKm = element[-1][-1]

            nazwa = "{}-{}_{}_{}".format(branch.riverName.split("_")[0], rzad_brnacha, connectedBranchName,startKm)
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
            nazwa = "{}-{}_{}_{}-{}_{}".format(branch.riverName.split("_")[0], rzad_brnacha, startKm[0], startKm[1], endKm[0], endKm[1])

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
                nazwa = "{}-{}_{}_{}_{}-{}_{}".format(branch.riverName.split("_")[0],rzad_brnacha, startKm[0][0], startKm[0][1],
                                                   endKm2[0], endKm2[1], endKm[0][1])
                #print(nazwa)

            elif len(startKm) == 2 and len(endKm) == 1:
                index = 0
                for element in startKm:
                    if element[0] == endKm[0][0]:
                        startKm2 = element
                        startKm.pop(index)
                    index+=1

                nazwa = "{}-{}_{}_{}_{}_{}-{}".format(branch.riverName.split("_")[0],rzad_brnacha, startKm[0][0], startKm[0][1], startKm2[0], startKm2[1], endKm[0][1])
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
                nazwa = "{}-{}_{}_{}-{}_{}_{}_{}".format(branch.riverName.split("_")[0], rzad_brnacha, startKm[0][0], startKm[0][1],
                                                   endKm[0][0], endKm[0][1],endKm[1][0],endKm[1][1])
            elif len(startKm) == 2 and len(endKm) == 1:
                nazwa = "{}-{}_{}_{}_{}_{}-{}_{}".format(branch.riverName.split("_")[0], rzad_brnacha, startKm[0][0], startKm[0][1],
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
            nazwa = "{}-{}_{}_{}-{}_{}_{}-{}".format(branch.riverName.split("_")[0], rzad_brnacha, river1[0], river1[1],
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
            # raise 'nie nadpisano nazwa'
        linklist = []
        riverNamesDrop = []
        nazwaOld=nazwa
        print(" ------------------------ ")
        print (branch.riverName)
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
        print(str(name).upper())
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