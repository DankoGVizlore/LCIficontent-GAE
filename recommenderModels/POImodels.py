from google.appengine.ext import ndb


class POI(ndb.Model):
    """ Model for basic POI 
        for days we use 1 - Monday; 2 - Tuesday; 3 - Wednesday; 4 - Thursday; 5 - Friday; 6 - Saturday; 7 - Sunday;
        categoryID is a ID from category table
    """
    name = ndb.StringProperty()
    categoryID = ndb.IntegerProperty()
    lat = ndb.FloatProperty()
    lon = ndb.FloatProperty()
    description = ndb.TextProperty()
    open = ndb.StringProperty()
    close = ndb.StringProperty()
    days = ndb.IntegerProperty()
    address = ndb.StringProperty()
    website = ndb.StringProperty()