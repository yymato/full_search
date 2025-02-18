import math


def lonlat_dist(self_point, org_point):
    self_x, self_y = map(float, self_point.split(','))
    org_x, org_y = map(float, org_point.split(','))

    x = abs(self_x - org_x)
    y = abs(self_y - org_y)
    median_lat = (self_y + org_y) / 2

    x_meters = (6400 * 1000) * math.cos(math.radians(median_lat)) * math.radians(x)
    y_meters = (6400 * 1000) * math.radians(y)

    distance = math.sqrt(x_meters ** 2 + y_meters ** 2)
    return distance


