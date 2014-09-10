from math import sin, cos, atan2, sqrt, radians, degrees
from google.appengine.ext import ndb
from recommenderModels.POImodels import POI


def distance_between_points(lat_a, lon_a, lat_b, lon_b):
    """
    Calculates the distance in metres between two gps points
    :param lat_a: the latitude of the first point
    :param lon_a: the longitude of the first point
    :param lat_b: the latitude of the second point
    :param lon_b: the longitude of the second point
    :return: returns the distance in metres
    """
    r = 6378100  # radius of the earth in metres
    d_lon = radians(lon_b - lon_a)
    d_lat = radians(lat_b - lat_a)
    a = ((sin(d_lat/2)) ** 2) + cos(radians(lat_a)) * cos(radians(lat_b)) * ((sin(d_lon/2)) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return r * c


def get_poi_between_latitudes(lat_min, lat_max, category_id=None):
    """
    Returns all POI that have their latitudes between lat_min i lat_max
    :param lat_min:
    :param lat_max:
    :param category_id:
    :return:
    """
    ancestor_key = ndb.Key("FIContent_v1", "POI")
    if category_id is not None:
        poi_query = POI.query(ancestor=ancestor_key).filter(POI.lat > lat_min).filter(POI.lat < lat_max)\
            .filter(POI.categoryID == category_id)
    else:
        poi_query = POI.query(ancestor=ancestor_key).filter(POI.lat > lat_min).filter(POI.lat < lat_max)

    return poi_query.fetch(projection=[POI.lat, POI.lon])


def process_poi(potential_poi, radius, p_lat, p_lon, p_lon_min, p_lon_max):
    """
    Finds all poi given in the array potential_poi in the given radius of a point
    :param potential_poi: a list of POI
    :param radius: the requested radius
    :param p_lat: latitude of the point
    :param p_lon: longitude of the point
    :param p_lon_min: minimum longitude
    :param p_lon_max: maximum longitude
    :return: a list of tuples (distance, POI)
    """
    out_dict = []
    for poi in potential_poi:
        if p_lon_min < poi.lon < p_lon_max:
            dist = distance_between_points(p_lat, p_lon, poi.lat, poi.lon)
            if dist < radius:
                out_dict.append((dist, poi))
    return out_dict


def get_poi_within_radius(p_lat, p_lon, radius, category_id=None):
    """
    Returns all the points of interest (POI) within the radius of the given point
    The POI have only the longitude and latitude fields set
    :param p_lat: the latitude of the given point
    :param p_lon: the longitude of the given point
    :param radius: the radius in metres
    :param category_id: the optional id of a certain category if left blank all categories will be considered
    :return: returns a list of tuples (distance, POI)
    """
    approx_error = 100

    r_longitude = 6378100 * cos(radians(45.2516700))
    r_latitude = 6378100.0

    approx_latitude_shift = degrees((radius + approx_error) / r_latitude)
    approx_longitude_shift = degrees((radius + approx_error) / r_longitude)

    p_lat_min = p_lat - approx_latitude_shift
    p_lat_max = p_lat + approx_latitude_shift

    p_lon_min = p_lon - approx_longitude_shift
    p_lon_max = p_lon + approx_longitude_shift

    potential_poi = get_poi_between_latitudes(p_lat_min, p_lat_max, category_id)

    return process_poi(potential_poi, radius, p_lat, p_lon, p_lon_min, p_lon_max)


def get_poi_within_radius_old(p_lat, p_lon, radius, category_id=None):
    """
    Returns all the points of interest (POI) within the radius of the given point
    :param p_lat: the latitude of the given point
    :param p_lon: the longitude of the given point
    :param radius: the radius in metres
    :param category_id: the optional id of a certain category if left blank all categories will be considered
    :return: returns a list of tuples (distance, POI)
    """
    ret_val = []
    ancestor_key = ndb.Key("FIContent_v1", "POI")

    if category_id is not None:
        poi_query = POI.query(ancestor=ancestor_key).filter(POI.categoryID == category_id)
    else:
        poi_query = POI.query(ancestor=ancestor_key)

    potential_poi = poi_query.fetch()

    for poi in potential_poi:
        dist = distance_between_points(p_lat, p_lon, poi.lat, poi.lon)
        if dist < radius:
            ret_val.append((dist, poi))

    return ret_val