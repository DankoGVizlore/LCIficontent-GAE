import os
import xml.etree.ElementTree as ET

import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

from recommenderModels.POImodels import POI


class PoiHandler(webapp2.RequestHandler):

    def insert_item(self, item):
        """
        Inserts a POI item into the data store
        :param item: XML Element with the required fields
        """
        c_name = item.find('name').text
        c_address = item.find('address').text
        c_latitude = item.find('latitude').text
        c_longitude = item.find('longitude').text
        c_open = item.find('open').text
        c_close = ''
        c_website = item.find('website').text
        c_category_id = self.request.get('category_id').encode('utf-8')
        c_description = ''
        c_days = '0'

        ancestor_key = ndb.Key("FIContent_v1", "POI")
        p = POI(parent=ancestor_key, name=c_name, categoryID=int(c_category_id), lat=float(c_latitude),
                lon=float(c_longitude), description=c_description, open=c_open, close=c_close, days=int(c_days),
                address=c_address, website=c_website)
        p.put()

    def get(self):
        """
        Outputs the menu for the XML upload
        """
        path = os.path.join(os.path.dirname(__file__), 'poi_index.html')
        template_values = {}

        self.response.out.write(template.render(path, template_values))

    def post(self):
        """
        Processes the post request and parses the XML.
        """
        xml_raw = self.request.get('xml_input').encode('utf-8')
        root = ET.fromstring(xml_raw)

        items = root.findall("./")

        for item in items:
            self.insert_item(item)

        self.response.out.write('')