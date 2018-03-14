import math
from rdp import rdp
from operator import itemgetter
import time
import matplotlib.pyplot as plt

def get_xy_delta(self):
    if self.right[0] > self.left[0]:
        x1, x2 = 2, -2
    elif self.right[0] < self.left[0]:
        x1, x2 = -2, 2
    else:
        x1, x2 = 0, 0
    if self.right[1] > self.left[1]:
        y1, y2 = 2, -2
    elif self.right[1] < self.left[1]:
        y1, y2 = -2, 2
    else:
        y1, y2 = 0, 0
    return(x1,y1,x2,y2)


class XS(object):
    def __init__(self):
        self.dane = []
    def kordy(self):
        self.left = self.cords.split()[1:3]
        self.right = self.cords.split()[3:5]
        elev_points = []
        #print(len(self.dane))
        for element in self.dane:
            try:
                h = element.split()[1]
                elev_points.append(h)
            except:
                print(element)
        #print(self.reach_code, self.km)
        self.max_left = max(elev_points[0:5])
        self.min_left = min(elev_points[0:10])
        self.mean_left = float(self.max_left) / 5
        self.max_right = max(elev_points[-5:-1])
        self.min_right = min(elev_points[-10:-1])
        self.mean_right = float(self.max_right) / 5
    pass

class link(object):
    def __init__(self, object1, object2):
        self.object1 = object1
        self.object2 = object2
        self.pkt = []
        self.river1 = object1.river_code
        self.chain1 = object1.km
        self.river2 = object2.river_code
        self.chain2 = object2.km
        self.rzad = 0
        self.kolej = 0
        self.main_chan = "Riv"
        self.main_km = 0
        self.main_site = "C"
        self.topo = "Topo"

    def data_definition(self):
        self.main_km = int(self.main_km)
        if self.rzad == 0:
            print("brak przypisania")
            print(self.river1, self.chain1, self.river2, self.chain2)
        else:
            if "LTZ" in self.object1.river_code or "LTZ" in self.object2.river_code:
                self.main_site = "L"
            elif "PTZ" in self.object1.river_code or "PTZ" in self.object2.river_code:
                self.main_site = "P"
            if self.kolej == 1:
                self.connections = [self.object1.river_code, self.object1.km, self.object2.river_code, self.object2.km]
                x1, y1, x2, y2 = get_xy_delta(self.object1)

            elif self.kolej == 2:
                self.connections = [self.object2.river_code, self.object2.km, self.object1.river_code, self.object1.km]
                x2, y2, x1, y1 = get_xy_delta(self.object1)
            self.definitions = ["KP_"+str(self.rzad)+"_"+str(self.main_chan)+"_"+str(self.main_km)+"_"+self.main_site, self.topo,0,5,0,10000,1]
            h_elev = float(max(self.object1.max_left, self.object2.max_right))
            h2_elev = float((self.object2.min_right))
            self.geometry = [h_elev, h2_elev]
            self.cross_section = [[0,0],[0.1, float(self.object1.len)], [3, float(self.object1.len)]]
            self.points = [float(self.object1.left[0]) +x1, float(self.object1.left[1]) +y1,
                           float(self.object1.left[0]) +x2, float(self.object1.left[1]) +y2]


def printowanie(list_lin, num):
    point_list = []
    f = open('branche.txt', 'w')
    f.write("   [POINTS]\n")
    for element in list_lin:
        point1 = str(element.points[0:2])
        elem = [num+1,point1]
        point_list.append(elem)
        f.write("      point = "+str(elem).replace("[","").replace("]","").replace("'","")+", 1, 0.00, 0"+"\n")
        point2 = str(element.points[2:4])
        elem2 = [num+2, point2]
        point_list.append(elem2)
        f.write("      point = "+str(elem2).replace("[","").replace("]","").replace("'","")+", 1, 5.00, 0"+"\n")
        num+=2
        element.points2=[num-1, num]
    f.write("-------------\n\n")
    for element in list_lin:
        f.write("      [branch]\n")
        f.write("         definitions = "+str(element.definitions).replace("[","").replace("]","") + "\n")
        f.write("         connections = "+str(element.connections).replace("[","").replace("]","") + "\n")
        f.write("         points = "+str(element.points2).replace("[","").replace("]","") + "\n")
        f.write("         [linkchannel]\n")
        f.write("            Geometry = "+str(element.geometry).replace("[","").replace("]","") + ", 0\n")
        f.write("            HeadLossFactors = 0.5, 1, 0, 1, 0.5, 1, 0, 1\n")
        f.write("            Bed_Resistance = 1, 0.03\n")
        f.write("            [Cross_Section]\n")
        for data in element.cross_section:
            f.write("               Data = "+str(data).replace("[","").replace("]","") + "\n")
        f.write("            EndSect  // Cross_Section\n\n")
        f.write("         EndSect  // linkchannel\n\n")
        f.write("      EndSect  // branch\n\n")
    return (point_list)

