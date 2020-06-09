import unittest
from graph import *

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


def djikstra(digraph,start,end):
	#initialize variables
	shortest = {}
	predecessor = {}
	infinity = float('inf')
	path = []
	if start == end:
		return 'You are already here!'
	#get set of nodes
	unseenNodes = digraph.nodes.copy()
	#loop through nodes
	for node in unseenNodes:
		#assign a value of inf to each unvisited node
		shortest[node] = infinity
	#assign a value of 0 to the node start (since we are there)
	shortest[Node(start)] = 0
	#run this loop while unseen nodes in non-empty
	while unseenNodes:
		#initialzie minNode value
		minNode = None
		# iterate through nodes in node list to return the node with the minimum distance from start
		for node in unseenNodes:
			
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
					
			#if the distance + the existing path is less then the distance from the start the thhe previous childnode, thats our new shortest path.
			if total_dst + shortest[minNode] < shortest[Cnode]:
				shortest[Cnode] =  total_dst + shortest[minNode]
				#add to the dict to build a path later
				predecessor[Cnode] = minNode
		#this minNode has now been explored, get rid of it
		unseenNodes.discard(minNode)
	#initialize var
	curNode = Node(end)
	#while were not at the end
	while Node(start) != Node(end):
		try:
			#insert the last node into our path
			path.insert(0,curNode)
			#our next node is the predecessor of our current one
			curNode = predecessor[curNode]
		except KeyError:
			break
	#insert our start


	#if we found a path, give it. 
	if shortest[Node(end)] != infinity:
		return path,shortest[Node(end)]

print(djikstra(load_map('mit_map.txt'),'32','36'))


				
		   
				
