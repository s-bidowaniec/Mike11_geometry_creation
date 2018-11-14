
# coding: utf-8

# In[29]:



import ogr
import math


# In[70]:


# podaj sciezke do pliku *.shp:
shapefile = r"D:\ISOK_II\MODELE\Przemsza_API\SHP\Robocze\Przekroje_korytowe_3D.shp"

# okresl pole w pliku *.shp charakterystyczne dla kazdego przekroju:
field = "Nr_przekr"

driver = ogr.GetDriverByName("Esri Shapefile")
dataSource = driver.Open(shapefile, 0)
layer = dataSource.GetLayer()

for feature in layer:
    # river = feature.GetField("RiverCode")
    ident = feature.GetField("Nr_przekr")
    geom = feature.GetGeometryRef()
    count = geom.GetPointCount()
    xp = geom.GetX(0)
    yp = geom.GetY(0)
    xk = geom.GetX(count-1)
    yk = geom.GetY(count-1)
    maxDistance = math.sqrt(((xk-xp)**2) + ((yk-yp)**2))
    number = 1
    distance = None
    while number < count:
        
        x = geom.GetX(number)
        y = geom.GetY(number)
        dxp = abs(xp-x)
        dyp = abs(yp-y)
        dxk = abs(xk-x)
        dyk = abs(yk-y)
        
        # obliczanie odleglosci vertexa od pierwszego punktu
        if dxp and dyp:
            distP = math.sqrt((dxp**2)+(dyp**2))
        elif dxp:
            distP = dxp
        elif dyp:
            distP = dyp
        else:
            print("\nBlad przy wyliczaniu odleglosci od poczatku przekroju:\n"
                  "identyfikator:", ident, "\n"
                  "Punkt poczatku:", xp, ";", yp, "\n"
                  "Punkt obliczany:", x, ";", y, end= '\n\n')
            distP = 0
            
        # obliczanie odleglosci vertexa od ostatniego punktu
        if dxk and dyk:
            distK = math.sqrt((dxk**2)+(dyk**2))
        elif dxk:
            distK = dxk
        elif dyk:
            distK = dyk
        elif count - 1 == number:
            pass
        else:
            print("\nBlad przy wyliczaniu odleglosci od konca przekroju:\n"
                  "identyfikator:", ident, "\n"
                  "Punkt konca:", xk, ";", yk, "\n"
                  "Punkt obliczany:", x, ";", y, end= '\n\n')
            
        if not distance:
            distance = distP
            
        elif distP <= distance:
            print(hydroID, "punkt:", number)
            
        elif  distP > distance:
            distance = distP
        else:
            print("Blad przy wyliczaniu dist i distance:", ident)
        
        if distP > maxDistance:
            print("Blad konca przekroju:", ident)
            
        if distK > maxDistance:
            print("Blad poczatku przekroju", ident)
            
        number += 1


# In[8]:


dir(geom)


# In[43]:


yk

