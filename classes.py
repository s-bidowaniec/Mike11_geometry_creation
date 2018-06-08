import math, collections
from operator import itemgetter

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

    deltaX = (x1-x2)/4
    deltaY = (y1-y2)/4


    return x1+deltaY, y1-deltaX, x2+deltaY, y2-deltaX

class Pkt(object):
    def __init__(self, line="0, 0, 0, <#0>"):
        if line is str and len(line.split()) != 7:
            print(len(line.split()))
            print(line,'\n','-----------')
        #self.station, self.z, self.manning.py, self.kod = zip(*line.split()[:-3])
        self.station, self.z, self.manning, self.kod = line.split()[0], line.split()[1],line.split()[2],line.split()[3]
        #return '{} {}'.format(self.station, self.z)

class Xs(object):
    def __init__(self):
        self.dane = []
        self.points=[]
        self.cs = 0
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
        self.max_left = max(elev_points[0:5])
        self.min_left = min(elev_points[0:10])
        self.mean_left = float(self.max_left) / 5
        self.max_right = max(elev_points[-5:-1])
        self.min_right = min(elev_points[-10:-1])
        self.mean_right = float(self.max_right) / 5
    def rdp_pkt(self, epsilon):
        self.pointsRdp=[]
        set = [[float(i.station), float(i.z)] for i in self.points]
        set2 = rdp(set, epsilon=epsilon)
        set3 = [i[0] for i in set2]
        print('Redukcja RDP o {} punktów z {}, river: {} km: {}.'.format(len(set)-len(set2), len(set), self.riverCode, self.km))
        manningOld = 0
        for pkt in self.points:
            if str(float(pkt.station)) in str(set3):
                self.pointsRdp.append(pkt)
            elif pkt.manning != manningOld or pkt.kod != '<#0>':
                self.pointsRdp.append(pkt)
                print('Zachowano punkt zmiany manninga z {} na {} w station: {}.'.format(manningOld, pkt.manning, pkt.station))
            manningOld = pkt.manning
        if len(self.pointsRdp)>3:
            self.points = self.pointsRdp
    def print_txt(self, file, zaok, rr):
        #print(self.km)
        file.write('{}\r\n'.format(self.reachCode))
        file.write('{}\r\n'.format(self.riverCode))
        file.write('               {}\r\n'.format(round(float(self.km), zaok)))
        file.write('COORDINATES\r\n')
        file.write('{}'.format(self.cords))
        file.write('FLOW DIRECTION\r\n{}'.format(self.fd))
        file.write('PROTECT DATA\r\n{}'.format(self.pd))
        file.write('DATUM\r\n{}'.format(self.datum))
        try:
            if self.cs == 1:
                file.write('CLOSED SECTION\r\n    {}\r\n'.format(self.cs))
            else:
                pass
        except:
            pass
        file.write('RADIUS TYPE\r\n{}'.format(self.rt))
        file.write('DIVIDE X-Section\r\n{}'.format(self.dx))
        file.write('SECTION ID\r\n    {}'.format(self.id))
        file.write('INTERPOLATED\r\n{}'.format(self.inter))
        file.write('ANGLE\r\n{}'.format(self.angle))
        try:
            rr = self.rr
        except:
            pass
        if rr == None:
            file.write('RESISTANCE NUMBERS\r\n   2  1     1.000     1.000     1.000    1.000    1.000\r\n')
        else:
            file.write('RESISTANCE NUMBERS\r\n   2  0     1.000     1.000     1.000    1.000    1.000\r\n')
        file.write('PROFILE        {}\r\n'.format(self.profile))
        for pkt in self.points:
            if rr == None:
                file.write('  {}   {}   {}     {}     0     0.000     0\r\n'.format(pkt.station, pkt.z, pkt.manning, pkt.kod))
            elif rr != None:
                file.write(
                    '  {}   {}   {}     {}     0     0.000     0\r\n'.format(pkt.station, pkt.z, float(pkt.manning)/rr, pkt.kod))
        file.write('LEVEL PARAMS\r\n{}'.format(self.lp))
        file.write('*******************************\r\n')
class Link(object):
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
            self.definitions = [
                "KP_" + str(self.rzad) + "_" + str(self.main_chan) + "_" + str(self.main_km) + "_" + self.main_site,
                self.topo, 0, 5, 0, 10000, 1]
            h_elev = float(max(self.object1.max_left, self.object2.max_right))
            h2_elev = float(self.object2.min_right)
            self.geometry = [h_elev, h2_elev]
            self.cross_section = [[0, 0], [0.1, float(self.object1.len)], [3, float(self.object1.len)]]
            self.points = [float(self.object1.left[0]) + x1, float(self.object1.left[1]) + y1,
                           float(self.object1.left[0]) + x2, float(self.object1.left[1]) + y2]


def printowanie(list_lin, num):
    point_list = []
    f = open('branche.txt', 'w')
    f.write("   [POINTS]\n")
    for element in list_lin:
        point1 = str(element.points[0:2])
        elem = [num + 1, point1]
        point_list.append(elem)
        f.write("      point = " + str(elem).replace("[", "").replace("]", "").replace("'", "") + ", 1, 0.00, 0" + "\n")
        point2 = str(element.points[2:4])
        elem2 = [num + 2, point2]
        point_list.append(elem2)
        f.write(
            "      point = " + str(elem2).replace("[", "").replace("]", "").replace("'", "") + ", 1, 5.00, 0" + "\n")
        num += 2
        element.points2 = [num - 1, num]
    f.write("-------------\n\n")
    for element in list_lin:
        f.write("      [branch]\n")
        f.write("         definitions = " + str(element.definitions).replace("[", "").replace("]", "") + "\n")
        f.write("         connections = " + str(element.connections).replace("[", "").replace("]", "") + "\n")
        f.write("         points = " + str(element.points2).replace("[", "").replace("]", "") + "\n")
        f.write("         [linkchannel]\n")
        f.write("            Geometry = " + str(element.geometry).replace("[", "").replace("]", "") + ", 0\n")
        f.write("            HeadLossFactors = 0.5, 1, 0, 1, 0.5, 1, 0, 1\n")
        f.write("            Bed_Resistance = 1, 0.03\n")
        f.write("            [Cross_Section]\n")
        for data in element.cross_section:
            f.write("               Data = " + str(data).replace("[", "").replace("]", "") + "\n")
        f.write("            EndSect  // Cross_Section\n\n")
        f.write("         EndSect  // linkchannel\n\n")
        f.write("      EndSect  // branch\n\n")
    return point_list


