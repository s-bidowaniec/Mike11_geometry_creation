import openpyxl, time
import dbm
import pickle
import copy

from functions import *
# --------------------------------- PARAMETRY -----------------------------------------------------------------
# spadek minimalny:
spadMin = 0
# -------------------------------- PLIKI WSADOWE --------------------------------------------------------------
# plik wsadowy rawdata, pobierane sa punkty wspolne na przekrojach oraz inne dane do generacji linku
xsInputDir = r"C:\!!Mode ISOKII\!ISOK II\Dobka\hec_ras2\Dobka_man.txt"
fileWejscieXS = open(xsInputDir,'r')
bazaXsRawData, XsOrder = read_XSraw(fileWejscieXS)
# plik wsadowy nwk, pobierana jest lista punktow oraz branchy do ktorych dopisywane sa dane z nowych linkow
nwkInputDir = r"C:\!!Mode ISOKII\!ISOK II\Dobka\hec_ras2\Dobka.nwk11"
fileWejscieNWK = open(nwkInputDir, 'r')
nwk = read_NWK(fileWejscieNWK)
# plik z mostami
wb = openpyxl.load_workbook(r'C:\!!Mode ISOKII\!ISOK II\Dobka\hec_ras2\Dobka_progi3.xlsx')
bridges = read_bridge_xlsx(wb)
base_manning = 0.04
# --------------------------------- PLIKI WYNIKOWE -----------------------------------------------------------
# nowy plik NWK z naniesionymi mostasmi
nwkOutDir = r"C:\!!Mode ISOKII\!ISOK II\Dobka\hec_ras2\otput\S01_Dobka_bridge_v3.nwk11"
if nwkOutDir == nwkInputDir:
    raise ValueError('NWK input file equals NWK output file', 'foo', 'bar', 'baz')
fileWynikNWK = open(nwkOutDir, "w")
# nowy plik XSrawData z naniesionymi mostasmi
xsOutputDir = r"C:\!!Mode ISOKII\!ISOK II\Dobka\hec_ras2\otput\rawdata_z_m_v3.txt"
if xsInputDir == xsOutputDir:
    raise ValueError('XS input file equals XS output file', 'foo', 'bar', 'baz')
fileWynikXS = open(xsOutputDir,'w')
"""
base = open('Test\\test_XsRawData.pkl', 'wb')
pickle.dump(bazaXsRawData, base, protocol=None, fix_imports=True)
base.close()
"""
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# zaczytanie obiektow z xlsx, nwk i txt raw data
# mosty z xlsx

