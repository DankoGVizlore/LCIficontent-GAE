#Andrej fill in the descriptions
import webapp2
import numpy as np

from recommenderModels.categoryModel import *
from recommenderModels.POImodels import *
from recommenderModels.likeModel import *


class DataAcquisition(webapp2.RequestHandler):
    """ Global variables for given class"""

    def __init__(self):
        """

        """
        super(DataAcquisition, self).__init__()
        self.ancestor_key_category = ndb.Key("FIContent_v1", "Category")
        self.ancestor_key_POI = ndb.Key("FIContent_v1", "POI")
        self.ancestor_key_likes = ndb.Key("FIContent_v1", "Like")
        self.POIMap = self.get_poi_mapping()

    """ Functions available in this class"""

    def get_number_of_categories(self):
        """

        :return:
        """
        number_of_categories = Category.query(ancestor=self.ancestor_key_category).count()
        return number_of_categories

    def get_number_of_poi(self):
        """

        :return:
        """
        number_of_poi = POI.query(ancestor=self.ancestor_key_POI).count()
        return number_of_poi

    def get_number_of_rated_poi(self, user_id):
        """

        :param user_id:
        :return:
        """
        number_of_rated_poi = Like.query(ancestor=self.ancestor_key_likes).filter(Like.deviceID == user_id).count()
        return number_of_rated_poi

    def get_poi_features(self):
        """

        :return:
        """
        poi_features = np.zeros((self.get_number_of_poi(), self.get_number_of_categories() + 1))
        # Take names of all categories and map them. To save mapping we use dictionary. 
        # Using this method we don't have to take care about categoryID to be one continuum.
        categories = Category.query(ancestor=self.ancestor_key_category).fetch()
        index = 0
        mapping = dict()
        for category in categories:
            mapping[category.categoryID] = index
            index += 1
        # Going trough POI entities, we update poi_features table for later use.
        features = POI.query(ancestor=self.ancestor_key_POI).fetch()
        row_number = 0
        for row in features:
            poi_features[row_number, mapping[row.categoryID] + 1] = 1
            row_number += 1
        # Every feature vector should start with 1, this one number needs to be inserted in this way.
        for line in range(row_number):
            poi_features[line, 0] = 1

        return poi_features

    def get_poi_mapping(self):
        """

        :return:
        """
        poi_mapping = dict()
        poi_entities = POI.query(ancestor=self.ancestor_key_POI).fetch()
        index = 0
        for entity in poi_entities:
            poi_mapping[entity.key.id()] = index
            index += 1
        return poi_mapping

    def get_user_ratings(self, user_id):
        """

        :param user_id:
        :return:
        """
        user_ratings = np.zeros((1, self.get_number_of_poi()))
        # POIMap = self.getPOIMapping()
        # Going trough likePOIs we copy ratings to this new table.
        liked_poi = Like.query(ancestor=self.ancestor_key_likes).filter(Like.deviceID == user_id).fetch()
        for row in liked_poi:
            if row.viewed:
                user_ratings[0, self.POIMap[row.POIID]] = 1 + row.like
        return user_ratings

    # I'm using get just for testing        
    def get(self):
        """

        """
        self.response.write("OK! <br>")
        self.get_user_ratings(1)
        self.response.write(self.get_poi_features())


app = webapp2.WSGIApplication([
                                  ('/recommender/dataAcquisition', DataAcquisition)
                              ], debug=True)