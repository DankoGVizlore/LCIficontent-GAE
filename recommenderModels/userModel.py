from google.appengine.ext import ndb


class User(ndb.Model):
    """ Model for basic user data """
    """ deviceId has been changed to string """
    deviceID = ndb.StringProperty()
    GCMRegID = ndb.StringProperty()