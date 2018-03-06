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
        self.max_right = max(elev_points[-6:-1])
    pass

class link(object):
    def __init__(self, object1, object2):
        self.pkt = []
        self.river1 = object1.river_code
        self.chain1 = object1.km
        self.river2 = object2.river_code
        self.chain2 = object2.km
        self.rzad = 0