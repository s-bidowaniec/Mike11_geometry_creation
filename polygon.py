import numpy as np
array = [[0.928347365933718,391.32],[3.20855993299333,392.83],[5.5629339357402,391.33]]


def linear_equation(array):
    a = np.array([
         [(array[0][0]) ** 2, array[0][0], 1],
         [(array[1][0]) ** 2, array[1][0], 1],
         [(array[2][0]) ** 2, array[2][0], 1]
         ])
    b = np.array([
        array[0][1],
        array[1][1],
        array[2][1]
        ])
    x = np.linalg.solve(a,b)
    return lambda y: x[0]*y**2 + x[1]*y + x[2]

print(linear_equation(array)(2.5))