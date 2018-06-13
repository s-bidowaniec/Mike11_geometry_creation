#from classes import  Xs, Link, printowanie
from functions import read_XSraw, raport_XS
import xlsxwriter
file = open(r'C:\!!Modele ISOKII\BUDKOWICZANKA\Eksport_2\Budkowiczanka_Q2.txt', 'r')
output = r'C:\!!Modele ISOKII\BUDKOWICZANKA\Eksport_2\test.xlsx'
XS_dat = read_XSraw(file)
raport_XS(XS_dat, output)