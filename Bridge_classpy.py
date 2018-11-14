class Bridge(object):
    '''object hold on data for Bridge in Nwk object,
    have reference to'''

    def __init__(self, parent = None):
        self.bridgeParams = {}
        self.end = "EndSect  // bridge_data"
        self.parent = parent

    def add_parameters(self, string_list, name, line):
        '''load parameters...'''

        if name:
            self.bridgeParams[name] = line
        
napis = '''BranchName = 'PTZ_BUD_33053-36358'
            Chainage = 125
            ID = 'BUD_M-109_B1'
            TopoID = 'BUD_S01'
            Type = 8
            ChannelWidth = 0
            SectionArea = 0'''
napis = napis.replace(" ",'')
print(napis.split('\n'))
