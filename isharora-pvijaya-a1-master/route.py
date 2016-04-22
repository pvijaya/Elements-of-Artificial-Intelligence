# code goes here
#!/usr/bin/python
'''
Report on the code below:

This is basically an implementation to find the path between two given cities on the map.
It has the implementation of Breadth First Search , Depth First Search and A* algorithm
While implementing BFS and DFS we do not consider the cost associated with each edge between the
two nodes(cities) as these algorithms are the Blind Search techniques which will simply give the first
path that is found via the algorithm.

If we try to include the cost of each edge from one city to another, starting from the start city to 
the end city, then the algorithm will be called Dijkastra's algorithm.

In Dijkastra's, we consider the cost associated with each child of the node and the best path is choosen 
based on the cost. This is not implemented as part of this assignment.

For A* algorithm, we have considered three different routing options like distance, time and number of turns
between two nodes(which is the length of the path between two nodes)

In case of distance:

	We have considered the distance in miles from one city to another.
	
In case of time:

	We have considered the time taken to travel from one city to another (t = D/s using the given distance and speed values)

In case of segments:

	We have considered 1 for each turn(highway) coming between two cities.
	
For heuristic:

	In case of distance, we have considered two options for calculating heuristics, 
		1. Using the euclidean distance between the two latitude and longitude points
		2. Using the great circle distance between the two latitude and longitude points of two cities.
			This is considered to be a better heuristic as when the path is long between the two cities then the cities cannot be taken to be on a plane.
			As the Earth is spherical,so for longer distances between two points it will not be a plane.
			
	In case of time, the heuristics is calculated using the great circle distance and the average speed of all the speeds given in the road-segments.txt file.
		so, the h value becomes (Great Circle Distance/Average Speed)
		
	In case of segments, there is no need to estimate the heuristics as for taking a turn we cannot do it in less than 1 for each highway.
	
Out of all these three algorithms implemented, A* gives the better results as it is considering the costs. But we cannot say it is optimal in terms of the number of turns.
It is best in terms of the distance. For time as it uses the average speed, it can or cannot be exactly equivalent to the optimal cost.

I have used one package from online, for using the priority queue function from that for sorting the f values in A* algorithm.
This package is imported into this code and will be submitted as a separate file to be included in the folder before running the code.

here is the reference for the same:
http://pydoc.net/Python/pqdict/0.5/pqdict/

Only the PQDict function is used from this file.

Other references:

https://docs.python.org
https://stackoverflow.com
http://www.tutorialspoint.com/
https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

Sample command for running the code:

python route.py "Anaconda,_Montana" "Crackerville,_Montana" time astar
'''

from collections import deque
from collections import defaultdict
from operator import is_not
from functools import partial
from pqdict import PQDict

import fileinput
import re
import math
import time
import getopt, sys

'''
Class for the city to store all the variables associated with one city including the inedges, outedges
'''
class City:

		#initialization function for City class
		def __init__(self,name,latitude,longitude):
			self.name = name
			self.latitude = latitude
			self.longitude = longitude
			self.inEdges = []
			self.outEdges = []
		
		#method to add the highway to the city
		def addHighway(self,name,speed,miles,city2):
			h = Highway(name,speed,miles,self,city2)
			if h is not None:
				self.outEdges.append(h)
				city2.inEdges.append(h)
		
		#getter method to obtain the city name
		def get_cityname(self):
			return self.name
		
		#getter method to obtain the latitude value of the city
		def get_latitude(self):
			return self.latitude
		
		#getter method to obtain the longitude value of the city
		def get_longitude(self):
			return self.longitude
		
		#method to fetch the in-edges(in-highways) of a city
		def get_inEdges(self):
			filter(partial(is_not, None), self.inEdges)
			return self.inEdges
		
		#method to fetch the out-edges(out-highways) of a city
		def get_outEdges(self):
			filter(partial(is_not, None), self.outEdges)
			return self.outEdges

'''
Highway class to store the values from road-segments file and add the corresponding cities between each highway
'''			
class Highway:
		#initialization method for highway class
		def __init__(self,name,speed,miles,start,end):
			self.name = name
			self.speed = speed
			self.miles = miles
			self.start = start
			self.end = end
		
		#getter method to obtain the highway name
		def get_highwayname(self):
			return self.name
		
		#getter method to obtain the speed of the highway
		def get_speed(self):
			return self.speed
		
		#getter method to obtain the miles associated with a highway between two cities
		def get_miles(self):
			return self.miles
		
		#getter to obtain the start city of a highway
		def get_highway_start(self):
			return self.start
		
		#getter method to obtain the end city of a highway
		def get_highway_end(self):
			return self.end

			
