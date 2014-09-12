import json
from google.appengine.api import urlfetch

poi_proxy_url = "http://app.prodevelop.es"


def get_poi_proxy_server_response(service_request_url):
    """
    Gets the result from the POI proxy server
    :param service_request_url: the extension to the base url
    :return: the raw request string
    """
    result = urlfetch.fetch(poi_proxy_url + service_request_url, deadline=10)
    if result.status_code == 200:
        return result.content

    return None


def get_available_services():

    """
    Gets all the services that the POI proxy can make use of
    :return: a list dictionary where each key is the name of a service and the value is a dictionary containing the
    relevant information about that service.
    """
    raw_data = get_poi_proxy_server_response("/poiproxy/describeServices")
    return json.loads(raw_data)['services']


def get_available_categories():

    """
    Returns all the categories that the POI proxy can recognize
    :return: A list of strings each string represents a category
    """
    raw_data = get_poi_proxy_server_response("/poiproxy/describeServices")
    return json.loads(raw_data)['categories']


def browse_by_tile(x, y, z):
    """
    Browses POI by a google tile
    :param x: the x of a tile in google maps
    :param y: the y of a tile in google maps
    :param z: the z of a tile in google maps
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, datetaken, dateupload, image, license, name, owner,
    ownername, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/poiproxy/browse?service=panoramio&z=%d&x=%d&y=%d" % (z, y, x)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']


def browse_by_extent(min_x, max_x, min_y, max_y):

    """
    Browses POI within a bounding box
    :param min_x: a value in the coordinate reference system EPSG:4326
    :param max_x: a value in the coordinate reference system EPSG:4326
    :param min_y: a value in the coordinate reference system EPSG:4326
    :param max_y: a value in the coordinate reference system EPSG:4326
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, datetaken, dateupload, image, license, name, owner,
    ownername, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/poiproxy/browseByExtent?service=panoramio&minX=%f&minY=%f&maxX=%f&maxY=%f" % \
              (min_x, min_y, max_x, max_y)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']


def browse_by_radius(lat, lon, radius):
    """
    Browses POI within the radius of a certain point
    :param lat: latitude of a point
    :param lon: longitude of a point
    :param radius: the radius
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, datetaken, dateupload, image, license, name, owner,
    ownername, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/poiproxy/browseByLonLat?service=panoramio&lon=%f&lat=%f&dist=%f" % (lat, lon, radius)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']


def search_by_tile(x, y, z, search_term):
    """
    Searches POI by a google tile
    :param x: the x of a tile in google maps
    :param y: the y of a tile in google maps
    :param z: the z of a tile in google maps
    :param search_term: the term you are searching for ex. cave, bar...
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, datetaken, dateupload, image, license, name, owner,
    ownername, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/poiproxy/browse?service=flickr&z=%d&x=%d&y=%d&query=%s" % (z, y, x, search_term)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']


def search_by_extent(min_x, max_x, min_y, max_y, search_term):
    """
    Searches POI within a bounding box
    :param min_x: a value in the coordinate reference system EPSG:4326
    :param max_x: a value in the coordinate reference system EPSG:4326
    :param min_y: a value in the coordinate reference system EPSG:4326
    :param max_y: a value in the coordinate reference system EPSG:4326
    :param search_term:  cave, bar...
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, datetaken, dateupload, image, license, name, owner,
    ownername, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/poiproxy/browseByExtent?service=flickr&minX=%f&minY=%f&maxX=%f&maxY=%f&query=%s" % \
              (min_x, min_y, max_x, max_y, search_term)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']


def search_by_radius(lat, lon, radius, search_term):
    """
    Searches POI within the radius of a certain point
    :param lat: latitude of a point
    :param lon: longitude of a point
    :param radius: the radius
    :param search_term:  cave, bar...
    :return: list of Features. Each feature is a dictionary with the following fields : 'geometry' and 'properties'
    geometry is also a dictionary and it has the following fields : coordinates
    coordinates is a list of two points that represent the longitude and latitude of the point
    properties is a dictionary with the following fields : _content, datetaken, dateupload, image, license, name, owner,
    ownername, place_id, px_categories, px_service, url_l, url_m, url_s, url_t, views
    all these fields are a string
    """
    request = "/poiproxy/browseByLonLat?service=flickr&lon=%f&lat=%f&dist=%f&query=%s" % (lat, lon, radius, search_term)
    raw_data = get_poi_proxy_server_response(request)
    return json.loads(raw_data)['features']