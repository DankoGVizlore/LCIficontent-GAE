#Andrej Fill in the missing prams and descriptions
from recommenderFunctions.dataAcquisition import *


class Recommender(webapp2.RequestHandler):

    def __init__(self, user_id):
        """
        Constructor for this class, accept user ID
        :param user_id:
        """
        super(Recommender, self).__init__()
        self.user_id = user_id
        self.data = DataAcquisition()
        self.number_of_POIs = self.data.get_number_of_poi()
        self.number_of_rated_POIs = self.data.get_number_of_rated_poi(user_id)
        self.number_of_classes = self.data.get_number_of_categories()
        self.cost_function = []
        self.theta_hist = np.zeros((1, 8))

    def get_cost_function_result(self, poi_features, user_ratings, user_theta_vector):
        """
        This function returns how far are we from idle fit
        :param poi_features:
        :param user_ratings:
        :param user_theta_vector:
        :return:
        """
        total_cost = 0
        for i in range(self.number_of_POIs):
            if user_ratings[0, i] != 0:
                total_cost += (user_theta_vector.dot(poi_features[i, :]) - user_ratings[0, i]) ** 2

        if self.number_of_rated_POIs != 0:
            return total_cost / (2 * self.number_of_rated_POIs)
        else:
            return 0

    def get_summation(self, poi_features, user_ratings, user_theta_vector, learning_rate, index):
        """
        This function just compute sum term in gradient descent
        :param poi_features:
        :param user_ratings:
        :param user_theta_vector:
        :param learning_rate:
        :param index:
        :return:
        """
        summation = 0
        if index == 0:
            for i in range(self.number_of_POIs):
                if user_ratings[0, i] != 0:
                    summation += (user_theta_vector.dot(poi_features[i, :]) - user_ratings[0, i]) * poi_features[
                        i, index]
        else:
            for i in range(self.number_of_POIs):
                if user_ratings[0, i] != 0:
                    shake = learning_rate * user_theta_vector[0, index]
                    summation += (user_theta_vector.dot(poi_features[i, :]) - user_ratings[0, i]) * poi_features[
                        i, index] + shake

        return summation

    def best_fit(self, poi_features, user_ratings, learning_rate):
        """
        This function runs gradient descent to fit the line closer to given rating
        :param poi_features:
        :param user_ratings:
        :param learning_rate:
        :return:
        """
        user_theta_vector = np.zeros((1, self.number_of_classes + 1))
        new_user_theta_vector = user_theta_vector
        old_cost = 100
        new_cost = 99

        while (new_cost < old_cost) & (abs(new_cost - old_cost) > learning_rate / 10):
            old_cost = new_cost
            new_cost = self.get_cost_function_result(poi_features, user_ratings, user_theta_vector)
            self.cost_function.append(new_cost)

            for i in range(len(user_theta_vector[0, :])):
                new_user_theta_vector[0, i] = \
                    user_theta_vector[0, i] - learning_rate * self.get_summation(poi_features,
                                                                                 user_ratings,
                                                                                 user_theta_vector,
                                                                                 learning_rate,
                                                                                 i)

            self.theta_hist = np.vstack([self.theta_hist, new_user_theta_vector])
            user_theta_vector = new_user_theta_vector

        return user_theta_vector

    # FOR TESTING    
    def get_cost(self):
        """
        Description
        :return:
        """
        return self.cost_function

    def get_theta_hist(self):
        """
        Description
        :return:
        """
        return self.theta_hist

    def get_predicted_ratings(self):
        """
        This function represents main function in this module. After running estimations, we use user_theta_vector to
        calculate what grades will user give to all POIs. Resulting table represents pairs POI - rating.
        :return:
        """
        poi_features = self.data.get_poi_features()
        theta = self.best_fit(poi_features, self.data.get_user_ratings(self.user_id), 0.005)

        results = np.zeros((self.number_of_POIs, 2))
        for key, value in self.data.POIMap.iteritems():
            results[value, 0] = key
            results[value, 1] = theta.dot(poi_features[value, :])
        return results

    def get(self):
        """
        I'm using get just for testing for now
        """
        self.response.write("Recommender process!")
        self.response.write(str(self.number_of_POIs))


app = webapp2.WSGIApplication([
                                  ('/recommender/recommenderProcess', Recommender)
                              ], debug=True)