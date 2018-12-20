from functions import *
from classes import *
#---------------------------------------------------------------------------------------------------------------------
# plik wsadowy NWK
inputNwkDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v3.01_13.12\testy\S01_Czarny_Potok_link.nwk11"
# nowy plik NWK
outputNwkDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v3.01_13.12\testy\S01_Czarny_Potok_sort.nwk11"
#---------------------------------------------------------------------------------------------------------------------

""" czy ma zrobic redukcje pkt w branch (True, False) """
robicRDP = False
#---------------------------------------------------------------------------------------------------------------------

if inputNwkDir == outputNwkDir:
    raise 'Error: input == output'
# Otwarcie plikow
if inputNwkDir != outputNwkDir:
    fileWejscieNWK = open(inputNwkDir, 'r')
    fileWynik = open(outputNwkDir, "w")

nwk = read_NWK(fileWejscieNWK)

### Drukowanie utworzonej struktury do pliku *.nwk
if robicRDP == True:
    nwk.nwk_rdp()
nwk.sort_points()
nwk.branchList.sort(key=lambda x: x.riverName.replace("KP_", "zzzc").replace("LTZ_", "zzza").replace("PTZ_","zzzb"))
nwk.print_to_nwk(fileWynik)
fileWynik.close()
fileWejscieNWK.close()
print("done")