# bridges----------------------------------------------------------------------------------------------------------------

def distance(x1, x2, y1, y2):
    try:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    except:
        return 0


def is_between(x1, y1, x, y, x2, y2):
    return round(distance(x1, x, y1, y)) + round(distance(x, x2, y, y2)) == round(distance(x1, x2, y1, y2))


def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    line1 = [[x1, y1], [x2, y2]]
    line2 = [[x3, y3], [x4, y4]]
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
        b = (is_between(x3, y3, x, y, x4, y4))
        c = (is_between(x1, y1, x, y, x2, y2))

    return x, y, b, c


class Point(object):
    def __init__(self, lp, x, y, z, kod="nul", cos="nul"):
        self.lp = int(lp)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.kod = str(kod)
        self.cos = [cos]


class XSt(object):
    def __init__(self, file):
        print(file)
        self.km = 0
        self.rzeka = "Riv"
        self.data = "01.01.1990"
        self.type = "none"
        self.dane = []
        self.point_data = []
        for line in file.read().split("\n"):
            line2 = line.replace("\t\t", "").replace("\r", "")
            numbers = sum(c.isdigit() for c in line2)
            if numbers < 14:
                self.dane.append(line2)

            else:

                self.point_data.append(Point(*line2.split('\t')[:6]))

                try:
                    #print(line2.split('\t')[0])
                    int(float(line2.split('\t')[0]))
                    self.point_data.append(Point(*line2.split('\t')[:]))
                except:
                    pass
                    #self.point_data.append(Point(*line2.split('\t')[1:]))

        r = 0
        while sum(c.islower() for c in self.dane[r]) < 1:
            r += 1
        if "rzek" in str.lower(self.dane[r]) or "zeka" in str.lower(self.dane[0]):
            self.rzeka = self.dane[r].split(':')[1]
        else:
            print("Brak: river def", self.lp)
        if "przek" in str.lower(self.dane[r + 1]) or "rzekr" in str.lower(self.dane[1]):
            self.lp = self.dane[r + 1].split(':')[1]
        else:
            print("Brak: lp def", self.lp)
        if "dat" in str.lower(self.dane[r + 2]) or "ata" in str.lower(self.dane[2]):
            self.data = self.dane[r + 2].split(':')[1]
        else:
            print("Brak: data def", self.lp)
        if "typ" in str.lower(self.dane[r + 4]) or "obiekt" in str.lower(self.dane[4]):
            self.type = self.dane[r + 4].split(':')[1]
        else:
            print("Brak: type def", self.lp)
        if self.type == "none" or self.type == '':
            # print(self.lp)
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
            if "ZWW" in str(poi.cos):
                line.append(poi.x)
                line.append(poi.y)
        return line[0], line[1], line[2], line[3]

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
            dist = math.sqrt((dx ** 2) + (dy ** 2))
            i.dist = dist

    def dist_sort(self):
        self.point_data = sorted(self.point_data, key=operator.attrgetter('dist'))

    def count_40(self):
        for pkt in self.point_data:
            licz == 0
            if "40" in str(pkt.kod):
                licz += 1
        self.licz40 = licz

    def get_culvert(self):
        self.geom = []
        self.kor = []
        self.kor_c = []
        for pkt in self.point_data:
            if "40" not in str(pkt.kod) and "41" not in str(pkt.kod) and "42" not in str(pkt.kod) and "66" not in str(
                    pkt.kod):
                self.kor.append((float(pkt.dist), float(pkt.z)))
            elif "40" in str(pkt.kod):
                self.geom.append((float(pkt.dist), float(pkt.z)))
        print(len(self.geom))
        self.max_d = max(self.geom, key=itemgetter(0))[0]
        self.min_d = min(self.geom, key=itemgetter(0))[0]
        print(self.min_d, self.max_d)
        for element in self.kor:
            if float(element[0]) > self.max_d + 0.1 or float(element[0]) < self.min_d:
                pass
                # print(element)
            else:
                self.kor_c.append(element)
        self.geom.reverse()
        plt.plot(*zip(*self.kor))
        plt.plot(*zip(*self.geom))
        plt.show()


class Points2Line(object):
    """klasa zawierająca w sobie współrzędne dwóch punktów określających prostą, oraz
    jednego punktu który będzie na nią rzutowany"""

    def __init__(self, x1, y1, x2, y2, x=None, y=None):
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        self.x = float(x)
        self.y = float(y)

        # def computePoints(self):
        licznik = ((self.x - self.x1) * (self.x2 - self.x1)) + ((self.y - self.y1) * (self.y2 - self.y1))
        mianownik = ((self.x1 - self.x2) ** 2) + ((self.y1 - self.y2) ** 2)
        try:
            u = licznik / mianownik
        except:
            u = 0
        self.xp = ((self.x2 - self.x1) * u) + self.x1
        self.yp = ((self.y2 - self.y1) * u) + self.y1
