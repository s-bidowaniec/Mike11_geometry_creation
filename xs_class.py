class XS(object):
    def __init__(self):
        self.dane = []
    def kordy(self):
        self.Left = self.cords.split()[1:3]
        self.Right = self.cords.split()[3:5]
        elev_points = []
        #print(len(self.dane))
        for element in self.dane:
            try:
                h = element.split()[1]
                elev_points.append(h)
            except:
                print(element)
        self.MaxLeft = max(elev_points[0:5])
        self.MaxRight = max(elev_points[-6:-1])
    pass