from google.appengine.ext import ndb


class Like(ndb.Model):
    """ Model for basic like
    Changed:
        For like properties 0 - dislike, 1 - default, 2 - like.
        POIID is id from POI table. 
        deviceID is id of a device taken from user table.  
    """
    POIID = ndb.IntegerProperty()
    deviceID = ndb.StringProperty()
    viewed = ndb.BooleanProperty()
    like  = ndb.IntegerProperty()