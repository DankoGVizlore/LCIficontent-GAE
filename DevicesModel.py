from google.appengine.ext import ndb


class DevicesFIContent(ndb.Model):
    """ Model for devices GCM related data """
    reg_id = ndb.StringProperty()
    device_id = ndb.StringProperty()
    app_id = ndb.StringProperty()
    date = ndb.DateTimeProperty()


class DevicesLocationFIContent(ndb.Model):
    """ Model for devices location related data """
    reg_id = ndb.StringProperty()
    app_id = ndb.StringProperty()
    lat = ndb.StringProperty()
    lon = ndb.StringProperty()
    date = ndb.DateTimeProperty()