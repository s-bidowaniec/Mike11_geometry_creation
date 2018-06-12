from classes import *
from functions import *
# plik wsadowy nwk, pobierana jest lista punktow oraz branchy do ktorych dopisywane sa dane z nowych linkow
nwkInputDir = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\BUDKOWICZANKA_S01_Qn.nwk11"
fileWejscieNWK = open(nwkInputDir, 'r')
nwk = read_NWK(fileWejscieNWK)

# nowy plik NWK z naniesionymi mostasmi
nwkOutDir = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\BUDKOWICZANKA_S01_Qn_bridgeTest2.nwk11"
if nwkOutDir == nwkInputDir:
    raise ValueError('NWK input file equals NWK output file', 'foo', 'bar', 'baz')
fileWynikNWK = open(nwkOutDir, "w")
# execute rdp on branches
nwk.nwk_rdp()
# save nwk to new file
nwk.print_to_nwk(fileWynikNWK)
