import openpyxl, time
import dbm
import pickle


from functions import *
# --------------------------------- PARAMETRY -----------------------------------------------------------------
# spadek minimalny:
spadMin = 0
# -------------------------------- PLIKI WSADOWE --------------------------------------------------------------
# plik wsadowy rawdata, pobierane sa punkty wspolne na przekrojach oraz inne dane do generacji linku
xsInputDir = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\Budkowiczanka_Qn22.06.txt"
fileWejscieXS = open(xsInputDir,'r')
bazaXsRawData, XsOrder = read_XSraw(fileWejscieXS)
# plik wsadowy nwk, pobierana jest lista punktow oraz branchy do ktorych dopisywane sa dane z nowych linkow
nwkInputDir = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\v3_25.06\BUDKOWICZANKA_S01_Qn_bridge_clipped.nwk11"
fileWejscieNWK = open(nwkInputDir, 'r')
nwk = read_NWK(fileWejscieNWK)
# plik z mostami
wb = openpyxl.load_workbook(r'C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\Wstawianie mostów\Kopia pliku Budkowiczanka_mosty2.xlsx')
bridges = read_bridge_xlsx(wb)
base_manning = 0.04
# --------------------------------- PLIKI WYNIKOWE -----------------------------------------------------------
# nowy plik NWK z naniesionymi mostasmi
nwkOutDir = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\v3_25.06\BUDKOWICZANKA_S01_Qn_bridgeV3.nwk11"
if nwkOutDir == nwkInputDir:
    raise ValueError('NWK input file equals NWK output file', 'foo', 'bar', 'baz')
fileWynikNWK = open(nwkOutDir, "w")
# nowy plik XSrawData z naniesionymi mostasmi
xsOutputDir = r"C:\!!Modele ISOKII\!Etap1\BUDKOWICZANKA_V1\v3_25.06\Budkowiczanka_Qn_bridgeV3.txt"
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
    nwk.culvertList[-1].riverName = bridge.rzeka
    nwk.culvertList[-1].km = bridge.km
    nwk.culvertList[-1].ID = bridge.lp
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
    nwk.culvertList[-1].culvertParams['HeadLossFactors'] = [0.0, 0, 1, 0, 0.0, 0, 1, 0]
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
    dodawany = [str.lower(bridge.rzeka).replace(' ', ''), round(float(bridge.km))]
    if dodawany in set:
        print("Zastapiono przekroj; {} {}".format(str.lower(bridge.rzeka), round(float(bridge.km))))
        del bazaXsRawData[set.index(dodawany)]
    # --- End XS conflict detection ---

    # --- DOPASOWANIE PRZEKROI -----------------------------------------------------------------------------------
    # -- Wybranie xs sasiednich --
    setKm = [float(i[1]) for i in set if i[0] == str.lower(bridge.rzeka).replace(' ', '')]
    setKm.sort()
    kmDown = max([i for i in setKm if i < bridge.km])
    kmUp = min([i for i in setKm if i > bridge.km])
    xsUp = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)]
    xsDown = XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmDown)]
    print(xsUp.points[0].station,"stat1")
    print(xsUp.km, 'km')
    # -- xs dobrane --
    # spasowanie przekroi
    xsUp2, xsDown2 = fit_xs(xsUp,xsDown)
    print(xsUp2.points[0].station, "stat2")
    print(xsUp2.points[0].z, "z2")


    xsDown, xsUp, bridgeShift = fit_bridge(xsDown2, xsUp2, bridge, base_manning=base_manning)
    print(xsUp.points[0].station, "stat3")
    print(xsUp.points[0].z, "z3")
    # wbicie koryta na xs
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)] = xsUp
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmDown)] = xsDown
    # shift bridge
    nwk.culvertList[-1].culvertParams['HorizOffset'] = [0]
    # --- Przekroje dopasowane ---
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), kmUp)] = xsUp
    #bazaXsRawData.append(Xs())
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)] = Xs()
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].riverCode = bridge.rzeka
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].reachCode = bridge.topoID
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].km = bridge.km
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].cords = '    0  00.00  00.00 00.00  00.00\n'
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].fd = '    0\n'  # flow direction
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].pd = '    0\n'  # protect data
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].datum = '    0\n'  # datum
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].cs = 1  # closed
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].rt = '    0\n'  # radius type
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].dx = '    0\n'  # divide xs
    xsID = str.upper(bridge.rzeka[0:3]) + "_M-" + str(bridge.lp).replace(' ', '') + "_C1\n"
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].id = xsID  # section id
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].inter = '    0\n'  # interpolated
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].angle = '    0.00   0\n'  # angle
    #bazaXsRawData[-1].rn = '   0  0     1.000     1.000     1.000    1.000    1.000'  # resistance number
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].rr = None
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].profile = str(len(bridge.przepust))  # profile
    for pkt in bridge.przepust:
        XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].points.append(Pkt('    {}   {}     {}     <#0>     0     0.000     0'.format(pkt[0]+bridgeShift,pkt[1], bridge.mann)))
    XsOrder['{} {}'.format(str.lower(bridge.rzeka).replace(' ', ''), bridge.km)].lp = '   1  0    0.000  0    0.000  250\n'  # level params

    # ---- END XS -----

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
    nwk.weirList[-1].topoID = bridge.topoID
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
    # ---- END WEIR -----
    print(len(XsOrder), "len od XsOrder")
nwk.print_to_nwk(fileWynikNWK)
fileWynikNWK.close()
for element in list(XsOrder.values()):
    element.print_txt(fileWynikXS, None, 1)