#bridges----------------------------------------------------------------------------------------------------------------

def distance(x1, x2, y1, y2):
    try:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    except:
        return False

def is_between(x1, y1, x, y, x2, y2):
    #print(round(distance(X1, x, Y1, y)) + round(distance(x, X2, y, Y2)), round(distance(X1, X2, Y1, Y2)))
    #val = round(distance(x1, x, y1, y)) + round(distance(x, x2, y, y2)) == round(distance(x1, x2, y1, y2))
    val = False
    if x1 < x < x2 or x1 > x > x2 and y1 < y < y2 or y1 > y > y2:
        val = True
    #elif x == x1 and y == y1 or x == x2 and y == y2:
            #val == True
    return val

def is_between2(x1, y1, x, y, x2, y2):
    val = False
    val = x1 < x < x2 and y1 < y < y2
    if val == False:
        val = x2 < x < x1 and y2 < y < y1
    if val == False:
        val = x2 < x < x1 and y2 > y > y1
    if val == False:
        val = x2 > x > x1 and y2 < y < y1
    return val
def line_intersection(X1, Y1, X2, Y2, X3, Y3, X4, Y4):
    line1 = [[X1, Y1], [X2, Y2]]
    line2 = [[X3, Y3], [X4, Y4]]
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        x, y, b, c = None, None, None, None
    else:
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        b = (is_between(X3, Y3, x, y, X4, Y4))
        c = (is_between(X1, Y1, x, y, X2, Y2))

    return [x, y, b, c]



class point(object):
    def __init__(self, lp, x, y, z, kod="nul", cos="nul", ogon='nul'):
        self.lp = int(float(lp.replace("o","0").replace("O","0")))
        self.x = float(x.replace("o","0").replace("O","0"))
        self.y = float(y.replace("o","0").replace("O","0"))
        self.z = float(z.replace("o","0").replace("O","0"))
        self.kod = str(kod)
        self.cos = [cos]

