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
* currently the waypoint is hardcoded in the code. 
  --> Fix it to read either from command line, or via UDP server.
* Need to publish the distance. Currently it only prints the distance in the Terminal
