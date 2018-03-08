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

class XS_t(object):
    def __init__(self, file):
        self.km = 0
        self.rzeka = "Riv"
        self.data = "01.01.1990"
        self.x = []
        self.y = []
        self.z = []
        self.kod = []
        self.dane = file.read().split("\n")