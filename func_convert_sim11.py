import codecs
import os
import time
import geopandas
import pandas as pd
from shapely.geometry import Point, Polygon
import shapefile
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


def convert_res11(res11_lok):
    nazwa = os.path.basename(res11_lok)
    nazwa = os.path.splitext(nazwa)[0]
    if "HDAdd" not in nazwa:
        # lokalizacja progframiku mike do konwersji res11
        read11res_lok = "\"C:\\Program Files (x86)\\DHI\\2011\\bin\\RES11READ.exe\""
        # stworzenie folderu do zapisu wynikow
        lok_file = os.path.dirname(res11_lok)
        if not os.path.exists(lok_file + "\\GIS"):
            os.makedirs(lok_file + "\\GIS")

        res_lok = lok_file + "\\GIS"
        # ------------------------------------------------------------------------------------------------------------------------
        # wywołanie programiku res11read do konwersji res 11 na cos przystepnego xy

        os.system('"'+read11res_lok + " -xyh " + '"'+res11_lok+'"' + " " + '"'+res_lok+ "\\" + nazwa + ".csv"+'"'+'"')

        # wywalenie majkowej inwokacji pliku
        data2=[]
        with open(res_lok + "\\" + nazwa + ".csv", 'r') as fin:
            data = fin.read().splitlines(True)
            data = data[19:-3]

            for line in data:
                line = line[:24] + ' ' + line[24:]
                if len(line.split()) > 16:
                    line = line.split()
                    line = line[0:2]+[line[2]+"_"+line[3]]+line[3:]
                    line = ' '.join(line)
                data2.append(line)
        with open(res_lok + "\\" + nazwa + ".csv", 'w') as fout:
            fout.writelines(data2)

        # dodanie nagłówka pliku na sztywny zdefiniowany w line 37
        plik = codecs.open(res_lok + "\\" + nazwa + ".csv", "r", encoding='windows-1250')
        napis = plik.readline()
        plik2 = codecs.open(res_lok + "\\" + nazwa + "_out.csv", "w", encoding='utf-8')
        # "X_Left ", "Y_Left ", "X_Right ", "Y_Right ", "X_Marker_1 ", "Y_Marker_1 ", "X_Marker_3 ", "Y_Marker_3\n",
        title = [" X ", "Y ", "River ", "Chainage ", "Type ", "Bottom ", "LeftBank ", "RightBank ", "X_Left ",
                 "Y_Left ", "X_Right ", "Y_Right ", "X_Marker_1 ", "Y_Marker_1 ", "X_Marker_3 ", "Y_Marker_3\r\n"]
        plik2.writelines(title)

        # usuwa powielajace sie znaki podzialu, programik z mike dzieli spacjami w roznej ilosci, tak zeby bylo
        # czytelne dla ludzi
        while napis != '':
            licznik = 0
            napis = list(napis)
            while licznik < len(napis):
                if napis[licznik] == " ":
                    while napis[licznik + 1] == " ":
                        del napis[licznik]
                licznik += 1
            napis = "".join(napis)
            # print(napis)
            plik2.writelines(napis)
            napis = plik.readline()
        plik.close()
        plik2.close()
        # ------------------------------------------------------------------------------------------------------------------------
        # wywolanie programiku res11read do konwersji res 11 na cos przystepnego h
        # -allres -OutputFrequency10
        os.system('"'+read11res_lok + " -allres -FloodWatch " + '"'+res11_lok+'"' + " " + '"'+res_lok + "/" + nazwa + "_h.csv"+'"'+'"')

        with open(res_lok + "\\" + nazwa + "_h.csv") as f:
            lines = f.read().splitlines()
            ts = []
            for line in lines:
                line2 = line.split(';')
                ts.append(line2)
            # print("test ts")
            # print(ts[26][1])

        with open(res_lok + "\\" + nazwa + "_out.csv") as f:
            lines = f.read().splitlines()
            srednie_l = []
            xy = []
            for line in lines:
                line2 = line.split(' ')
                xy.append(line2[1:])
            kroki_czasowe = len(ts) - 1
            df_xy = {}
            xy[0].append("H_elev")
            xy[0].append("H_elev_test")
            for i in range(len(xy)-1):
                srednia = (float(ts[kroki_czasowe][i + 1]) + float(ts[kroki_czasowe - 1][i + 1]) + float(
                    ts[kroki_czasowe - 2][i + 1])) / 3
                last = float(ts[kroki_czasowe][i + 1])
                differ = srednia - last

                xy[i+1].append(last)
                xy[i + 1].append(0)
                srednie_l.append(differ)

            #xy2 = [[row[i] for row in xy] for i in range(len(xy[0]))]
            xy2 = list(zip(*xy))


            for x in range(len(xy2)):
                df_xy[xy2[x][0]] = xy2[x]

            df = pd.DataFrame(data=df_xy)
            konwert = list(zip(*ts))

        # usuniecie powielen
        df = df.drop_duplicates()

        # usuwanie przekroi o Type = 1 (nie wiadomo co to, wychodza obrocone)
        df = df[df.Type != "1"]
        # usuniecie link channel
        counts = df['River'].value_counts()
        print(counts)
        counts[counts > 2]
        df = df[df['River'].isin(counts[counts > 3].index)]

        total_rows = df.shape[0]
        print("Ilosc wierszy: ")
        print(total_rows)
        m1 = []
        m2 = []
        m3 = []
        for i in range(total_rows):
            m1.append("m1")
            m2.append("m2")
            m3.append("m3")

        m1 = pd.Series(data=m1)
        m2 = pd.Series(data=m2)
        m3 = pd.Series(data=m3)


        koryto = df[['X', 'Y', 'H_elev', 'River', 'Chainage', ]]
        koryto['M'] = m2.values

        lewy = df[['X_Marker_1', 'Y_Marker_1', 'H_elev', 'River', 'Chainage', ]]
        lewy = lewy.rename(columns={'X_Marker_1': 'X', 'Y_Marker_1': 'Y'})
        lewy['M'] = m1.values

        prawy = df[['X_Marker_3', 'Y_Marker_3', 'H_elev', 'River', 'Chainage', ]]
        prawy = prawy.rename(columns={'X_Marker_3': 'X', 'Y_Marker_3': 'Y'})
        prawy['M'] = m3.values
        frames = [koryto, lewy, prawy]

        zbiorcza = pd.concat(frames)
        zbiorcza = zbiorcza.sort_values(by=['River','Chainage','M'])
        writer = pd.ExcelWriter(res_lok + "\\" + nazwa + '.xlsx')
        zbiorcza.to_excel(writer, 'Sheet1')
        # df_left.to_excel(writer,'LewyBrzeg')
        # df_right.to_excel(writer,'PrawyBrzeg')
        writer.save()
        writer.close()
        #podzial na zestawy dla rzek teras zalewowych
        grouped = zbiorcza.groupby(['River'])
        l_grouped = list(grouped)
        #wydruk zbiorczego shp
        zbiorcza['geometry'] = zbiorcza.apply(lambda x: Point((float(x.X), float(x.Y))), axis=1)
        zbiorcza = geopandas.GeoDataFrame(zbiorcza, geometry='geometry')
        zbiorcza.to_file(res_lok + "\\" + nazwa + '.shp', driver='ESRI Shapefile')


        #przetwarzanie pojedynczych rzek: poligon i punkty
        #print(df1.head())
        from osgeo import ogr
        for river in range(4):

            #pobieranie wartosci z podzielonego dataframe i tworzenie poligonu
            df1 = l_grouped[river][1]
            df_poligon = df1[df1.M !="m2"]
            df_poligon.Chainage = df_poligon.Chainage.astype(float)
            df_poligon = df_poligon.sort_values(by=['M','Chainage']).reset_index()
            print(df_poligon)
            #pobranie nazwy rzeki
            nazwa = df_poligon.get_value(0,'River')
            #punkty z rzędnymi na cieku
            df_riv_p = df1[df1.M !="m1"]
            df_riv_p = df_riv_p[df_riv_p.M !="m3"]
            df_riv_p = df_riv_p.sort_values(by=['Chainage']).reset_index()

            #tworzenie folderu
            if not os.path.exists(res_lok + "\\"+nazwa):
                os.makedirs(res_lok + "\\"+nazwa)

            res_lok_ri = res_lok + "\\"+nazwa

            # zapis pkt do shp
            df_riv_p['geometry'] = df_riv_p.apply(lambda x: Point((float(x.X), float(x.Y))), axis=1)
            df_riv_p = geopandas.GeoDataFrame(df_riv_p, geometry='geometry')
            df_riv_p.to_file(res_lok_ri + "\\" + nazwa + '.shp', driver='ESRI Shapefile')

            lista_pkt=[]
            lista1_pkt=[]
            for index, row in df_poligon.iterrows():
                print(row)
                lista1_pkt.append(float(row['X']))
                lista1_pkt.append(float(row['Y']))
                lista_pkt.append(lista1_pkt)
                lista1_pkt = []
            print(lista_pkt)
            polowa = int(len(lista_pkt)/2)

            lista = lista_pkt[: polowa]
            lista2 = lista_pkt[polowa :]
            lista2.reverse()
            pierwszy = lista_pkt[0]
            lista_pkt = lista+lista2
            lista_pkt.append(pierwszy)
            lista_pkt.reverse()
            print(lista_pkt)
            w = shapefile.Writer(shapefile.POLYGON)
            w.poly(parts=[lista_pkt])
            w.field('FIRST_FLD', 'C', '40')
            w.record('First', 'Polygon')
            w.save(res_lok_ri+"\\"+"polygon_"+str(nazwa))
            print(res_lok_ri)
    else:
        pass
    return konwert
