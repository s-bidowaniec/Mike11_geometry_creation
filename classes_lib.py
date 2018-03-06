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
        self.max_left = max(elev_points[0:5])
        self.mean_left = float(self.max_left) / 5
        self.max_right = max(elev_points[-6:-1])
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
        if self.rzad == 0:
            print("brak przypisania")
            print(self.river1, self.chain1, self.river2, self.chain2)
        else:
            if self.kolej == 1:
                self.definitions = ["KP_"+str(self.main_chan)+"_"+str(self.main_km)+"_"+self.main_site, self.topo,0,5,0,10000,1]
                self.connections = [self.object1.river_code, self.object1.km, self.object2.river_code, self.object2.km]
                self.points = [float(self.object1.left[0])-2, float(self.object1.left[1])-2, float(self.object1.left[0])+2, float(self.object1.left[1])+2]
                h_elev = float(max(self.object1.max_left, self.object2.max_right))
                self.geometry = [h_elev, h_elev-1]
                self.cross_section = [[0,0],[0.1, float(self.object1.len)], [3, float(self.object1.len)]]
            elif self.kolej == 2:
                self.definitions = ["KP_"+str(self.main_chan)+"_"+str(self.main_km)+"_"+self.main_site, self.topo,0,5,0,10000,1]
                self.connections = [self.object2.river_code, self.object2.km, self.object1.river_code, self.object1.km]
                self.points = [float(self.object1.left[0])-2, float(self.object1.left[1])-2, float(self.object1.left[0])+2, float(self.object1.left[1])+2]
                h_elev = float(max(self.object1.max_left, self.object2.max_right))
                self.geometry = [h_elev, h_elev-1]
                self.cross_section = [[0,0],[0.1, float(self.object1.len)], [3, float(self.object1.len)]]
            pass