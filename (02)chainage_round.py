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

nwk = read_NWK(fileWejscieNWK)

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
