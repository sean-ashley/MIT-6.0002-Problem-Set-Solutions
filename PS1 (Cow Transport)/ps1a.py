###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
from collections import OrderedDict

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    #open file and read the lines
    data = open(filename,'r')
    data_lines = data.readlines()
    #initialize empty dict
    cows = {}
    #iterate thru lines
    for line in data_lines:
        #split on comma and new line to isolate name and weight.
        line = line.split(',')
        weight = line[1].split('\n')
        #create dict
        cows[line[0]] = int(weight[0])
    return cows



# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #initialize trips list
    trips = []
    #create a copy of our dict
    cows_copy = cows.copy()
    #sort that dict in ascending value order
    cows_copy = OrderedDict(sorted(cows_copy.items(), key=lambda t: 1/t[1]))
    #get a list of the names in the proper order
    cow_names = list(cows_copy.keys())
    #initialze counter,weight,and trip list
    i = 0
    cur_weight = 0
    trip = []
    #while cow_names is non-empty
    while cow_names:
        try:
            #if it would go over our weight, skip it
            if cows_copy[cow_names[i]] + cur_weight > limit:
                i += 1
            #itherwise add it, add to our current weight, and delete the name from the list
            else:
                trip.append(cow_names[i])
                cur_weight +=  cows_copy[cow_names[i]]
                del cow_names[i]
                i += 1
        #if we reach the end of the list, jump back to the start and reset everything
        except:
            trips.append(trip)
            i = 0
            trip = []
            cur_weight = 0
            continue
    return trips



# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #create a copy of the dict
    cows_copy = cows.copy()
    #get the names of the cows
    cow_names = cows_copy.keys()
    #create a generator object from the names
    partitioned_list = get_partitions(cow_names)
    #set up variables for alter
    min_length = float('inf')
    cur_weight = 0
    best_trips = []
    #loop through trip lists in partitioned list
    for partition in partitioned_list:
        #set the count to 0 
        count = 0
        
        #loop through each trip in the trip list
        for trip in partition:
            #reset weight for new trip
            cur_weight = 0
            #loop thru each cow
            for cow in trip:
                #if the current weight + cow weight is less or equal to the limit, add that weight ot our current weight
                if cur_weight + cows_copy[cow] <= limit:
                    cur_weight += cows_copy[cow]
                #otherwise change count and break out of loop
                else:
                    count = 1
                    break
        #if the count is not 1 (AKA we made it to the end of the loop) and the length of the trip list is less the our min length, thats our new best trip list.
        if count != 1 and len(partition) < min_length:
            min_length = len(partition)
            best_trips = partition
    return best_trips

            



    

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    #time the greedy algorithm
    greedy_t0 = time.time()
    return_val = greedy_cow_transport(load_cows('ps1_cow_data.txt'))
    greedy_t1 = time.time()
    #get the amount of time it takes
    greedy_t = greedy_t1 - greedy_t0
    #print time and num or trips
    print('Greedy takes ' + str(greedy_t) + ' seconds and the number of trips is ' + str(len(return_val)))
    #repeat for brute force algo
    brute_t0 = time.time()
    return_val = brute_force_cow_transport(load_cows('ps1_cow_data.txt'))
    brute_t1 = time.time()

    brute_t = brute_t1 - brute_t0

    print('Brute force takes ' + str(brute_t) + ' seconds and the number of trips is ' + str(len(return_val)))




