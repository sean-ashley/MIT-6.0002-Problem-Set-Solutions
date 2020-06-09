# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import *
import time
#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
	"""
	Parses the map file and constructs a directed graph

	Parameters:
		map_filename : name of the map file

	Assumes:
		Each entry in the map file consists of the following four positive
		integers, separated by a blank space:
			From To TotalDistance DistanceOutdoors
		e.g.
			32 76 54 23
		This entry would become an edge from 32 to 76.

	Returns:
		a Digraph representing the map
	"""

	print("Loading map from file...")
	mit_map = open(map_filename,'r')
	mit_map_lines = mit_map.readlines()
	digraph = Digraph()
	for line in mit_map_lines:
	   stripped_line = line.rstrip("\n")
	   split_line = stripped_line.split()
	   src = Node(split_line[0])
	   dest = Node(split_line[1])
	   edge = WeightedEdge(src,dest,split_line[2],split_line[3])
	   if digraph.has_node(dest) and digraph.has_node(src):
		   digraph.add_edge(edge)
	   elif digraph.has_node(dest) is False and digraph.has_node(src):
		   digraph.add_node(dest)
		   digraph.add_edge(edge)
	   elif digraph.has_node(dest)  and digraph.has_node(src) is False:
		   digraph.add_node(src)
		   digraph.add_edge(edge)
	   else:
		   digraph.add_node(src)
		   digraph.add_node(dest)
		   digraph.add_edge(edge)

	return digraph

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#

# Problem 3b: Implement get_best_path
#uses djikstras algorithm implementation. Inspired from code seen in video : https://www.youtube.com/watch?v=IG1QioWSXRI&t=424s
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
				  best_path,max_total_dist):
	"""
	Finds the shortest path between buildings subject to constraints.

	Parameters:
		digraph: Digraph instance
			The graph on which to carry out the search
		start: string
			Building number at which to start
		end: string
			Building number at which to end
		path: list composed of [[list of strings], int, int]
			Represents the current path of nodes being traversed. Contains
			a list of node names, total distance traveled, and total
			distance outdoors.
		max_dist_outdoors: int
			Maximum distance spent outdoors on a path
		best_dist: int
			The smallest distance between the original start and end node
			for the initial problem that you are trying to solve
		best_path: list of strings
			The shortest path found so far between the original start
			and end node.

	Returns:
		A tuple with the shortest-path from start to end, represented by
		a list of building numbers (in strings), [n_1, n_2, ..., n_k],
		where there exists an edge from n_i to n_(i+1) in digraph,
		for all 1 <= i < k and the distance of that path.

		If there exists no path that satisfies max_total_dist and
		max_dist_outdoors constraints, then return None.
	"""
   
#initialize variables
	shortest = {}
	shortest_out = {}
	predecessor = {}
	infinity = float('inf')
	best_path = []
	if start == end:
		return 'You are already here!'
	#get set of nodes
	unexploredNodes = digraph.nodes.copy()
	#loop through nodes
	for node in unexploredNodes:
		#assign a value of inf to each unvisited node
		shortest[node] = infinity
	#assign a value of 0 to the node start (since we are there)
	shortest[Node(start)] = 0
	shortest_out[Node(start)] = 0
	#run this loop while unseen nodes in non-empty
	while unexploredNodes:
		#initialzie minNode value
		minNode = None
		# iterate through nodes in node list to return the node with the minimum distance from start
		for node in unexploredNodes:
			
			#if its the first run thru, node is the min node
			if minNode is None:
				
				minNode = node
			#otherwise take the smallest distance
			elif shortest[node] < shortest[minNode]:
				minNode = node
				
		#iterate through children of the current node we are one (minNode)
		for Cnode in digraph.childrenOf(minNode):
			#match edge to nodes
			for i in digraph.get_edge_list():
				if i.src == minNode and i.dest == Cnode:
					
					#gives distance from minNode to childNode
					total_dst = int(i.get_total_distance())
					total_out = int(i.get_outdoor_distance())
			#if the distance from the parent node to the childnode + the existing path is less then the distance from the start to the the previous childnode, thats our new shortest path.
			if total_dst + shortest[minNode] < shortest[Cnode]:
				shortest[Cnode] =  total_dst + shortest[minNode]
				shortest_out[Cnode] = total_out + shortest_out[minNode]
				#add to the dict to build a path later
				predecessor[Cnode] = minNode
		#this minNode has now been explored, get rid of it
		unexploredNodes.discard(minNode)
	#initialize var
	curNode = Node(end)
	#while were not at the end
	while Node(start) != Node(end):
		try:
			#insert the last node into our path
			best_path.insert(0,curNode)
			#our next node is the predecessor of our current one
			curNode = predecessor[curNode]
		except KeyError:
			break


	#if we found a path, give it. 
	if shortest[Node(end)] != infinity:
		#if they meet our distance constraints
		if shortest[Node(end)] <= max_total_dist and shortest_out[Node(end)] <= max_dist_outdoors:
			best_dist = shortest[Node(end)]
			path = [best_path,best_dist]
			return best_path,shortest[Node(end)]
		else:
			return None
	else:
		raise ValueError('No path meets these requirements.')

					
					





# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
	"""
	Finds the shortest path from start to end using a directed depth-first
	search. The total distance traveled on the path must not
	exceed max_total_dist, and the distance spent outdoors on this path must
	not exceed max_dist_outdoors.

	Parameters:
		digraph: Digraph instance
			The graph on which to carry out the search
		start: string
			Building number at which to start
		end: string
			Building number at which to end
		max_total_dist: int
			Maximum total distance on a path
		max_dist_outdoors: int
			Maximum distance spent outdoors on a path

	Returns:
		The shortest-path from start to end, represented by
		a list of building numbers (in strings), [n_1, n_2, ..., n_k],
		where there exists an edge from n_i to n_(i+1) in digraph,
		for all 1 <= i < k

		If there exists no path that satisfies max_total_dist and
		max_dist_outdoors constraints, then raises a ValueError.
	"""
	if get_best_path(digraph,start,end,[],max_dist_outdoors,None,None,max_total_dist) == None:
		raise ValueError("No solution, constraints breached")
	else:
		return get_best_path(digraph,start,end,[],max_dist_outdoors,None,None,max_total_dist)[0]






