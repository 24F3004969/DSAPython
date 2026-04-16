import math


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def closest_strip(strip, d):
    min_val = d
    strip.sort(key=lambda point: point[1])

    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if (strip[j][1] - strip[i][1]) >= min_val:
                break
            min_val = min(min_val, dist(strip[i], strip[j]))
    return min_val


def closest_recursive(pts_x):
    n = len(pts_x)
    if n <= 3:
        min_d = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                min_d = min(min_d, dist(pts_x[i], pts_x[j]))
        return min_d

    mid = n // 2
    mid_point = pts_x[mid]

    dl = closest_recursive(pts_x[:mid])
    dr = closest_recursive(pts_x[mid:])
    d = min(dl, dr)

    strip = []
    for i in range(n):
        if abs(pts_x[i][0] - mid_point[0]) < d:
            strip.append(pts_x[i])

    return min(d, closest_strip(strip, d))


def minDistance(Points):
    pts_x = sorted(Points)
    result = closest_recursive(pts_x)
    return round(result, 2)