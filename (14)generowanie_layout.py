from functions import *
import os

inputSim = r"K:\Wymiana danych\Karol\Staszek\S02_CICHA_WODA_v3.02\01_MIKE11\01_SIM\S02_CICHA_WODA_500.sim11"
river = "Cicha woda"

read11res_lok = "\"C:\\Program Files (x86)\\DHI\\2011\\bin\\RES11READ.exe\""


with open(inputSim, 'r') as sim:
    dataSim = sim.read().splitlines(True)
res = False
for line in dataSim:
    line = line.split()
    if len(line) > 1:
        if line[0] == 'nwk':
            nwk = line[-1].replace('|', '')
        elif line[0] == 'start':
            start = line[1:]
        elif line[0] == 'start':
            start = line[1:]
        elif line[0] == '[Results]':
            res = True
        elif line[0] == 'hd':
            hd = line[1:][1].replace('|', '').replace(',', '')


tempNwk = nwk.split('\\')
level = tempNwk[0].count('.')
tempLoc = inputSim.split('\\')[:-level]
inputNwkDir = '\\'.join(tempLoc+tempNwk[1:])

tempHd = hd.split('\\')
level = tempHd[0].count('.')
tempLoc = inputSim.split('\\')[:-level]
res11_lok = '\\'.join(tempLoc+tempHd[1:])

claOutput = '\\'.join(tempLoc+tempHd[1:-1]+[river+'.CLA'])

fileWejscieNWK = open(inputNwkDir, 'r')
nwk = read_NWK(fileWejscieNWK)

fileCLA = open(claOutput,'w')


os.system(read11res_lok + " -xy -max1 " + res11_lok + " " + 'outTest.csv')
with open('outTest.csv', 'r') as fin:
    data = fin.read().splitlines(True)
    data = data[19:-3]
