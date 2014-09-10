import numpy as np

from re import search
from google.appengine.ext import ndb

from recommenderModels.userLocationModel import userLocation
from recommenderModels.POImodels import POI
from recommenderFunctions.recommender_misc import get_poi_within_radius, distance_between_points


def _get_activity1(ssid):
    """
    Activity according to SSID
    """
    places = {
        'cafe': ['cafe', 'caffe', 'kafe', 'bar', 'pub', 'kafana'],
        'restaurant': ['restaurant', 'restoran', 'pizzeria', 'picerija', 'food'],
        'hotel': ['hotel', 'motel']
    }

    for key in places.keys():
        for name in places[key]:
            match = search(name, ssid.lower())
            if match:
                return key

    return None


def _get_activity2(speed, previous=None):
    """
    Activity according to speed
    :return: 0-STANDING, 1-WALKING, 2-TRANSPORT
    """
    act = 3
    p = {0: (0.5 ** (1 / 0.3)) ** speed, 1: (0.5 ** (1 / 1.1)) ** abs(speed - 1.4),
         2: 0.5 + np.arctan(speed - 2.5) / np.pi}

    mat = [[0.6, 0.3, 0.1], [0.3, 0.5, 0.2], [0.2, 0.2, 0.6]]

    mx = 0
    mi = 0
    i = 0

    for a in range(act):
        if previous is not None:
            if mx < mat[previous][a] * p[a]:
                mx = mat[previous][a] * p[a]
                mi = i
        else:
            if mx < p[a]:
                mx = p[a]
                mi = i
        i += 1

    return mi


def activity(dev_id):
    """
    :return: return tuple (moving_code, place)
    moving_code: -1-CAN_NOT_CALCULATE_SPEED, 0-STANDING, 1-WALKING, 2-TRANSPORT
    places: cafe, restaurant, hotel
    """
    ancestor_key = ndb.Key("FIContent_v1", "userLocation")

    points = userLocation.query(ancestor=ancestor_key).filter(userLocation.deviceID == dev_id).order(
        userLocation.date).fetch()

    l = len(points)

    if l >= 2:
        a = (points[l - 1].lat, points[l - 1].lon)
        b = (points[l - 2].lat, points[l - 2].lon)
        d = distance_between_points(a[0], a[1], b[0], b[1])

        t = (points[l - 1].date - points[l - 2].date).seconds
        if t > 0:
            speed = d / t
            a2 = _get_activity2(speed)
        else:
            a2 = -1
    else:
        a2 = -1

    a1 = None
    if l >= 1:
        ssid = points[l - 1].ssid.split('\r\n')
        for x in ssid:
            a1 = _get_activity1(x)
            if a1 is not None:
                break

    return a2, a1


def get_list_of_sorted_poi(matrix_of_poi, max_radius, user_lat, user_lon):
    values = []
    list_poi_in_radius = get_poi_within_radius(user_lat, user_lon, max_radius)

    for poi in matrix_of_poi:
        for row in list_poi_in_radius:
            if poi[0] == row[1].key.id():
                values.append((row[1], row[0], poi[1]))

    header = [('POI', POI), ('distance', float), ('rating', float)]

    ret_list = np.array(values, dtype=header)
    ret_list.sort(order=['rating', 'distance'])

    return ret_list
