import openpyxl, time
import dbm
import pickle
import copy
from classes import Bridge
from functions import *
# -------------------------------- PARAMETRY --------------------------------------------
# linia 41, wartość jest dodawana do istniejacej wartości manninga, można zmieniać wzór przemnażać itp, river do warunku w lini 33
wart = 0.01
river = 'CZARNY_POTOK'
startKM = 0
endKM = 1968100
if startKM > endKM: endKM, startKM = startKM, endKM
# -------------------------------- PLIKI WSADOWE --------------------------------------------------------------
"""plik wsadowy rawdata, pobiera manninga i przelicza"""
xsInputDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v3.01_05.02_czyszczone0602\01_MIKE11\03_S01_Czarny_Potok_XNS\man_0.01.txt"
fileWejscieXS = open(xsInputDir,'r')
bazaXsRawData, XsOrder = read_XSraw(fileWejscieXS)

# --------------------------------- PLIKI WYNIKOWE -----------------------------------------------------------
# nowy plik XSrawData z naniesionymi mostasmi
xsOutputDir = r"C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v3.01_05.02_czyszczone0602\01_MIKE11\03_S01_Czarny_Potok_XNS\man_k_0.01.txt"
if xsInputDir == xsOutputDir:
    raise ValueError('XS input file equals XS output file', 'foo', 'bar', 'baz')
fileWynikXS = open(xsOutputDir,'w')
"""
Kody markerów:
marker 1 -> '<#1>'
marker 2 -> '<#2>'
marker 3 -> '<#4>'
marker 4 -> '<#8>'
marker 5 -> '<#16>'
marker 1/4 -> '<#9>'
marker 3/5 -> '<#20>'
"""
for element in list(XsOrder.values()):
    if element.riverCode.lower() in river.lower() and startKM <= element.km <= endKM:
        flag = 1
        for pkt in element.points:
            if pkt.kod == '<#8>' or pkt.kod == '<#9>':
                flag = 1

            if flag:
                pkt.manning = str(float(pkt.manning)+wart)                 # <- Tutaj wzorek na przeliczenie manninga

            if pkt.kod == '<#16>' or pkt.kod == '<#20>':
                flag = 1
    element.print_txt(fileWynikXS, None, 1)