os.remove('outTest.csv')
a = r"""
// Created     : 2018-12-31 8:14:13
// DLL id      : C:\Program Files (x86)\DHI\2011\bin\pfs2004.dll
// PFS version : Jan  6 2011 20:45:15

[Bitmaps]
EndSect  // Bitmaps

[GroupNames]
EndSect  // GroupNames

[MV_Resul_Window]
   [Position]
      cs_x = 43
      cs_y = 27
      cs_cx = 1697
      cs_cy = 948
      Status = 1
   EndSect  // Position

   [AXIS_LIST]
      [AXIS]
         A_type = 2
         Units = '[meter]'
         Label = ''
         FUnits = 1
         FLabel = 1
         Info = {xStart}, {xEnd}, true, 0, 1
      EndSect  // AXIS

      [AXIS]
         A_type = 3
         Units = '[meter]'
         Label = ''
         FUnits = 1
         FLabel = 1
         Info = {yStart}, {yEnd}, true, 0, 0
      EndSect  // AXIS

   EndSect  // AXIS_LIST

   [Horiz_Font]
      lfHeight = -11
      lfWidth = 0
      lfEscapement = 0
      lfOrientation = 0
      lfWeight = 400
      lfItalic = 0
      lfUnderline = 0
      lfStrikeOut = 0
      lfCharSet = 0
      lfOutPrecision = 2
      lfClipPrecision = 2
      lfQuality = 1
      lfPitchAndFamily = 34
      lfFaceName = 'Arial'
   EndSect  // Horiz_Font

   [Parameters]
      dGrid = true
      dUnits = true
      dAxisLabels = true
      dWinHeather = true
      x_orient = true
      y_orient = true
      BMP = false, ''
      DXF = false, ''
      DXFparam = 0, 192, 192, 192, false
      m_EMF_FileNamePrefix = ''
      WriteToEMF = 1
      useClassName = 1
      IncludeDateInEMFFileName = 1
      LegendePos = 0
      drawLegend = false
      ShowLogotype = false
      [Bitmaps]
      EndSect  // Bitmaps

      bNodes = true
      bPipes = true
      bLabels = false
      bSlope = true
      bPipeSize = 1
      bStrucSize = 5
      bNodeSize = 3
      bNodeSize = 3
      bFlowDir = true
      FlowDirNum = 1
      m_drawUserTitle = false
      m_userTitle = ''
   EndSect  // Parameters

   [RESULT_SOURCE]
      MOUSE_MIKE = 2, 'MIKE11'
      ItemNum1 = 100
      ItemNum2 = 0
      WIN_TYPE = 4, 'Horiz'
      FileNum = 0
      PlanTyp = 1
      MinmaxAnim = 10
      SynchroTime = '00:00:00'
      pOverView = 1796, 0, 136, 100, 1
      Palle_pos = 60, 58, 140, 276
      Palle_param = 1, true
      [ColPalletteFont]
         lfHeight = 12
         lfWidth = 0
         lfEscapement = 0
         lfOrientation = 0
         lfWeight = 400
         lfItalic = 0
         lfUnderline = 0
         lfStrikeOut = 0
         lfCharSet = 0
         lfOutPrecision = 15
         lfClipPrecision = 0
         lfQuality = 0
         lfPitchAndFamily = 34
         lfFaceName = 'MS Sans Serif'
      EndSect  // ColPalletteFont

   EndSect  // RESULT_SOURCE

   [PALETTES]
   EndSect  // PALETTES

   [FULL_DATA]
      ResFile = '{hdRes}', 1, 1969, 2, 100, 200
      ResFileM11_new = '{res11lok}', 1, 1969, 2, 100, '', 'Water Level', 'Water Level', 200, '', 'Discharge', 'Discharge'
   EndSect  // FULL_DATA

   [Encroachment]
   EndSect  // Encroachment

EndSect  // MV_Resul_Window

[GroupInfo]
EndSect  // GroupInfo

[MV_Resul_Window]
   [Position]
      cs_x = 310
      cs_y = 209
      cs_cx = 1787
      cs_cy = 999
      Status = 1
   EndSect  // Position

   [AXIS_LIST]
      [AXIS]
         A_type = 2
         Units = '[m]'
         Label = ''
         FUnits = 1
         FLabel = 1
         Info = {kmStart}, {kmEnd}, true, 0, 1
      EndSect  // AXIS

      [AXIS]
         A_type = 3
         Units = '[meter]'
         Label = ''
         FUnits = 1
         FLabel = 1
         Info = {zStart}, {zEnd}, true, 0, 0
      EndSect  // AXIS

   EndSect  // AXIS_LIST

   [axisFont]
      lfHeight = -11
      lfWidth = 0
      lfEscapement = 0
      lfOrientation = 0
      lfWeight = 400
      lfItalic = 0
      lfUnderline = 0
      lfStrikeOut = 0
      lfCharSet = 0
      lfOutPrecision = 2
      lfClipPrecision = 2
      lfQuality = 1
      lfPitchAndFamily = 34
      lfFaceName = 'Arial'
   EndSect  // axisFont

   [Parameters]
      dGrid = true
      dUnits = true
      dAxisLabels = true
      dWinHeather = true
      x_orient = true
      y_orient = true
      BMP = false, ''
      DXF = false, ''
      DXFparam = 0, 192, 192, 192, false
      m_EMF_FileNamePrefix = ''
      WriteToEMF = 1
      useClassName = 1
      IncludeDateInEMFFileName = 1
      LegendePos = 0
      drawLegend = false
      ShowLogotype = false
      [Bitmaps]
      EndSect  // Bitmaps

      m_bColl = false
      m_bMin = true
      m_bMax = true
      m_UserTitle = ''
      m_drawUserTitle = 0
      m_MI_label1 = true
      m_MI_label2 = true
      m_Cross1 = false
      m_Cross2 = true
      m_Cross3 = false
      m_vertical = 0
      m_bLabels = true
      Angle = 45
      m_SecItemDecNum = 3
      m_secItemLegend = 1
      m_avoidOverlapping = 1
      m_animGraph = 0
      m_animTable = 0
      m_dchainage = 0
      m_FillWater = true
      m_DrawHistory = false
      PumpThickness = 2
      PumpColor = 0
      WeirThickness = 2
      WeirColor = 0
      DisVertCoef = 2
   EndSect  // Parameters

   [RESULT_SOURCE]
      MOUSE_MIKE = 2, 'MIKE'
      WIN_TYPE = 2, 'LongProf'
      FileNum = 0
      ItemNum = 100
      ManItemNum = -1
      SynchroTime = '{synchroTime}'
   EndSect  // RESULT_SOURCE

   [MultipleAreas]
      NumofSubArea = 0
   EndSect  // MultipleAreas

   [MV_GraphItems]
      [OneGraphItem]
         DefaultName = 'Water Level'
         ActName = ''
         dynamicItem = 1
         staticItemType = 0
         userMark = 0
         interpol = 0
         useSecondAxis = 0
         AreaNum = 0
         filepos = 0
         res_item_pos = 0
         lineWidth = 0
         linestyle = 0
         drawLine = true
         line_color = 0
         marker_type = 0
         marker_size = 3
         marker_fill = 0
         marker_color = 0
         drawNarker = false
         Axis = 0
         Value = 0
         ValueY = 0
      EndSect  // OneGraphItem

   EndSect  // MV_GraphItems

   [MV_DiffItems]
   EndSect  // MV_DiffItems

   [MV_TabItems]
   EndSect  // MV_TabItems

   [ProfTableFontName]
      lfHeight = -11
      lfWidth = 0
      lfEscapement = 0
      lfOrientation = 0
      lfWeight = 400
      lfItalic = 0
      lfUnderline = 0
      lfStrikeOut = 0
      lfCharSet = 0
      lfOutPrecision = 2
      lfClipPrecision = 2
      lfQuality = 1
      lfPitchAndFamily = 34
      lfFaceName = 'Arial'
   EndSect  // ProfTableFontName

   [MV_CapacityCalc]
      testTypes = 0
      resultFilePos = -1
      numOfCalcs = 0
   EndSect  // MV_CapacityCalc

   [MV_Indicators]
   EndSect  // MV_Indicators

   [PROFILE_DEF]
{profile}
   EndSect  // PROFILE_DEF

EndSect  // MV_Resul_Window

[GroupInfo]
EndSect  // GroupInfo

[Logo]
   [LogoFont]
      lfHeight = -11
      lfWidth = 0
      lfEscapement = 0
      lfOrientation = 0
      lfWeight = 400
      lfItalic = 0
      lfUnderline = 0
      lfStrikeOut = 0
      lfCharSet = 0
      lfOutPrecision = 2
      lfClipPrecision = 2
      lfQuality = 1
      lfPitchAndFamily = 34
      lfFaceName = 'Arial'
   EndSect  // LogoFont

   Text1 = ''
   Text2 = ''
   Draw = false
   File = ''
   Path = ''
EndSect  // Logo


"""

