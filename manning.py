from Functions import *
import bisect
#lokacja dbf z maningiem
dbf = r'E:\!!Modele_IsokII\Zlotna_161152\Mike\V1\manning.dbf'
baseManning = read_manning_dbf(dbf)
#lokacja rawdata
file = open(r'E:\!!Modele_IsokII\Zlotna_161152\Mike\V1\S01_Zlotna_Qn_raw.txt', 'r')
crossSections = read_xs_raw(file)
#output file
output = r'E:\!!Modele_IsokII\Zlotna_161152\Mike\V1\S01_Zlotna_Qn_man.txt'
f = open(output, 'w')
#epsilon to parametr algorytmu rdp od usuwania punktow, ustawiony na None pomija funkcję
epsilon = 0.08
#zaokraglenie km przekroi(podać ilość miejsc po przecinku, lub None - pominięcie
zaok = 0
#bazowa wartosc manninga do relative resistance(distibutet, relative resistance) None - wartosci normalne (distributet, manning's n)
rr = 0.04
for element in crossSections:
    key1 = '{} {} {}'.format(element.riverCode, element.reachCode, int(float("{0:.2f}".format(element.km))))
    if key1 in baseManning.keys():
        manningDats = baseManning[key1]
        for point in element.points:
            stat = float(point.station)
            index = bisect.bisect_left(list(manningDats.punkty.keys()), stat)
            key = list(manningDats.punkty.keys())[index-1]
            stat2 = manningDats.punkty[key].station
            if stat2 > stat:
                if stat == 0:
                    key = list(manningDats.punkty.keys())[0]
                    point.manning = manningDats.punkty[key].manning
                else:
                    print('Warning; przypisano manning od prawej zamiast od lewej. Klucz: {}; station: {}'.format(key1, key))
                    print(stat2, stat)
            else:
                point.manning = manningDats.punkty[key].manning
    else:
        print('Warning; nie odnaleziono zgodnosci kluczy pomiedzy raw data(txt) a manning(dbf). Klucz: {}'.format(key))
    if epsilon != None:
        element.rdp_pkt(epsilon)
    element.print_txt(f, zaok, rr)
f.close()
