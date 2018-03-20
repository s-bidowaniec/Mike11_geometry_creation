from classes import ManningXS, Pkt, PktN, Xs
from dbfread import DBF
def read_xs_raw(file):
    lines = file.readlines()
    row = 0
    XSnum = 0
    XS_dat = []
    for line in lines:

        if row == 0:
            if '**' in line:
                row = -1
            else:
                XS_dat.append(Xs())
                XS_dat[XSnum].reachCode = line.replace("\n", "")
        elif row == 1:
            XS_dat[XSnum].riverCode = line.replace("\n", "")
        elif row == 2:
            XS_dat[XSnum].km = float("{0:.2f}".format(float(line)))
        elif 'COORDINATES' in old:
            XS_dat[XSnum].cords = line
        elif 'FLOW DIRECTION' in old:
            XS_dat[XSnum].fd = line #flow direction
        elif 'PROTECT DATA' in old:
            XS_dat[XSnum].pd = line #protect data
        elif 'DATUM' in old:
            XS_dat[XSnum].datum = line #datum
        elif 'CLOSED SECTION' in old:
            XS_dat[XSnum].cs = line #closed
        elif 'RADIUS TYPE' in old:
            XS_dat[XSnum].rt = line # radius type
        elif 'DIVIDE X-Section' in old:
            XS_dat[XSnum].dx = line # divide xs
        elif 'SECTION ID' in old:
            XS_dat[XSnum].id = str(line).replace(" ","") # section id
        elif 'INTERPOLATED' in old:
            XS_dat[XSnum].inter = line # interpolated
        elif 'ANGLE' in old:
            XS_dat[XSnum].angle = line # angle
        elif 'RESISTANCE NUMBERS' in old:
            XS_dat[XSnum].rn = line # resistance number
        elif 'PROFILE' in line:
            XS_dat[XSnum].profile = str(line).split()[-1] # profile
        elif sum(c.isdigit() for c in line) > 5 and row > 5 and '<#' in line:
            XS_dat[XSnum].dane.append(line)
            XS_dat[XSnum].points.append(Pkt(line))
        elif 'LEVEL PARAMS' in line:
            row_num = row
            row = -100
        elif row == -99 and 'LEVEL PARAMS' not in line:
            XS_dat[XSnum].lp = line # level params
            row = int(row_num)
        elif '**' in line:
            row = -1
            XSnum += 1
        else:
            pass
        row += 1
        old = line
    return XS_dat

def read_manning_dbf(dbf):
    base = {}
    for record in DBF(dbf):
        kod = '{} {} {}'.format(record['RiverCode'], record['ReachCode'], int(float("{0:.2f}".format(record['ProfileM']))))
        if kod in base.keys():
            base[kod].dodaj(record)
        else:
            base[kod] = ManningXS(record)
    return base