'''
Graph class for creating the graph using the cities and the highways and containing the bfs,dfs and a-star algorithms
'''
class Graph:
	
	#initialization function for Graph class
	def __init__(self):
		
		self.cities = {}
		self.avg_speed = 0
		self.total_speed = 0
		self.num_lines = 0
		
		
		#fetching cities from city-gps file and adding them to the City class
		with open('city-gps.txt','r') as fp:
			for row in fp:
				self.cities[row.split()[0]] = City(row.split()[0],row.split()[1],row.split()[2])
		
		
		#fetching the details from road-segments.txt file and adding the details to the Highway class
		# Here, if a highway does not have speed, then I am assuming speed to be 0.00 and adding the same for that highway object
		with open('road-segments.txt','r') as f:
			for i, line in enumerate(f,1):
				newline = re.sub(' ', '#', line.rstrip())
				k = newline.split("#")
				if not k[3]:
					k[3] = '0.00'
				newl = ' '.join(k)
				if(newl.split()[0] not in self.cities.keys()):
					self.cities[newl.split()[0]] = City(newl.split()[0],0.0,0.0)
				if(newl.split()[1] not in self.cities.keys()):
					self.cities[newl.split()[1]] = City(newl.split()[1],0.0,0.0)
				self.cities[newl.split()[0]].addHighway(newl.split()[4],newl.split()[2],newl.split()[3],self.cities[newl.split()[1]])
				self.total_speed =  self.total_speed + float(newl.split()[3])
				if(float(newl.split()[3]) != 0.00):
					self.num_lines = self.num_lines + 1
					
		#calculating the average speed of all the speeds in the road-segments file, to be used for heuristic function
		self.avg_speed = self.total_speed / self.num_lines
		
	
	
	#method to print the output of the algo in the end and also to print the path for each algorithm
	def bfs_short_path(self, parent_nodes, start_city, end_city):
		path = [[end_city,None]]
		end = end_city
		finalpath = []
		while end != start_city:
			next = parent_nodes[end]
			path.append(next)
			end = parent_nodes[end][0]
		
		for i in reversed(path):
			finalpath.append(i)
		
		totaldistance = 0
		totaltime = 0 
		
		for i in range(len(finalpath)):
			highway_route = finalpath[i]
			if(highway_route[1] and highway_route):
				
				if(float(highway_route[1].get_speed()) != 0):
					time = float(highway_route[1].get_miles())/float(highway_route[1].get_speed())
				else:
					time = 0
					print "PATH HAS UNDEFINED SPEEDS AND TIME HAS BEEN CONSIDERED 0 NOT THAT PATH"
				print "city:",highway_route[1].get_highway_start().get_cityname(),"time:",time,"distance:",highway_route[1].get_miles(),"Highway name:",highway_route[1].get_highwayname()
				totaldistance = totaldistance + float(highway_route[1].get_miles())
				totaltime = totaltime + time
				
		print "end city:",end_city
		print "last line:"
		lastline= str(totaldistance)  + " " +str(totaltime) 
		for i in range(len(finalpath)):
			highway_route = finalpath[i]
			if(highway_route[1]):
				lastline = lastline +" " + highway_route[1].get_highway_start().get_cityname()
		lastline = lastline+" "+end_city
		print "length of path taken is" , len(path)
		print lastline
		return

	
	#method to implement bfs algorithm, this algorithm doesn't consider the cost associated with any highway
	def bfs(self, start_city, end_city2):
		print "Calling bfs algorithm"
		if start_city not in self.cities.keys():
			print "start city is not present, enter a valid city name like  eg: Austintown,_Ohio"
			sys.exit()
			
		highway_object = {}
		parent_nodes = {}
		visited = set()
		q = deque()
		q.append(start_city)	
			
		#iterating throught the queue to find the path
		while q:
			next = q.popleft()
			if(next == end_city2):
				self.bfs_short_path(parent_nodes, start_city, end_city2)
				return 1
			if(next not in visited):
				visited.add(next)
				l = self.cities[next].get_outEdges()
				filter(partial(is_not, None), l)
				for x in range(len(l)):
					temp_end_city = l[x].get_highway_end().get_cityname()
					parent_nodes[temp_end_city] =  [next,l[x]]
					q.append(temp_end_city)
		return 0
	
	
		
	#method to implement the dfs algorith on the graph
	def dfs(self, start_city, end_city):
		print "Calling dfs algorithm"
		parent_nodes = {}
		visited = []
		s = []
		s.append(start_city)
		
		while s:
			next = s.pop()
			if(next == end_city):
				self.bfs_short_path(parent_nodes, start_city, end_city)
				return 1
			if(next not in visited):
				visited.append(next)
				l = self.cities[next].get_outEdges()
				filter(partial(is_not, None), l)
				for x in range(len(l)):
					temp_end_city = l[x].get_highway_end().get_cityname()
					parent_nodes[temp_end_city] = [next,l[x]]
					s.append(temp_end_city)
		return 0
	
	#method to calculate the heuristic using the euclidean distance between the two latitude and longitude combination of the cities passed
	def heuristic_cal(self, start_city, end_city):
		x1 = math.ceil((float(self.cities[start_city].get_latitude())*100)/100)
		y1 = math.ceil((float(self.cities[start_city].get_longitude())*100)/100)
	
		x2 = math.ceil((float(self.cities[end_city].get_latitude())*100)/100)
		y2 = math.ceil((float(self.cities[end_city].get_longitude())*100)/100)
	
		X = (x2-x1)*(x2-x1)
		Y = (y2-y1)*(y2-y1)
		return math.sqrt(X+Y)
		
	'''
	reference : https://en.wikipedia.org/wiki/A*_search_algorithm
				http://www.movable-type.co.uk/scripts/latlong.html
	
	method to calculate the heuristic using great circle distance using haversine formula 
	between the two latitude and longitude points as Earth is a sphere and Euclidean distance works well if we have a plane not the spehere.
	'''
	
	def great_circle_distance(self, start_city, end_city):
		
		R = 6371000
		
		X1 = math.radians(float(self.cities[start_city].get_latitude()))
		
		Y1 = math.radians(float(self.cities[start_city].get_longitude()))
		
		X2 = math.radians(float(self.cities[end_city].get_latitude()))
		
		Y2 = math.radians(float(self.cities[end_city].get_longitude()))
		
		delX = math.radians(float(self.cities[end_city].get_latitude()) - float(self.cities[start_city].get_latitude()))
		
		delY = math.radians(float(self.cities[end_city].get_longitude()) - float(self.cities[start_city].get_longitude()))
		
		a = math.sin(delX/2) * math.sin(delX/2) + math.cos(X1)*math.cos(X2)*math.sin(delY/2)* math.sin(delY/2)
		
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));

		distance = R * c
		
		#converting the distance to miles
		distance = distance * 0.000621371
		
		return distance
		
	
	'''
	reference : https://en.wikipedia.org/wiki/A*_search_algorithm
	
	'''
	#method to implement a star algorithm
	def a_star_algo(self, start_city, end_city, routing_option):
		print "calling a-star algorithm"
		close = set()
		open = set()
		open.add(start_city)
		parent = {}
		
		g_score = defaultdict(lambda: math.inf)
		g_score[start_city] = 0
		
		# PQDict is a function imported from a code found online.
		# reference : http://pydoc.net/Python/pqdict/0.5/pqdict/
		
		f_score = PQDict.minpq()
		
		if routing_option == "distance":
			f_score[start_city] =  g_score[start_city] + self.great_circle_distance(start_city, end_city)
		elif routing_option == "segments":
			f_score[start_city] =  g_score[start_city]
		elif routing_option == "time":
			f_score[start_city] =  g_score[start_city] + self.great_circle_distance(start_city, end_city)/self.avg_speed
		
		while open:
			temp_current = f_score.pop()
			current = temp_current
			
			if current == end_city:
				self.bfs_short_path(parent,start_city, end_city)
				return 1
				
			if current in open:
				open.discard(current)
			close.add(current)
			
			
			l = self.cities[current].get_outEdges()
			for x in range(len(l)): 
				temp_city = l[x].get_highway_end().get_cityname()
				if temp_city in close:
					continue
				
				# if requested for miles
				if routing_option == "distance":
					new_g_value = g_score[current] + int(l[x].get_miles())
				# if requested for segments
				elif routing_option == "segments":
					new_g_value = g_score[current] + 1
				# if requested for time
				elif routing_option == "time":
					dis = int(l[x].get_miles())
					speed = int(l[x].get_speed())
					new_g_value = g_score[current] + int(dis/speed)
				
				if temp_city not in open or new_g_value < g_score[temp_city]:
					parent[temp_city] = [current,l[x]]
					g_score[temp_city] = new_g_value
					if routing_option == "distance":
						f_score[temp_city] = g_score[temp_city] + self.great_circle_distance(temp_city,end_city)
					elif routing_option == "segments":
						f_score[temp_city] =  g_score[temp_city]
					elif routing_option == "time":
						f_score[temp_city] =  g_score[temp_city] + self.great_circle_distance(temp_city, end_city)/self.avg_speed
					if temp_city not in open:
						open.add(temp_city)
		return 0
		
	
