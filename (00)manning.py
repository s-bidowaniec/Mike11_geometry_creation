from functions import *
import pdb
import bisect
# lokacja dbf z maningiem, jesli base manning none - pomija przypisanie manninga, ustawic wtedy tez rr na none
dbf = r'C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Projekt_hecras\wksport_08.11.18\Manning_Output.dbf'
#baseManning = None   #<--- wylacza przypisanie maninga z dbf
if dbf != None: baseManning = read_manning_dbf(dbf)   #<--- zaczytanie tabeli dbf do manninga
else: baseManning = None
# lokacja rawdata
input = r'C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v1\S01_Czarny_Potok_raw.txt'
file = open(input, 'r')
crossSections, order = read_XSraw(file)
# output file
output = r'C:\!!Mode ISOKII\!ISOK II\Czarny Potok\Mike_v1\S01_Czarny_Potok_man.txt'
f = open(output, 'w')
# epsilon to parametr algorytmu rdp od usuwania punktow(im wyższy tym więcej usuwa), ustawiony na None pomija funkcję
# dajemy tak od 0.04 do 0.08
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
        
        key1 = '{} {} {}'.format(str(element.riverCode).title(), element.reachCode, round(float("{0:.1"
                                                                                   "f}".format(element.km)),0))
        
        key2 = '{} {} {}'.format(str(element.riverCode).title(), element.reachCode, round(float("{0:.1"
                                                                                   "f}".format(element.km)),0)+1)
        key3 = '{} {} {}'.format(str(element.riverCode).title(), element.reachCode, round(float("{0:.1"
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
            # przesuniecie na zero
            start_point = min([float(x.station) for x in element.points])

            for point in element.points:
                stat = float(point.station)-start_point
                index = bisect.bisect_left(list(manningDats.punkty.keys()), stat)
                key = list(manningDats.punkty.keys())[index-1]
                stat2 = manningDats.punkty[key].station
                #if min([float(x.station) for x in element.points]) < 0:
                    #pdb.set_trace()
                if stat2 > stat:
                    if stat == 0:
                        key = list(manningDats.punkty.keys())[0]
                        if rr != None:
                            point.manning = (manningDats.punkty[key].manning)/rr
                            #pdb.set_trace()
                        elif rr == None:
                            point.manning = manningDats.punkty[key].manning
                    else:
                        print('Warning; przypisano manning od prawej zamiast od lewej. Klucz: {}; station: {}'.format(key1, key))
                        print(stat2, stat)
                else:
                    if rr != None:
                        point.manning = (manningDats.punkty[key].manning) / rr
                        # pdb.set_trace()
                    elif rr == None:
                        point.manning = manningDats.punkty[key].manning
        else:
            print('Warning; nie odnaleziono zgodnosci kluczy pomiedzy raw data(txt) a manning(dbf). Klucz: {}'.format(key2))
    else:
        pass
    if epsilon != None:
        element.rdp_pkt(epsilon)
    element.print_txt(f, zaok, rr)
f.close()
