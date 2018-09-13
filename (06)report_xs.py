#from classes import  Xs, Link, printowanie
from classes import *
from functions import *
import xlsxwriter
file = open(r'C:\!!Mode ISOKII\!ISOK II\Dobka\hec_res\Dobka_man.txt', 'r')
output = r'C:\!!Mode ISOKII\!ISOK II\Dobka\hec_res\Dobka_report_xs.xlsx'
XS_dat, XS_order = read_XSraw(file)
raport_XS(XS_dat, output)