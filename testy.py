from math import sqrt

import matplotlib.pyplot as plt


def distance(x1, x2, y1, y2):
    try:
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    except:
        return 0


def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    def is_between(x1, y1, x, y, x2, y2):
        return round(distance(x1, x, y1, y)) + round(distance(x, x2, y, y2)) == round(distance(x1, x2, y1, y2))

    line1 = [[x1, y1], [x2, y2]]
    line2 = [[x3, y3], [x4, y4]]
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        print('brak przeciecia')
        x = None
        y = None
        b = None
        c = None
    else:
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        b = (is_between(x3, y3, x, y, x4, y4))
        c = (is_between(x1, y1, x, y, x2, y2))

    plt.plot(*zip(*line1))
    plt.plot(*zip(*line2))
    plt.plot([x], [y], 'ro')
    plt.show()
    return x, y, b, c


print(line_intersection(0, 0, 100, 100, 0, 20, 10, 20))
plt.close()
