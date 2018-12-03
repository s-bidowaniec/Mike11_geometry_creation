import openpyxl, time
import dbm
import pickle
import copy
from classes import Bridge
from functions import *
# -------------------------------- PARAMETRY --------------------------------------------
mnoznik = 0.04
# -------------------------------- PLIKI WSADOWE --------------------------------------------------------------
"""plik wsadowy rawdata, pobiera manninga i przelicza"""
xsInputDir = r"C:\!!Mode ISOKII\!ISOK II\testy\pszczynka_test.txt"
fileWejscieXS = open(xsInputDir,'r')
bazaXsRawData, XsOrder = read_XSraw(fileWejscieXS)

# --------------------------------- PLIKI WYNIKOWE -----------------------------------------------------------
# nowy plik XSrawData z naniesionymi mostasmi
xsOutputDir = r"C:\!!Mode ISOKII\!ISOK II\testy\pszczynka_out.txt"
if xsInputDir == xsOutputDir:
    raise ValueError('XS input file equals XS output file', 'foo', 'bar', 'baz')
fileWynikXS = open(xsOutputDir,'w')

for element in list(XsOrder.values()):
    for pkt in element.points:
        pkt.manning = str(float(pkt.manning)*mnoznik)
    element.print_txt(fileWynikXS, None, 1)
