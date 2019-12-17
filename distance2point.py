#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 11:59:14 2018

@author: Coral Moreno

Steps in this code:
1. A waypoint is given in (LAT,LONG)
2. Assigning the given waypoint (LAT,LONG) to a GeoPointStamped variable
3. Transforming given WPT from (LAT,LONG) to ECEF reference frame (RF), a.k.a 'earth' RF.
4. Transforming given WPT from 'earth' RF to 'map' RF. 
   'map' is the local reference frame. units: [m]
5. Subscribing for the boat (ASV) position in the map RF
6. Calculating the distance between the ASV and the given WPT in meters  
"""

import rospy
import tf2_ros
import tf2_geometry_msgs 
#from tf2_geometry_msgs import  PointStamped  
from geometry_msgs.msg import  PoseStamped , PointStamped  
from project11_transformations.srv import LatLongToEarth
from geographic_msgs.msg import GeoPointStamped
import numpy as np

LAT = 43.06940#43.071003
LONG = -70.70820#-70.708592

class Dist_to_Point:

	def latlong_to_GeoPointStamped(self,LAT,LONG):
		''' Assigning the given waypoint (LAT,LONG) to a GeoPointStamped variable '''
		# because the message type of the input to the service 'wgs84_to_earth' LatLongToEarth.srv is GeoPointStamp     	
		wpt_latlong = GeoPointStamped() 
	 	#latlong_location.header.frame_id = 'earth' # <-- Don't need it 
		wpt_latlong.position.latitude = LAT
		wpt_latlong.position.longitude = LONG
		#print "Given WPT - LAT,LONG :"
		#print wpt_latlong
		return wpt_latlong

	def boat_map_loc_callback(self,data):
		self.boat_map = data#.pose
		#print "boat location in map reference frame:"
		#print self.boat_map
       
	def LatLong2Earth(self): 
		rospy.wait_for_service('wgs84_to_earth')
		wgs84_to_earth = rospy.ServiceProxy('wgs84_to_earth', LatLongToEarth)
		'''
		Explanation:
		#wpt_earth_temp = PointStamped()    # <-- Not necessary

		For the transformation 'earth' --> 'map' the variable "self.wpt_earth" needs to be of type 
		PoseStamped, while the message type of the output of the service 'wgs84_to_earth' LatLongToEarth.srv 
		is PointStamped. Therefore, the use of a intermediate variable wpt_earth_temp
		'''
		wpt_earth_temp = wgs84_to_earth(self.latlong_to_GeoPointStamped(LAT,LONG))
		# For Degugging - START		
		#print "wpt_earth_temp"
		#print wpt_earth_temp
		# For Debugging - END
		self.wpt_earth.header = wpt_earth_temp.earth.header
		self.wpt_earth.pose.position = wpt_earth_temp.earth.point
		# For Degugging - START
		#print "wpt_earth:"
		#print self.wpt_earth
		# For Degugging - END
		#return wgs84_to_earth(self.latlong_to_GeoPointStamped(LAT,LONG)) # <-- I don't think that it is necessary
		
		 
	def Earth2Map(self):
		self.LatLong2Earth()
		# Get the given waypoint (LAT,LONG) in the map reference frame  
		''' https://answers.ros.org/question/222306/transform-a-pose-to-another-frame-with-tf2-in-python/ '''

		tfBuffer = tf2_ros.Buffer()
		tf_listener = tf2_ros.TransformListener(tfBuffer)
				
		while not tfBuffer.can_transform('map','earth',rospy.Time(0)):
				rospy.sleep(0.2)

		transform = tfBuffer.lookup_transform('map', #target frame
											'earth',#self.wpt_earth.header.frame_id, #'earth', #source frame
											rospy.Time(0), # get the tf at the first available time
											rospy.Duration(1.0)) #wait for 1 sec
		# For Debugging - START
		#print "transformation: earth --> map :"
		#print transform    
		# For Debugging - END

		# For Degugging - START
		#print "Given WPT point in earth RF:"
		#print self.wpt_earth
		# For Degugging - END

		# The given WPT in the 'map' RF:
		self.wpt_map = tf2_geometry_msgs.do_transform_pose(self.wpt_earth,transform)

		# For Degugging - START
		#print "Given WPT point in map RF:"
		#print self.wpt_map
		# For Degugging - END
		    

    
	def distance2point(self):
		self.Earth2Map() 
		
		wpt_map_x = self.wpt_map.pose.position.x	
		wpt_map_y = self.wpt_map.pose.position.y

		#curr_boat_map = self.boat_map
		#curr_boat_map_x = curr_boat_map.pose.position.x
		#curr_boat_map_y = curr_boat_map.pose.position.y
		
		curr_boat_map_x = self.boat_map.pose.position.x
		curr_boat_map_y = self.boat_map.pose.position.y	
		
		self.dist = np.sqrt((curr_boat_map_x-wpt_map_x)**2+(curr_boat_map_y-wpt_map_y)**2) 	
		print "Distance to a waypoint"
		print self.dist
		
		# For Degugging - START
		#print "boat location in map RF:"
		#print self.boat_map

		#print "Given waypoint in map RF:"
		#print self.wpt_map
		# For Degugging - END

   

	def __init__(self):
		rospy.init_node('distance2point', anonymous = False)
		self.boat_map = PoseStamped()  # because this is the type of message in the /position_map topic
		self.wpt_earth = PoseStamped()
		self.wpt_map = PoseStamped()
		
		# get the boat location on the map reference frame
		rospy.Subscriber('/position_map',PoseStamped, self.boat_map_loc_callback) 
		
    
if __name__=='__main__':
	dtp = Dist_to_Point()	
	while not rospy.is_shutdown():
		try:
			dtp.distance2point()
		except rospy.ROSInterruptException:
			pass
    
