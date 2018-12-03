#from classes import  Xs, Link, printowanie
from classes import *
from functions import *
import xlsxwriter
file = open(r'C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v2.01\xs_DO_RAPORT.txt', 'r')
output = r'C:\!!Mode ISOKII\!ISOK II\Czarny Potok\S01_Czarny_Potok_v2.01\Czarny_potok_report_xs.xlsx'
XS_dat, XS_order = read_XSraw(file)
raport_XS(XS_dat, output)