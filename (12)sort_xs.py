from functions import *

# -------------------------------- PLIKI WSADOWE --------------------------------------------------------------
"""plik wsadowy rawdata"""
xsInputDir = r"C:\!!Mode ISOKII\!Etap1\Budkowiczanka_kalibracja\S01_BUDKOWICZANKA_v2.01\S01_Budkowiczanka_shift.txt"
fileWejscieXS = open(xsInputDir,'r')
bazaXsRawData, XsOrder = read_XSraw(fileWejscieXS)

# --------------------------------- PLIKI WYNIKOWE -----------------------------------------------------------
# nowy plik XSrawData
xsOutputDir = r"C:\!!Mode ISOKII\!Etap1\Budkowiczanka_kalibracja\S01_BUDKOWICZANKA_v2.01\S01_Budkowiczanka_sort.txt"
if xsInputDir == xsOutputDir:
    raise ValueError('XS input file equals XS output file', 'foo', 'bar', 'baz')
fileWynikXS = open(xsOutputDir,'w')

# --------------------------------- SORTOWANIE -----------------------------------------------------------
bazaXsRawData.sort(key=lambda x: x.riverCode.replace("KP_", "zzzc").replace("LTZ_", "zzza").replace("PTZ_","zzzb"))
# --------------------------------- ZAPIS -----------------------------------------------------------
for element in bazaXsRawData:
    element.print_txt(fileWynikXS, None, 1)