class XS_t(object):
    def __init__(self, file):
        name = str(file).replace("\\"," ").split()[-3]
        name = name.replace(".", " ").replace("_", " ").split()
        for element in name:
            if element[0].isdigit():
                name = element
        self.name = name
        self.km = 0
        self.rzeka = "Riv"
        self.data = "01.01.1990"
        self.type = "none"
        self.dane = []
        self.point_data = []
        self.geom2 = []
        for line in file.read().split("\n"):
            napis = list(line.replace("\t","  "))
            licznik = 0
            while licznik < len(napis):
                if napis[licznik] == ' ':
                    try:
                        while napis[licznik + 1] == ' ':
                            del napis[licznik]
                    except:
                        pass
                licznik += 1
            napis = "".join(napis).replace('*', '').replace('\r\n','')  # koniec usuwania powielonych znakow podzialu, zamiana listy na string
            line2 = napis.replace("\t"," ").replace("  "," ")
            numbers = sum(c.isdigit() for c in line2)
            if numbers < 14:
                self.dane.append(line2)

            else:
                line3 = line2.split(' ')
                if len(line3)>6:
                    cos = line3[6:]
                    line3=line3[:6]
                    line3.append(cos)
                #print(line3)
                try:
                    int(float(line3[0]))
                    self.point_data.append(point(*line3[:]))
                except:
                    print(line3)
                    self.point_data.append(point(*line3[1:]))

        r = 0
        while sum(c.islower() for c in self.dane[r]) < 1:
            r+=1
        if "rzek" in str.lower(self.dane[r]) or "zeka" in str.lower(self.dane[0]):
            self.rzeka = self.dane[r].split(':')[1]
        else:
            print("Brak: river def", self.lp)
        if "przek" in str.lower(self.dane[r+1]) or "rzekr" in str.lower(self.dane[1]):
            self.lp = self.dane[r+1].split(':')[1]
        else:
            print("Brak: lp def", self.lp)
        if "dat" in str.lower(self.dane[r+2]) or "ata" in str.lower(self.dane[2]):
            self.data = self.dane[r+2].split(':')[1]
        else:
            print("Brak: data def", self.lp)
        if "typ" in str.lower(self.dane[r+3]) or "obiekt" in str.lower(self.dane[3]):
            self.type = self.dane[r+3].split(':')[1]
        elif "kąt" in str.lower(self.dane[r+4]) or "krzyzowan" in str.lower(self.dane[3]):
            self.kat = self.dane[r + 4].split(':')[1]

        try:
            if "foto" in str.lower(self.dane[r+4]):
                self.foto = self.dane[r+4].split(':')[1]
        except:
            pass
        try:
            if "admin" in str.lower(self.dane[r+5]):
                self.admin = self.dane[r+5].split(':')[1]
        except:
            self.admin = "None"
        try:
            if "uwagi" in str.lower(self.dane[r+6]):
                self.uwagi = self.dane[r+6].split(':')[1]
        except:
            self.uwagi = "None"
        try:
            if "szer" in str.lower(self.dane[r+7]):
                self.szer = self.dane[r+7].split(':')[1]
        except:
            self.szer = "None"


        if self.type == "none" or self.type == '':
            print("Brak: type def", self.lp)
            try:
                if "obie" in str(self.dane[-4:-1]).lower():
                    self.type = "obiekt"
                else:
                    kody = []
                    for k in self.point_data:
                        kody.append(k.kod)
                    napis = str(kody)
                    if '40' in napis:
                        self.type = "obiekt"
                    else:
                        pass
            except:
                pass
    def get_far(self):
        line = []
        for poi in self.point_data:
            #print(poi.cos, poi.x, poi.y)
            if "zww" in str(poi.cos).lower():
                line.append(poi.x)
                line.append(poi.y)
        return(line[0],line[1],line[2],line[3])

    def distance(self):
        self.pierwszy_punkt = self.point_data[0]
        self.pozost_punkty = self.point_data[1:]
        self.punkty_odleglosci = {}
        self.sortowane = []
        x1, y1, z1 = self.pierwszy_punkt.xp, self.pierwszy_punkt.yp, self.pierwszy_punkt.z
        for i in self.point_data:
            x2, y2, z2 = i.xp, i.yp, i.z
            dx = math.fabs(x2 - x1)
            dy = math.fabs(y2 - y1)
            dist = math.sqrt((dx**2) + (dy**2))
            i.dist = dist
    def dist_sort(self):
        self.point_data = sorted(self.point_data, key=operator.attrgetter('dist'))


    ################################################################################################################
    """obliczanie dlugosci przekroju i dolnej pikiety"""
    def get_culver_len(self):

        for pkt in self.point_data:
            if "66" in pkt.kod or "7" in pkt.kod:
                print(pkt.y, pkt.xp, pkt.x, pkt.yp)
                self.culvert_len = math.sqrt((float(pkt.y) - float(pkt.xp)) ** 2 + (float(pkt.x) - float(pkt.yp)) ** 2)
                self.culvert_downS = pkt.z

    '''generuje punkty przeciecia'''
    def gen_pkt(self):
        if len(self.geom) == 0:
            print("geom error")
            time.sleep(5)
            self.geom = self.geom2
        '''jesli jeden pkt spodu konstrukcji dodanie pomocniczych'''
        if len(self.geom) == 1:
            self.geom.insert(0,[self.geom[0][0] - 0.5, self.geom[0][1]])
            self.geom.append([self.geom[0][0] + 0.5, self.geom[0][1]])
        '''jesli wiecej niz jeden punkt opisujacy zpod konstrukcji, tworzy liste punktow przeciecia prostych z konstrukcji na lini koryta'''
        if len(self.geom) > 1:
            pointLis = []
            for i in range(len(self.kor) - 1):
                for x in range(len(self.geom) - 1):
                    point = line_intersection(self.kor[i][0], self.kor[i][1], self.kor[i + 1][0],
                                              self.kor[i + 1][1], self.geom[x][0], self.geom[x][1],
                                              self.geom[x + 1][0], self.geom[x + 1][1])
                    if point[-1] == True:
                        pointLis.append(point)
            print("line 312 point len: ", len(pointLis))
            '''obliczenie odleglosci wygenerowanych punktow od punktow skrajnych konstrukcji'''
            for pkt in pointLis:
                if self.geom[0] == self.geom[-1]:
                    raise ('kryzys 2')
                dis1 = distance(self.geom[0][0], pkt[0], self.geom[0][1], pkt[1])
                pkt.append(dis1)
                dis2 = distance(self.geom[-1][0], pkt[0], self.geom[-1][1], pkt[1])
                pkt.append(dis2)

            """wybor punktow najblizszych, z usunieciem prawa lewa"""  ##################################################
            """sredni station dla konstrukcji"""
            midle_station = []
            for i in range(len(self.geom)):
                midle_station.append(self.geom[i][0])
            midle_station = sum(midle_station) / float(len(midle_station))
            """dwie listy pkt sprzed i za sredniej"""
            left_l2 = []
            right_l2 = []
            for i in range(len(pointLis)):
                if pointLis[i][0] > midle_station:
                    right_l2.append(pointLis[i])
            for i in range(len(pointLis)):
                if pointLis[i][0] < midle_station:
                    left_l2.append(pointLis[i])
            """sortowanie po odleglosci od konca"""
            right_l = sorted(right_l2, key=itemgetter(-2))
            left_l = sorted(left_l2, key=itemgetter(-1))
            "sprawdzenie wystapienia przeciec po obu stronach"
            if len(left_l) < 1 or len(right_l) < 1:
                print("przeciecia po lewej: {}\nprzeciecia po prawej: {}".format(len(left_l), len(right_l)))
            if len(left_l) < 1:
                z =self.geom[0][1]
                stat = self.kor[0][0]
                print(z,stat)
                left_l.insert(0, [stat,z, False, False, 0,0])
            if len(right_l) < 1:
                z = self.geom[-1][1]
                stat = self.kor[-1][0]
                print(z, stat)
                right_l.append([stat, z, False, False, 0,0])
                #time.sleep(5)
            """przypisanie konkretnych punktow R i L"""
            pointR = right_l[0]
            pointL = left_l[0]
        return pointR, pointL

        ### funkcja tworzaca obiekt typu culvert z przekroju geodezyjnego
    def get_culvert(self):
        print(self.lp)
        self.geom = []
        self.deck = []
        self.kor = []
        self.kor_c = []
        '''podzial na pkt koryta i obiektu, pobranie najnizszego punktu z koryta'''
        self.culvert_upS = 1000
        for pkt in self.point_data:
            lista_geo = []
            #if "40" not in str(pkt.kod) and "41" not in str(pkt.kod) and "42" not in str(pkt.kod) and "66" not in str(pkt.kod) and "7d" not in str(pkt.kod) and "50" not in str(pkt.kod) and "51" not in str(pkt.kod):
            if "K" in str(pkt.kod) or "T" in str(pkt.kod) or pkt.kod == None:
                self.kor.append([float(pkt.dist), float(pkt.z)])
                if pkt.z < self.culvert_upS:
                    self.culvert_upS = pkt.z
            if "40" in str(pkt.kod):
                self.geom2.append([float(pkt.dist), float(pkt.z)])
            if "40" in str(pkt.kod) and "None" in str(pkt.cos):
                self.geom.append([float(pkt.dist), float(pkt.z)])
            if "41" in str(pkt.kod):
                self.deck.append([float(pkt.dist), float(pkt.z)])
        '''algorytm do redukcji punktow, zmienia zageszczone zygzaki na prosta'''
        self.geom = rdp(self.geom, epsilon=0.8)
        self.deck = rdp(self.deck, epsilon=5)
        try:
            if self.geom[0][0] < self.geom[-1][0]:
                self.geom.reverse()
        except:
            pass
        pointR, pointL = self.gen_pkt()

        if pointR[-4] == True:
            dyst = pointR[0] - self.geom[0][0]
            new_elem=[]
            for element in self.geom:
                ele = element
                ele[0]=ele[0]+dyst
                new_elem.append(ele)
            self.geom = new_elem
            pointR, pointL = self.gen_pkt()
            print(pointR)
            print(dyst, '----')

        if pointL[-4] == True:
            dyst = pointL[0] - self.geom[-1][0]
            new_elem = []
            for element in self.geom:
                ele = element
                ele[0] = ele[0] + dyst
                new_elem.append(ele)
            self.geom = new_elem
            pointR, pointL = self.gen_pkt()
            print(pointL)
            print(dyst, '----')
        """jesli punkt lewy i prawy sa rowne error"""
        if pointL == pointR:
            print ('kryzys', pointL, pointR)
            print(self.geom)
            print(self.kor)
            print(pointLis)
        """dodanie punktow do geometri"""
        self.geom.insert(-1, [pointL[0], pointL[1]])
        self.geom.insert(0, [pointR[0], pointR[1]])
        """uciecie koryta"""
        lewy = None
        prawy = None
        for i in range(len(self.kor)-1):
            if is_between2(self.kor[i][0], self.kor[i][1], pointL[0], pointL[1], self.kor[i+1][0], self.kor[i+1][1]):
                lewy = i
        for i in range(len(self.kor)-1):
            if is_between2(self.kor[i][0], self.kor[i][1], pointR[0], pointR[1], self.kor[i+1][0], self.kor[i+1][1]):
                prawy = i+1
        if lewy != None and prawy != None:
            self.kor_c = self.kor[lewy+1:prawy]
        elif lewy != None and prawy == None:
            self.kor_c = self.kor[lewy + 1:]
        elif lewy == None and prawy != None:
            self.kor_c = self.kor[:prawy]
        """dodanie pkt tnacych do koryta"""
        self.kor_c.insert(0, [pointL[0], pointL[1]])
        self.kor_c.append([pointR[0], pointR[1]])
        self.culvertXS = self.kor_c+rdp(self.geom, epsilon=0.2)
        print(self.get_culver_len(),"----")
        print("dlugosc obiektu: ",round(self.culvert_len, 2))
        print("upstream z:",self.culvert_upS,"downstream z: ", self.culvert_downS)
        #plt.plot(*zip(*self.kor), color='brown')
        """
        plt.plot(*zip(*self.culvertXS))
        plt.plot(*zip(*self.deck))
        plt.plot(pointL[0], pointL[1], 'ro')
        plt.plot(pointR[0], pointR[1], 'bo')
        plt.show()
        """
    def excel_print(self, workbook):
        worksheet = workbook.add_worksheet(str(self.name))
        bold = workbook.add_format({'bold': 1})
        headings = ['Koryto Stat','Koryto Elev', 'Przepust Stat', 'Przepust Elev', 'Przelew Stat', 'Przelew Elev']
        worksheet.write_row('A10', headings, bold)
        worksheet.write(0, 0, 'Rzeka:')
        worksheet.write(0, 1, str(self.rzeka))
        worksheet.write(1, 0, 'Data pom:')
        worksheet.write(1, 1, str(self.data))
        worksheet.write(2, 0, 'Typ:')
        worksheet.write(2, 1, str(self.type))
        worksheet.write(3, 0, 'Lp:')
        worksheet.write(3, 1, str(self.lp))
        worksheet.write(4, 0, 'Długość:')
        worksheet.write(4, 1, str(self.culvert_len))
        worksheet.write(5, 0, 'Upstream:')
        worksheet.write(5, 1, str(self.culvert_upS))
        worksheet.write(6, 0, 'Downstream:')
        worksheet.write(6, 1, str(self.culvert_downS))
        try:
            worksheet.write(0, 3, 'Foto:')
            worksheet.write(0, 4, str(self.foto))
        except:
            pass
        try:
            worksheet.write(1, 3, 'Admin:')
            worksheet.write(1, 4, str(self.admin))
        except:
            pass
        try:
            worksheet.write(2, 3, 'Uwagi:')
            worksheet.write(2, 4, str(self.uwagi))
        except:
            pass
        try:
            worksheet.write(3, 3, 'Szer:')
            worksheet.write(3, 4, str(self.szer))
        except:
            pass

        chart1 = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
        for row, line in enumerate(self.kor):
            for col, cell in enumerate(line):
                worksheet.write(row+10, col, cell)

        chart1.add_series({
            'name': 'Koryto',
            'categories': [self.name, 10, 0, row+10, 0],
            'values': [self.name, 10, 1, row+10, 1],
        })

        for row, line in enumerate(self.culvertXS):
            for col, cell in enumerate(line):
                worksheet.write(row+10, col+2, cell)

        chart1.add_series({
            'name': 'Przepust',
            'categories': [self.name, 10, 2, row + 10, 2],
            'values': [self.name, 10, 3, row + 10, 3],
        })
        for row, line in enumerate(self.deck):
            for col, cell in enumerate(line):
                worksheet.write(row+10, col+4, cell)
        chart1.add_series({
            'name': 'Przelew',
            'categories': [self.name, 10, 4, row + 10, 4],
            'values': [self.name, 10, 5, row + 10, 5],
        })
        chart1.set_style(10)
        chart1.set_size({'width': 720, 'height': 576})
        worksheet.insert_chart('G1', chart1, {'x_offset': 25, 'y_offset': 15})
        #workbook.close()


############################################################################################
class points2Line(object):
    '''klasa zawierająca w sobie współrzędne dwóch punktów określających prostą, oraz
    jednego punktu który będzie na nią rzutowany'''
    def __init__(self, x1, y1, x2, y2, x=None, y=None):
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        self.x = float(x)
        self.y = float(y)
        #def computePoints(self):
        licznik = ((self.x - self.x1) * (self.x2 - self.x1)) + ((self.y - self.y1) * (self.y2 - self.y1))
        mianownik = ((self.x1 - self.x2) ** 2) + ((self.y1 - self.y2) ** 2)
        u = licznik / mianownik
        self.xp = ((self.x2 - self.x1) * u) + self.x1
        self.yp = ((self.y2 - self.y1) * u) + self.y1
