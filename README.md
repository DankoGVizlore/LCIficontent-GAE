LCIficontent-GAE
================

#Server/cloud part of LCI Context Aware Recommendation demo application

Server side application comprises the following modules:
- activity recognition
- recommender service 
- filtering module
- supporting database

## Activity recognition
In order to recognise corresponding activity, application uses the last two stored GPS coordinates and previous activity. By using the coordinates, module can calculate the speed. Based on calculated speed and previous activity, it presumes what is the current user activity. There are three possible activities currently available: 
- standing
- walking
- transportation

Server side application is also collecting data related to WiFi networks. If the device is using a WiFi, activity recognition module can read the SSID of the current WiFi network. If there are some known patterns of SSID name, module recognizes it. 

This module returns two information:
- what is the recognised/predicted activity
- recognised location ( restaurant, hotel, cafe, etc. ) by using SSID. 

Output from activity recognition module is represented as tuple in Python ( activity, location )
Additional sensors and activity classes will be added.

## Recommender service
Recommender service is implemented using content based filtering with VizLore properietary recommendation engine (source code not provided). The final version of the Context Aware Recommendation solution will utilize the Recommendation as a Service SE from the FIC2 project.

## Filtering module
Filtering module uses table of predicted ratings provided by recommender service and predicted activity provided by activity recognition service. When some device sends request for recommendation, mobile application expect five recommended POIs. To filter out only five POIs, this module sorts the POIs based on their predicted ratings. Based on current activity, module use some radius in which it recommends POIs ( standing-200m, walking-400m, using transportation-1800m). POIs which are not in this radius are strpiped. Finally, from the remaining POIs module returns five with best predicted ratings. This module can be used with custom recommender systems and will be used with the Recommender as a Service SE.

## Supporting database
Server side uses custom POI database. This database represent POIs from the city of Novi Sad. It's used to represent how the server side application should work after integration with the POIproxy SE.


