#from classes import  Xs, Link, printowanie
from classes import *
from functions import *
import xlsxwriter
file = open(r'K:\Wymiana danych\Karol\Staszek\S04_Przemsza_Mann.txt', 'r')
output = r'K:\Wymiana danych\Karol\Staszek\S04_Przemsza_Mann.xlsx'
XS_dat, XS_order = read_XSraw(file)
raport_XS(XS_dat, output)