from google.appengine.ext import ndb


class Category(ndb.Model):
    """ Model for basic category """
    categoryID = ndb.IntegerProperty()
    name = ndb.StringProperty()