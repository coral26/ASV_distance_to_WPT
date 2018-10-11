# ASV_distance_to_WPT
A ROS node that calculated the distance of the ASV to a given waypoint.

Steps in this code:
1. A waypoint is given in (LAT,LONG)
2. Assigning the given waypoint (LAT,LONG) to a GeoPointStamped variable
3. Transforming given WPT from (LAT,LONG) to ECEF reference frame (RF), a.k.a 'earth' RF.
4. Transforming given WPT from 'earth' RF to 'map' RF. 
   'map' is the local reference frame. units: [m]
5. Subscribing for the boat (ASV) position in the map RF
6. Calculating the distance between the ASV and the given WPT in meters  


TO DO:
* Make this node to calculate distance AND bearing to a given waypoint.
* currently the waypoint is hard-coded in the code.

  --> Fix it to read either from command line, or via UDP server.
      Implement 3 different ways to read a given waypoint: 
  1. Service that gets the wypoint and set it in the code.
  2. via the Parameter Server
  3. via a rostopic.
      
  --> For this need to write something that publish the waypointor a list of waypoints; or try via command-line.
      
* Need to publish the distance. Currently it only prints the distance in the Terminal.
  Make the node to send distance AND bearing via both a service and a publisher. 
  
  --> will have to write a custom message (with a header, i.e. stamped) , unless there is a suitable existing message (need to check).

