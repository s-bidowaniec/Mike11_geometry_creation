# -*- coding: utf-8 -*-

from classes import *
from functions import *

inp = r"C:\Users\kprzewdziek\Downloads\S01_Dobka_bridge_v3.nwk11"
out = r"C:\Users\kprzewdziek\Downloads\S01_Dobka_bridge_v4.nwk11"

finp = open(inp, 'r')
fout = open(out, 'w')

nwk = read_NWK(finp)
nwk.print_to_nwk(fout)
fout.close()
print("done")