dane = nwk.start.split()
x0 = dane[dane.index('x0')+2]
y0 = dane[dane.index('y0')+2]
x1 = dane[dane.index('x1')+2]
y1 = dane[dane.index('y1')+2]
bazaXs = []
kmList = []
maxZ = 0.0
minZ = 3000.0

data2 = []
for index in range(len(data)-2):
    try:
        line0 = data[index].split()
        line1 = data[index+1].split()
        line2 = data[index+2].split()
        if int(float(line0[4])) == 2 and int(float(line2[4])) == 2 and int(float(line1[4])) == 0:
            data2.append(float(line1[3]))
    except:
        break

for line in data:
    line = line.split()
    if len(line) == 0: break
    correct = False
    while not correct:
        try:
            float(line[3])
            correct = True
        except:
            line[2] = line[2] + ' ' + line.pop(3)
    if river.lower() in line[2].lower() and (int(float(line[4])) == 0 or int(float(line[4])) == 1):
        bazaXs.append(line)

        if float(line[5]) > maxZ:
            maxZ = float(line[5])
        if float(line[5]) < minZ:
            minZ = float(line[5])
        if float(line[3]) not in data2:
            kmList.append(float(line[3]))

river = bazaXs[0][2]
kmList = set(kmList)
kmList = list(kmList)
kmList.sort()
startKm = kmList[0]
endKm = kmList[-1]
branchLine = """      BRANCH = '{river} ', {kmStart}, {kmEnd}, 0"""
profileDef = []
for km in range(len(kmList)-1):
    profileDef.append(branchLine.format(river=river, kmStart=kmList[km], kmEnd=kmList[km+1]))

profileDef = "\n".join(profileDef)

day = start[2]
if len(day) == 1:
    day = '0'+ day
hour = start[4]
if len(hour) == 1:
    hour = '0'+hour
fileCLA.write(a.format(xStart=x0, xEnd=x1, yStart=y0, yEnd=y1, kmStart=startKm-500, kmEnd=endKm+500, zStart=minZ-5, zEnd=maxZ+5, synchroTime= '{}.{}.{} {}:00:00'.format(start[3], day, start[1], hour), profile=profileDef, hdRes=hd, res11lok=res11_lok))
fileCLA.close()
