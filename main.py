#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# application url 
# http://lacitadelleingficontent.appspot.com/
#
import webapp2
import httplib2
import logging
import os
import jinja2
import cgi
import urllib
import json
from gcm import GCM
from DevicesModel import DevicesFIContent, DevicesLocationFIContent
# import models for testing ndb
from recommenderModels.categoryModel import *
from recommenderModels.userLocationModel import *
from recommenderModels.POImodels import *
from recommenderModels.likeModel import *
from recommenderModels.userModel import *
from recommenderFunctions.recommenderProcess import *
from recommenderFunctions.recommender_misc import *
from recommenderFunctions.filtering_functions import *

from google.appengine.ext import ndb
from datetime import datetime
from poi_input_handler import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello!')

'''Recommender testing section'''
class RecommenderHandler(webapp2.RequestHandler):
    def get(self):
        
        korisnik = Recommender("f1dankog1")
        ocena = korisnik.get_predicted_ratings()
        l_his = korisnik.get_theta_hist()
        
        k = korisnik.get_cost()
        
        for i in l_his:
            self.response.write( str( i) + "<br>")
            
        self.response.write( "<br> Kostanje je: <br>" )
        for i in k:
            self.response.write( str(i) + "<br>")
            
        self.response.write( " <br> Ocene su: <br>" )
        for oc in ocena:
            self.response.write( str(oc) + "<br>" )
            
        '''
        ancestor_key_POI = ndb.Key("FIContent_v1", "POI")
        ancestor_key_category = ndb.Key("FIContent_v1", "Category")
        ancestor_key_user = ndb.Key("FIContent_v1", "User")
        ancestor_key_like = ndb.Key("FIContent_v1", "Like")
        
        # Deo za punjenje baza
        d = Like(parent = ancestor_key_like,
                POIID = 5478591563300864,
                deviceID = "f1andrejg1",
                viewed = True,
                like  = 2)
        d.put()
        
        # Deo za testiranje funkcijonalnosti
        broj_POI = POI.query(ancestor = ancestor_key_POI).count()
        broj_klasa = Category.query(ancestor = ancestor_key_category).count()     
        
        self.response.write("Broj POIa " + str(broj_POI) + " broj klasa " + str(broj_klasa) + "<br>")
        
        # Nacin na koji mogu povezati unique ID sa njegovim entitetom
        result = POI.query(ancestor = ancestor_key_POI).filter(POI.name == "BUBI").get()
        result_key = result.key.id()
        result = POI.get_by_id(result_key, parent = ancestor_key_POI)   
        '''
        
'''End of recommender testing section'''
#
# FI Content GCM registration handler
# Registration only
# Do not change
class RegHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write('ok')
  def post(self):
    regId = self.request.POST.get('RegId')
    deviceID = self.request.POST.get('DeviceId')
    AppId = self.request.POST.get('AppId')
    
    ancestor_key = ndb.Key("GoExpressContext_v1", "DevicesFIContent")
    device_found = DevicesFIContent.query(ancestor = ancestor_key).filter(DevicesFIContent.reg_id == regId).fetch()
    if not device_found:
      d = DevicesFIContent(parent = ancestor_key,
                    reg_id = str(regId),
                    app_id = str(AppId),
                    device_id = str(deviceID),
                    date = datetime.now()
                    )
      d.put()    
#
# FI Content GCM location handler
# Location only
# Do not change
class LocationHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write('ok')
  def post(self):
    regId = self.request.POST.get('RegId')
    appId = self.request.POST.get('AppId')  
    lat = self.request.POST.get('Lat')
    lon = self.request.POST.get('Lon')
    
    
    ancestor_key = ndb.Key("FIContent_v1", "DevicesLocationFIContent")
    d = DevicesLocationFIContent(parent = ancestor_key,
                  reg_id = str(regId),
                  app_id = str(appId),
                  lat = str(lat),
                  lon = str(lon),
                  date = datetime.now()
                  )
    d.put()
    
    