for bridge in bridges:
    print("----!!!----",bridge.typ,"----!!!----")
    flag = "non"
    if bridge.typ == "most" or bridge.typ == "przepust" or bridge.typ == "kładka":
        flag = "bridge"
        # ---- CULVERT -----
        # --- conflict detection ---
        set = [[str.lower(i.riverName).replace(' ', ''), round(float(i.km))] for i in nwk.culvertList]
        dodawany = [str.lower(bridge.rzeka).replace(' ', ''), round(float(bridge.km))]
        if dodawany in set:
            print("Zastapiono culvert; {} {}".format(str.lower(bridge.rzeka), round(float(bridge.km))))
            del nwk.culvertList[set.index(dodawany)]
        # --- end of conflict detection ---
        # GENERACJA PUSTEGO CULVERTU
        nwk.culvertList.append(Culvert())
        cl = nwk.culvertList[-1]
        cl.geometry = Geometry(cl)
        cl = cl.geometry
        cl.levelWidth = LevelWidth(cl)
        cl.irregular = Irregular(cl)
        cl = nwk.culvertList[-1]
        cl.reservoir = ReservoirData(cl)
        cl = cl.reservoir
        cl.elevation = Elevation(cl)
        # PRZYPISANIE DANYCH PODSTAWOWYCH
        culvertID = str.upper(bridge.rzeka[0:3]) + "_M-" + str(bridge.lp).replace(' ', '') + "_C1"
        nwk.culvertList[-1].riverName = bridge.rzeka
        nwk.culvertList[-1].km = bridge.km
        nwk.culvertList[-1].ID = culvertID
        nwk.culvertList[-1].topoID = bridge.topoID
        # uwzglednienie spadku
        downS, upS, length = float(bridge.downS), float(bridge.upS), float(bridge.dl)
        spad = (upS-downS)/length
        if spad < spadMin:
            delta = ((spadMin - spad)*length)/2
            bridge.downS = round((downS - delta), 2)
            bridge.upS = round((upS + delta), 2)

        # zamiana upstream na downstream
        attributes = [bridge.downS, bridge.upS, round(float(bridge.dl), 2), bridge.mann, 1, 0, 0]
        nwk.culvertList[-1].culvertParams['Attributes'] = attributes
        nwk.culvertList[-1].culvertParams['HorizOffset'] = [0]
        nwk.culvertList[-1].culvertParams['HeadLossFactors'] = [0.1, 0.3, 1, 0, 0.1, 0.3, 1, 0]
        bridgeID = str.upper(bridge.rzeka[0:3])+"_M-"+str(bridge.lp).replace(' ','')+"_C1"
        location = [str(bridge.rzeka).replace(' ',''), str(bridge.km).replace(' ',''), bridgeID, str(bridge.topoID).replace(' ','')]
        nwk.culvertList[-1].culvertParams['Location'] = location
        # GEOMETRY
        nwk.culvertList[-1].geometry.data['Type'] = [4]
        nwk.culvertList[-1].geometry.data['Rectangular'] = [0, 0]
        nwk.culvertList[-1].geometry.data['Cicular_Diameter'] = [0]
        nwk.culvertList[-1].geometry.irregular.data = [['-1e-155, -1e-155']]
        # RESERVOIR DATA
        nwk.culvertList[-1].reservoir.data['StructureType'] = [0]
        nwk.culvertList[-1].reservoir.data['StorageType'] = [0]
        nwk.culvertList[-1].reservoir.data['ApplyXY'] = [0]
        nwk.culvertList[-1].reservoir.data['CoordXY'] = [0]
        nwk.culvertList[-1].reservoir.data['InitialArea'] = [0]
        # ---- END CULVERT -----

        # ---- XS -----
        # --- Detect XS conflict ---

        set = [[str.lower(i.riverCode), round(float(i.km))] for i in bazaXsRawData]
        """
        dodawany = [str.lower(bridge.rzeka).replace(' ', ''), round(float(bridge.km))]
        if dodawany in set:
            print("Zastapiono przekroj; {} {}".format(str.lower(bridge.rzeka), round(float(bridge.km))))
            del bazaXsRawData[set.index(dodawany)]
        """
        # --- End XS conflict detection ---

        # --- DOPASOWANIE PRZEKROI -----------------------------------------------------------------------------------
        # -- Wybranie xs sasiednich --
        setKm = [float(i[1]) for i in set if i[0] == str.lower(bridge.rzeka).replace(' ', '')]
        setKm.sort()
        newSet = []
        for km in setKm:
            if abs(float(bridge.km) - float(km)) > 3:
                newSet.append(km)
            else:
                if int(km) == 1047:
                    import pdb
                    pdb.set_trace()
                km2 = km
                pass
        if km2:
            bridge.km = km2
            km2 = 0
        nwk.culvertList[-1].km = bridge.km
        kmDown = max([i for i in newSet if i < bridge.km])
        kmUp = min([i for i in newSet if i > bridge.km])


        xsUp = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)]
        xsDown = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmDown)]
        print(xsUp.points[0].station,"stat1")
        print(xsUp.km, 'km')
        # -- xs dobrane --
        # spasowanie przekroi
        xsUp2, xsDown2 = fit_xs(xsUp, xsDown)
        print(xsUp2.points[0].station, "stat2")
        print(xsUp2.points[0].z, "z2")


        xsDown, xsUp, bridgeShift, downMarker, upMarker = fit_bridge(xsDown2, xsUp2, bridge, base_manning=base_manning)
        print(xsUp.points[0].station, "stat3")
        print(xsUp.points[0].z, "z3")
        add_markers(xsDown, downMarker)
        add_markers(xsUp, upMarker)
        # wbicie koryta na xs
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)] = copy.deepcopy(xsUp)
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmDown)] = copy.deepcopy(xsDown)
        # shift bridge
        nwk.culvertList[-1].culvertParams['HorizOffset'] = [0]
        # --- Przekroje dopasowane ---
        #XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)] = xsUp
        #bazaXsRawData.append(Xs())
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)] = copy.deepcopy(Xs())
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].riverCode = bridge.rzeka
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].reachCode = str(bridge.topoID)+"_CULVERT"
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].km = bridge.km
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].mann = bridge.mann
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].cords = '    0  00.00  00.00 00.00  00.00\n'
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].fd = '    0\n'  # flow direction
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].pd = '    0\n'  # protect data
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].datum = '    0\n'  # datum
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].cs = 1  # closed
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].rt = '    0\n'  # radius type
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].dx = '    0\n'  # divide xs
        xsID = str.upper(bridge.rzeka[0:3]) + "_M-" + str(bridge.lp).replace(' ', '') + "_C1\n"
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].id = xsID  # section id
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].inter = '    0\n'  # interpolated
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].angle = '    0.00   0\n'  # angle
        #bazaXsRawData[-1].rn = '   0  0     1.000     1.000     1.000    1.000    1.000'  # resistance number
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].rr = None
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].profile = str(len(bridge.przepust))  # profile
        for pkt in bridge.przepust:
            XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].points.append(Pkt('    {}   {}     {}     <#0>     0     0.000     0'.format(pkt[0]+bridgeShift,pkt[1], bridge.mann)))
        XsOrder['{}b {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].lp = '   1  0    0.000  0    0.000  250\n'  # level params

        # ---- END XS -----
        """
        # ---- WEIR -----
        # --- conflict detection ---
        set = [[str.lower(i.riverName).replace(' ', ''), round(float(i.km))] for i in nwk.weirList]

        dodawany = [str.lower(bridge.rzeka).replace(' ', ''), round(float(bridge.km))]
        if dodawany in set:
            print("Zastapiono weir; {} {}".format(str.lower(bridge.rzeka), round(float(bridge.km))))
            del nwk.weirList[set.index(dodawany)]

        # --- end of conflict detection ---
        # GENERACJA PUSTEGO WEIR
        nwk.weirList.append(Weir())
        cl = nwk.weirList[-1]
        cl.geometry = Geometry(cl)
        cl = cl.geometry
        cl.levelWidth = LevelWidth(cl)
        cl = nwk.weirList[-1]
        cl.reservoir = ReservoirData(cl)
        cl = cl.reservoir
        cl.elevation = Elevation(cl)
        # PRZYPISANIE DANYCH PODSTAWOWYCH
        weirID = str.upper(bridge.rzeka[0:3]) + "_M-" + str(bridge.lp).replace(' ', '') + "_W1"
        location = [str(bridge.rzeka).replace(' ', ''), str(bridge.km).replace(' ', ''), weirID,
                    str(bridge.topoID).replace(' ', '')]

        nwk.weirList[-1].riverName = bridge.rzeka
        nwk.weirList[-1].km = bridge.km
        nwk.weirList[-1].ID = weirID
        nwk.weirList[-1].topoID = weirID
        print(bridge.km)
        print(bridge.rzeka)
        # PARAMS
        attributes = [0, 0]
        nwk.weirList[-1].weirParams['HorizOffset'] = '0'
        nwk.weirList[-1].weirParams['Attributes'] = attributes

        # nwk.weirList[-1].weirParams['Location'] = location
        nwk.weirList[-1].weirParams['HeadLossFactors'] = [0.0, 0, 1, 0.0, 0, 1]  # ?
        nwk.weirList[-1].weirParams['WeirFormulaParam'] = [1, 1, 1.838, 1.5, 1]  # ?
        nwk.weirList[-1].weirParams['WeirFormula2Param'] = [0, 0, 0]  # ?
        nwk.weirList[-1].weirParams['WeirFormula3Param'] = [0, 0, 0, 0.6, 1.02, 1.37, 1, 0.03, 1.018, 1, 0, 2.6, 1,
                                                            0.7]  # ?
        # RESERVOIR DATA
        nwk.weirList[-1].reservoir.data['StructureType'] = [0]
        nwk.weirList[-1].reservoir.data['StorageType'] = [0]
        nwk.weirList[-1].reservoir.data['ApplyXY'] = [0]
        nwk.weirList[-1].reservoir.data['CoordXY'] = [0]
        nwk.weirList[-1].reservoir.data['InitialArea'] = [0]
        # GEOMETRY
        nwk.weirList[-1].geometry.data['Attributes'] = [0, 0]
        # WYMIAR PRZELEWU
        szerWys = max(i[0] for i in bridge.koryto)  # maxymalny station w korytku
        szerNis = max(i[0] for i in bridge.przepust) - min(i[0] for i in bridge.przepust)  # roznica stationow w przepuscie
        startElev = min(i[1] for i in bridge.przelew)  # najnizsza rzedna gory konstrukcji
        nwk.weirList[-1].geometry.levelWidth.data = [[startElev, szerNis], [startElev + 0.1, szerWys],
                                                     [startElev + 2, bridge.weir_width]]
        """
        # ---- END WEIR -----
        print(len(XsOrder), "len od XsOrder")
    if bridge.typ == "próg" or bridge.typ == "most" or bridge.typ == "przepust" or bridge.typ == "kładka":
        if flag == "bridge":
            weirShift = bridgeShift
            for element in bridge.przelew:
                element[0] += weirShift
            litera ="M"
        else:
            litera = "H"
            weirShift = 0
        import pdb
        #pdb.set_trace()
        # ---- WEIR -----
        # --- conflict detection ---
        set = [[str.lower(i.riverName).replace(' ', ''), round(float(i.km))] for i in nwk.weirList]
        """
        dodawany = [str.lower(bridge.rzeka).replace(' ', ''), round(float(bridge.km))]
        if dodawany in set:
            print("Zastapiono weir; {} {}".format(str.lower(bridge.rzeka), round(float(bridge.km))))
            del nwk.weirList[set.index(dodawany)]
        """
        # --- end of conflict detection ---
        # GENERACJA PUSTEGO WEIR
        nwk.weirList.append(Weir())
        cl = nwk.weirList[-1]
        cl.geometry = Geometry(cl)
        cl = cl.geometry
        cl.levelWidth = LevelWidth(cl)
        cl = nwk.weirList[-1]
        cl.reservoir = ReservoirData(cl)
        cl = cl.reservoir
        cl.elevation = Elevation(cl)
        # PRZYPISANIE DANYCH PODSTAWOWYCH
        weirID = str.upper(bridge.rzeka[0:3]) + "_"+litera+"-" + str(bridge.lp).replace(' ', '') + "_W1"
        location = [str(bridge.rzeka).replace(' ', ''), str(bridge.km).replace(' ', ''), weirID,
                    str(bridge.topoID).replace(' ', '')]

        nwk.weirList[-1].riverName = bridge.rzeka
        nwk.weirList[-1].km = bridge.km
        nwk.weirList[-1].ID = weirID
        nwk.weirList[-1].topoID = weirID
        print(bridge.km)
        print(bridge.rzeka)
        # PARAMS
        attributes = [0, 0]
        nwk.weirList[-1].weirParams['HorizOffset'] = '0'
        nwk.weirList[-1].weirParams['Attributes'] = attributes

        # nwk.weirList[-1].weirParams['Location'] = location
        nwk.weirList[-1].weirParams['HeadLossFactors'] = [0.0, 0, 1, 0.0, 0, 1]  # ?
        nwk.weirList[-1].weirParams['WeirFormulaParam'] = [1, 1, 1.838, 1.5, 1]  # ?
        nwk.weirList[-1].weirParams['WeirFormula2Param'] = [0, 0, 0]  # ?
        nwk.weirList[-1].weirParams['WeirFormula3Param'] = [0, 0, 0, 0.6, 1.02, 1.37, 1, 0.03, 1.018, 1, 0, 2.6, 1,
                                                            0.7]  # ?
        # RESERVOIR DATA
        nwk.weirList[-1].reservoir.data['StructureType'] = [0]
        nwk.weirList[-1].reservoir.data['StorageType'] = [0]
        nwk.weirList[-1].reservoir.data['ApplyXY'] = [0]
        nwk.weirList[-1].reservoir.data['CoordXY'] = [0]
        nwk.weirList[-1].reservoir.data['InitialArea'] = [0]
        # GEOMETRY
        nwk.weirList[-1].geometry.data['Attributes'] = [0, 0]
        # WYMIAR PRZELEWU
        szerWys = 10   # maxymalny station w korytku
        szerNis = 5  # roznica stationow w przepuscie
        startElev = min(i[1] for i in bridge.przelew)  # najnizsza rzedna gory konstrukcji
        nwk.weirList[-1].geometry.levelWidth.data = [[startElev, szerNis], [startElev + 0.1, szerWys],
                                                     [startElev + 2, 120]]
        # ---- END WEIR -----
        # robocze start ------------------------------------------------------------------------------------------------------------------------------------------------
        # --- DOPASOWANIE PRZEKROI -----------------------------------------------------------------------------------
        # -- Wybranie xs sasiednich --

        set = [[str.lower(i.riverCode), round(float(i.km))] for i in bazaXsRawData]
        setKm = [float(i[1]) for i in set if i[0] == str.lower(bridge.rzeka).replace(' ', '')]
        setKm.sort()
        newSet = []
        for km in setKm:
            if abs(float(bridge.km) - float(km)) > 3:
                newSet.append(km)
            else:
                if int(km) == 1047:
                    import pdb
                    pdb.set_trace()
                km2 = km
                pass
        if km2:
            bridge.km = km2
            km2=0
        nwk.weirList[-1].km = bridge.km
        if flag != "bridge":
            kmDown = max([i for i in newSet if i < bridge.km])
            kmUp = min([i for i in newSet if i > bridge.km])

            xsUp = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)]
            xsDown = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmDown)]
            print(xsUp.points[0].station, "stat1")
            print(xsUp.km, 'km')
            # -- xs dobrane --
            # spasowanie przekroi
            xsUp2, xsDown2 = fit_xs(xsUp, xsDown)
            XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)] = copy.deepcopy(xsUp2)
            XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmDown)] = copy.deepcopy(xsDown2)

            weirKmOnXS = min(setKm, key=lambda x: abs(x - bridge.km))
            xsWeir = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), weirKmOnXS)]

            xsUp2, xsWeir = fit_xs(xsUp, xsWeir)

        elif flag == "bridge":
            kmUp = min([i for i in newSet if i > bridge.km])
            xsUp = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)]
            weirKmOnXS = min(setKm, key=lambda x: abs(x - bridge.km))
            xsWeir = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), weirKmOnXS)]
            xsUp2, xsWeir = fit_xs(xsUp, xsWeir)


            #weirKmOnXS = min(setKm, key=lambda x: abs(x-bridge.km))
            #xsWeir = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), weirKmOnXS)]
            #print(xsWeir)

            weir = copy.deepcopy(bridge)
            xsBridge, upMarker = fit_weir(xsWeir, weir, base_manning=0.04, bridgeType = True)
            add_markers(xsBridge, upMarker)
            #import pdb
            #pdb.set_trace()
            import copy
            XsOrder['{}B {}'.format(str.lower(bridge.rzeka).replace(' ', ''), weirKmOnXS)] = copy.deepcopy(xsBridge)
            XsOrder['{}B {}'.format(str.lower(bridge.rzeka).replace(' ', ''), weirKmOnXS)].reachCode = str(
                bridge.topoID) + "_bridge"

        weir = copy.deepcopy(bridge)
        weir.koryto = weir.przelew
        xsWeir, upMarker = fit_weir(xsWeir, weir, base_manning=0.04)
        add_markers(xsWeir, upMarker)
        XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), weirKmOnXS)] = xsWeir
        """
        print(xsUp2.points[0].station, "stat2")
        print(xsUp2.points[0].z, "z2")

        xsDown, xsUp, bridgeShift = fit_bridge(xsDown2, xsUp2, bridge, base_manning=base_manning)
        print(xsUp.points[0].station, "stat3")
        print(xsUp.points[0].z, "z3")
        """
        # wbicie koryta na xs
        XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)] = xsUp
        XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmDown)] = xsDown
        # robocze end ------------------------------------------------------------------------------------------------------------------------------------------------
        # ------  XS  ------
        # bazaXsRawData.append(Xs())
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)] = copy.deepcopy(Xs())
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].riverCode = bridge.rzeka
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].reachCode = str(bridge.topoID)+"_weir"
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].km = bridge.km
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].mann = bridge.mann
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''),
                               bridge.km)].cords = '    0  00.00  00.00 00.00  00.00\n'
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].fd = '    0\n'  # flow direction
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].pd = '    0\n'  # protect data
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].datum = '    0\n'  # datum
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].cs = 0  # closed
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].rt = '    0\n'  # radius type
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].dx = '    0\n'  # divide xs
        xsID = str.upper(bridge.rzeka[0:3]) + "_M-" + str(bridge.lp).replace(' ', '') + "_C1\n"
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].id = xsID  # section id
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].inter = '    0\n'  # interpolated
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].angle = '    0.00   0\n'  # angle
        # bazaXsRawData[-1].rn = '   0  0     1.000     1.000     1.000    1.000    1.000'  # resistance number
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].rr = None
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].profile = str(
            len(bridge.przelew))  # profile
        for pkt in bridge.przelew:
            XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].points.append(Pkt(
                '    {}   {}     {}     <#0>     0     0.000     0'.format(pkt[0], pkt[1], bridge.mann)))
        XsOrder['{}w {}'.format(str.lower(bridge.rzeka).replace(' ', ''),
                               bridge.km)].lp = '   1  0    0.000  0    0.000  250\n'  # level params
        # ---- END XS ----

nwk.print_to_nwk(fileWynikNWK)
fileWynikNWK.close()
for element in list(XsOrder.values()):
    element.print_txt(fileWynikXS, None, 1)
