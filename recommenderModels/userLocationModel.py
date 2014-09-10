from google.appengine.ext import ndb


class userLocation(ndb.Model):
    """ Model for devices location related data """
    deviceID = ndb.StringProperty()
    lat = ndb.FloatProperty()
    lon = ndb.FloatProperty()
    acc = ndb.StringProperty()
    ssid = ndb.StringProperty()
    bssid = ndb.StringProperty()
    date = ndb.DateTimeProperty()