class DataHandler(webapp2.RequestHandler):
  def get(self):
 
      self.response.write('ok')
  def post(self):
    
    data = self.request.POST.get('data')
    va = json.loads(data)
    
    for i in va:
      devId = i['DevId']
      BSSID = i['BSSID']
      SSID = i['SSID']
      Lat = i['Lat']
      Lon = i['Lon']
      Speed = i['Speed']
      Acc = i['Acc']
      try:
        Time = str(i['Time'])
        t = datetime.strptime( Time, "%Y-%m-%dT%H:%M:%S" )
      except ValueError:
        t = datetime.now()
        
      ancestor_key = ndb.Key("FIContent_v1", "userLocation")
     
      p = userLocation(parent = ancestor_key, 
                  deviceID = str(devId),
                  lat = float(Lat),
                  lon = float(Lon),
                  acc = str(Acc),
                  ssid = str(SSID),
                  bssid = str(BSSID),
                  date = t
                  )
      p.put()
    self.response.write('ok')
    
class ajaxCategoryHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write('ok')
  def post(self):
    ancestor_key = ndb.Key("FIContent_v1", "Category")
    c = Category.query(ancestor=ancestor_key).order(Category.categoryID).fetch()
    data = []
    for i in c:
      data.append({"name" :i.name, "id": i.categoryID})
    jsonData = json.dumps(data)

    self.response.out.write(jsonData)
    
class callPOIHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write( " Ok ") 
    def post(self):
        cat = self.request.POST.get('cat')  
        lat = self.request.POST.get('lat')
        lon = self.request.POST.get('lon')
        devID = self.request.POST.get('devID')
        
        ancestor_key_POI = ndb.Key("FIContent_v1", "POI")    
        ancestor_key_like = ndb.Key("FIContent_v1", "Like")
        #Something new is happening around the corner
        data = []
        try:
            cat = int(cat)
        except ValueError:
            cat = 0    
        
        if cat != 0:                  
            points = POI.query(ancestor = ancestor_key_POI).filter(POI.categoryID == cat).fetch()
            
            for point in points:
                user_like = Like.query(ancestor = ancestor_key_like).filter(Like.POIID == point.key.id()).filter(Like.deviceID == devID).fetch()
                
                if user_like == []:
                    data.append({"name": point.name ,"lat" :point.lat, "lon": point.lon, "desc": point.description, "poiId": point.key.id(), "media": point.website, "cat": point.categoryID, 'like': 1, 'viewed':False })
                else:
                    data.append({"name": point.name ,"lat" :point.lat, "lon": point.lon, "desc": point.description, "poiId": point.key.id(), "media": point.website, "cat": point.categoryID, 'like': user_like[0].like, 'viewed':user_like[0].viewed })
            
        else:
            # Here we call recommender functions to get recommendation data. And then filter POIs, using activity and GPS coordinates.
            user_data = Recommender( devID )
            logging.info(user_data)
            user_recommended_ratings = user_data.get_predicted_ratings()
            logging.info(user_recommended_ratings)
                        
            # Here we call activity recognition function. Standing 200m / Walking 800m / Transportation 1800m
            user_activity = activity( devID ) 
            #user_activity = ( 0, "caffe" )
            activity_radius = ( ( user_activity[0] + 1) ** 2 ) * 200  
            
            # Here we go trough sorted recommender ratings and then search for elements that are in given radius and pack them.
            list_of_interesting = get_list_of_sorted_poi(user_recommended_ratings, activity_radius, float(lat), float(lon))
            
            logging.info(list_of_interesting)
            size_of_list = len( list_of_interesting )
            
            number_of_recommended_POIs = 5
            if ( size_of_list - number_of_recommended_POIs - 1 > 0):
                end_index = size_of_list - number_of_recommended_POIs - 1
            else:
                end_index = 0
                
            for i in range( size_of_list - 1, end_index, -1 ):
                POI_key = list_of_interesting[i - 1][0].key.id()
                point = POI.get_by_id(POI_key, parent = ancestor_key_POI)
                user_like = Like.query(ancestor = ancestor_key_like).filter(Like.POIID == POI_key).filter(Like.deviceID == devID).fetch()
                                    
                if user_like == []:
                    data.append({"name": point.name ,"lat" :point.lat, "lon": point.lon, "desc": point.description, "poiId": POI_key, "media": point.website, "cat": point.categoryID, 'like': 1, 'viewed':False })
                else:
                    data.append({"name": point.name ,"lat" :point.lat, "lon": point.lon, "desc": point.description, "poiId": POI_key, "media": point.website, "cat": point.categoryID, 'like': user_like[0].like, 'viewed':user_like[0].viewed })
        
        jsonData = json.dumps(data)
        self.response.out.write(jsonData)
    
