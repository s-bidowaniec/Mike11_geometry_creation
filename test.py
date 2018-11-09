lista = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

a = 5
for i in range(2):
    part = [x if x > a else None for x in lista]

    print(part)
    x=0