#main method to parse the command line arguments and call the desired algo
def main():
	start_city = sys.argv[1]
	end_city = sys.argv[2]
	routing_option = sys.argv[3]
	routing_algo = sys.argv[4]
	a = Graph()
	
	#check to find out the number of arguments entered via command line
	if len(sys.argv) != 5:
		print "Valid number of inputs like python route.py [start-city] [end-city] [routing-option] [routing-algorithm]"
		sys.exit()
	
	#check to find whether the entered start city is in the file parsed or not
	if(a.cities.get(start_city) is None):
		print "entered start city is not present in the roadmap"
		sys.exit()
	
	#check to find whether the entered end city is in the file parsed or not
	if(a.cities.get(end_city) is None):
		print "entered end city is not present in the roadmap"
		sys.exit()
	
	#calling the requested graph algorithm
	if(routing_algo == "bfs"):
		
		z = a.bfs(start_city,end_city)
		if z == 0:
			print "no path exists"
		
	elif(routing_algo == "dfs"):
		
		y = a.dfs(start_city,end_city)
		if y == 0:
			print "no path exists"
		
	elif(routing_algo == "astar"):
		
		x = a.a_star_algo(start_city,end_city, routing_option)
		if x == 0:
			print "no path exists"
		
	else:
		print "Enter valid routing algorithm name"
		sys.exit()
	
main()	
		
		