class ajaxViewedHandler(webapp2.RequestHandler):
  def get(self):
    """
    ancestor_key = ndb.Key("FIContent_v1", "Like")
      
    c = Like.query(ancestor=ancestor_key).fetch()
    data = []
    for i in c:
      data.append({"POIID" :i.POIID, "id": i.deviceID, "like": i.like})
      
    jsonData = json.dumps(data)

    self.response.out.write(jsonData)
    """
    self.response.write('ok')
    
  def post(self):
    devID = self.request.POST.get('devID')
    poiID = self.request.POST.get('id')
    
    ancestor_key = ndb.Key("FIContent_v1", "Like")
    L = Like(parent = ancestor_key, 
                  POIID = int(poiID),
                  deviceID = int(devID),
                  viewed = True,
                  like = 1
                  )

    L.put()
    
    
class ajaxLikeHandler(webapp2.RequestHandler):
  def post(self):
    devID = self.request.POST.get('devID')
    poiID = self.request.POST.get('id')
    like = self.request.POST.get('value')
    
    ancestor_key = ndb.Key("FIContent_v1", "Like")
    
    like_found = Like.query(ancestor = ancestor_key).filter(Like.POIID == int(poiID)).filter(Like.deviceID == devID).fetch()
    if like_found:
      like_found[0].like = int(like)
      like_found[0].put()
      self.response.write('ok')
    else:
      L = Like(parent = ancestor_key, 
                    POIID = int(poiID),
                    deviceID = devID,
                    viewed = True,
                    like = int(like)
                    )
  
      L.put()
      self.response.write('ok')
    
class likeDislikeHandler(webapp2.RequestHandler):
  def post(self):
    devID = self.request.POST.get('devID')
    poiID = self.request.POST.get('id')
    value = self.request.POST.get('value')
    
    
    self.response.write('ok')
    
class addCategoryHandler(webapp2.RequestHandler):
  def get(self):
    ID = self.request.GET.get('id') 
    name = self.request.GET.get('name') 
    
    ancestor_key = ndb.Key("FIContent_v1", "Category")
    p = Category(parent = ancestor_key, 
                  categoryID = int(ID),
                  name = str(name)
                  )

    p.put()
    
    self.response.write(ID)

# This handler is called when user opens a POI popup
class POIviewedHandler(webapp2.RequestHandler):
  def post(self):
    devID = self.request.POST.get('devID')
    poiID = self.request.POST.get('id')
    
    ancestor_key = ndb.Key("FIContent_v1", "Like")
    
    like_found = Like.query(ancestor = ancestor_key).filter(Like.POIID == int(poiID)).filter(Like.deviceID == devID).fetch()
    if like_found:
      self.response.write('ok')
    else:
      L = Like(parent = ancestor_key, 
                    POIID = int(poiID),
                    deviceID = devID,
                    viewed = True,
                    like = int(1)
                    )
  
      L.put()
      self.response.write('ok')
      
class activityHandler(webapp2.RequestHandler):
    def post(self):
        devID = self.request.POST.get('devID')    
        p_activity = {-1:"NOT ENOUGH DATA", 0:"STANDING", 1:"WALKING",2:"TRANSPORT"}
        user_activity = activity( devID ) 
        self.response.write( p_activity[user_activity[0]] )
        
# test handler for geting GCM regId
class postregidHandler(webapp2.RequestHandler):
        
    def post(self):
        RegId = self.request.POST.get('RegId')
        devID = self.request.POST.get('DeviceID')
        
        ancestor_key = ndb.Key("FIContent_v1", "User")
        user_found = User.query(ancestor = ancestor_key).filter(User.GCMRegID == RegId).filter(User.deviceID == devID).fetch()
        
        if user_found:
          logging.info('user GCM reg id has been found')
        else:
          u = User(parent = ancestor_key, 
                        GCMRegID = RegId,
                        deviceID = devID
                        )
          u.put()  
        
    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/reg', RegHandler),
    ('/loc', LocationHandler),
    ('/data', DataHandler),
    ('/ajaxCategory', ajaxCategoryHandler),
    ('/ajaxViewed', ajaxViewedHandler),
    ('/ajaxLike', ajaxLikeHandler),
    ('/recommender', RecommenderHandler),
    ('/callPOI', callPOIHandler),
    ('/addCat', addCategoryHandler),
    ('/likeDislike', likeDislikeHandler),
    ('/POIviewed', POIviewedHandler),
    ('/poi_input', PoiHandler),
    ('/postregid', postregidHandler),
    ('/callAct', activityHandler)], debug=True)
