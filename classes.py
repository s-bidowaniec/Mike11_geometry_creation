import math
import operator
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

class point(object):
    def __init__(self, lp, x, y, z, kod="nul", cos="nul"):
        self.lp = lp
        self.x = x
        self.y = y
        self.z = z
        self.kod = kod
        self.cos = [cos]

class XS_t(object):
    def __init__(self, file):
        self.km = 0
        self.rzeka = "Riv"
        self.data = "01.01.1990"
        self.type = "none"
        self.dane = []
        self.point_data = []
        for line in file.read().split("\n"):
            line2 = line.replace("\t\t","").replace("\r","")
            numbers = sum(c.isdigit() for c in line2)
            if numbers < 14:
                self.dane.append(line2)

            else:
                self.point_data.append(point(*line2.split('\t')))

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
        else:
            print("Brak: type def", self.lp)
        if self.type == "none" or self.type == '':
            #print(self.lp)
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
        #self.point_data = sorted(self.point_data, key=operator.attrgetter('dist'))
    def get_culvert(self):
        self.geom = []
        self.kor = []
        self.kor_c = []
        for pkt in self.point_data:
            if "40" not in str(pkt.kod) and "41" not in str(pkt.kod) and "42" not in str(pkt.kod) and "66" not in str(pkt.kod):
                self.kor.append((pkt.dist, pkt.z))
            elif "40" in str(pkt.kod):
                self.geom.append((pkt.dist, pkt.z))
        print(len(self.geom))
        self.max_d = max(self.geom, key=itemgetter(0))[0]
        self.min_d = min(self.geom, key=itemgetter(0))[0]
        print(self.min_d, self.max_d)
        for element in self.kor:
            if float(element[0]) > self.max_d+0.1 or float(element[0]) < self.min_d:
                pass
                #print(element)
            else:
                self.kor_c.append(element)
        self.geom.reverse()
        wykres = self.kor+self.geom
        plt.plot(*zip(*wykres))
        plt.show()

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
