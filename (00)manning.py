from functions import *

import bisect
# lokacja dbf z maningiem, jesli base manning none - pomija przypisanie manninga, ustawic wtedy tez rr na none
dbf = r'K:\Wymiana danych\Staszek\KORN\Robocze_v1_linki_2\20180615_Manning.dbf'
#baseManning = None   #<--- wylacza przypisanie maninga z dbf
baseManning = read_manning_dbf(dbf)   #<--- zaczytanie tabeli dbf do manninga
# lokacja rawdata
input = r'K:\Wymiana danych\Staszek\KORN\Robocze_v1_linki_2\Swidnik_4_raw.txt'
file = open(input, 'r')
crossSections, order = read_XSraw(file)
# output file
output = r'K:\Wymiana danych\Staszek\KORN\Robocze_v1_linki_2\Swidnik_4_man.txt'
f = open(output, 'w')
# epsilon to parametr algorytmu rdp od usuwania punktow(im wyższy tym więcej usuwa), ustawiony na None pomija funkcję
epsilon = 0.04
# zaokraglenie km przekroi(podać ilość miejsc po przecinku, lub None - pominięcie
zaok = 0
# bazowa wartosc manninga do relative resistance(distibutet, relative resistance) None - wartosci normalne (distributet, manning's n)
rr = None
# przypisanie typu przekroju w polu id, dziala jesli typXS równy True
typXS = True
if input == output:
    raise 'Error'
# --------------------------------------------------------------------------------------------------------------------- #
if baseManning is None:
    rr = None
else:
    pass
for element in crossSections:
    if baseManning is not None:
        manningDats = None
        
        key1 = '{} {} {}'.format(element.riverCode, element.reachCode, round(float("{0:.1"
                                                                                   "f}".format(element.km)),0))
        
        key2 = '{} {} {}'.format(element.riverCode, element.reachCode, round(float("{0:.1"
                                                                                   "f}".format(element.km)),0)+1)
        key3 = '{} {} {}'.format(element.riverCode, element.reachCode, round(float("{0:.1"
                                                                                   "f}".format(element.km)),0)-1)
        
        
        if key1 in baseManning.keys():
            manningDats = baseManning[key1]

        elif key2 in baseManning.keys():
            manningDats = baseManning[key2]

        elif key3 in baseManning.keys():
            manningDats = baseManning[key3]

        if manningDats != None:
            
            if typXS is True:
                element.id = manningDats.typXS

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
    else:
        pass
    if epsilon != None:
        element.rdp_pkt(epsilon)
    element.print_txt(f, zaok, rr)
f.close()
