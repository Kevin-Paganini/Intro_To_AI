#
# CS2400 Introduction to AI
# rat3.py
#
# Spring, 2022
#
# Author: [TODO: YOUR NAME HERE]
#
# Stub class for Lab 2 
# This class creates a Rat agent to be used to explore a Dungeon
# 
# Note: Instance variables with a single preceeding underscore are intended 
# to be protected, so setters and getters are included to enable this convention.
#
# Note: The -> notation in the function definition line is a type hint.  This 
# will make identifying the appropriate return type easier, but they are not 
# enforced by Python.  
#

from dungeon3 import Dungeon, Room, Direction
from node3 import Node
from typing import *

#max depth for iterative deepening
MAX_DEPTH = 1000

class Rat:
    """Represents a Rat agent in a dungeon. It enables navigation of the 
    dungeon space through searching.

    Attributes:
        dungeon (Dungeon): identifier for the dungeon to be explored
        start_location (Room): identifier for current location of the rat
    """
    def __init__(self, dungeon: Dungeon, start_location: Room):
        """ This constructor stores the references when the Rat is 
        initialized. """
        self._dungeon = dungeon
        self._start_location = start_location
        self._self_rooms_searched = False

    @property
    def dungeon(self) -> Dungeon:
        """ This function returns a reference to the dungeon.  """
        return self._dungeon

    def set_echo_rooms_searched(self) -> None:
        """ The _self_rooms_searched variable is used as a flag for whether
        the rat should display rooms as they are visited. """
        self._self_rooms_searched = True

    def directions_to(self, target_location: Room, algorithm: str) -> List[str]:
        """ This function returns a list of the names of the rooms from the
        start_location to the target_location. """
        return self.path_to(target_location, algorithm)

    def path_to(self, target_location: Room, algorithm: str) -> List[Room]:
        """ This function finds and returns a list of Rooms from
        start_location to target_location. It first calls one of
        listed search algorithms and obtains either a Node if a path
        to the target was found or None. If found_node is not None,
        it then traces up the search tree using Node.parent in order to
        reconstruct the path of Rooms. It then returns that list of Rooms"""
        if algorithm == 'd':
            found_node = self.depth_first_search(target_location)
        elif algorithm == 'b':
            found_node = self.breadth_first_search(target_location)
        elif algorithm == 'i':
            found_node = self.iterative_deepening(target_location)
        elif algorithm == 'a':
            found_node = self.astar(target_location)
        else:
            print("Invalid algorithm code: " + algorithm)
            found_node = None

        ret = []
        current = found_node
        while current is not None:
            ret.append(current.state.name)
            current = current.parent
        ret.reverse()
        return ret

    def expand(self, node: Node) -> List[Node]:
        """ Takes in a node and returns a list of nodes. Each of the nodes in the list
        represents a neighbor of the passed in node. The states from these neighbors
        are the non-None values returns from node.state.neighbors
        For each Node in the list:
        State: Neighbor Room of node
        Parent: node
        Direction: Direction of the neighbor in relation to node.
        Cost: cost of node plus 1 since all actions cost here cost 1
        """
        ret = []
        # cost to move from one room to another is just 1
        travel_cost = 1
        for i, n in enumerate(node.state.neighbors):
            if n is not None:
                ret.append(Node(n, node, Direction(i + 1), node.cost + travel_cost))

        return ret

    def breadth_first_search(self, target_location: Room) -> Any:
        """Takes in a Room that represents the target location.
        Implements a Breadth First Search to find a path from the start location
        to the target location. Returns a Node for the target location if it is found
        or None if a path does not exist to the target location."""
        # TODO: Implement BFS.

        start_room = self.dungeon.start
        start_node = Node(start_room, None, None, 0)

        
        if (start_room == target_location): #check if room is target
            return start_node

        frontier = self.expand(start_node) # find neighbors to visit
        reached = {start_node.state.name: start_node} # keep track of reached nodes {Key: name of room : Value: Node}
        while len(frontier) != 0: # while not every node has been reached
            current_node = frontier.pop(0) # first neighbor to visit
            for node in self.expand(current_node): # list of nodes
                room = node.state # a room
                if room == target_location: # check if this is target
                    return node
                if node.state.name not in reached.keys(): # if it has not been reached yet
                    reached[node.state.name] = node # add it to reached
                    frontier.append(node) # add node to frontier
        

        return None # if failed


            
    # Implementation of A*
    # sorted by manhattan distance
    def astar(self, target_location: Room) -> Node:
        """Takes in a Room that represents the target location. 
        Implements A* to find a path from the start location to the target location. 
        Makes use of the estimated_cost_to method in Room to estimate h(n).
        """# TODO implement A*"
        start_room = self.dungeon.start
        start_node = Node(start_room, None, None, 0)



        frontier = [start_node] #start of frontier
        reached = {start_node.state.name: start_node} # reached dictionary
        while len(frontier) != 0: # while frontier is not empty
            frontier = sorted(frontier, key = lambda x: (x.cost + x.state.estimated_cost_to(target_location))) # sorting frontier by cost and estimate
            
            current_node = frontier.pop(0) # take the first element
            print(current_node) # for debugging
            if current_node.state == target_location: #if its the target return the node
                return current_node
            for node in self.expand(current_node): # expand on current node
                room = node.state
                if node.state.name not in reached.keys() or node.cost < reached[node.state.name].cost: # if not in reached or node cost is less than reached node cost
                    reached[node.state.name] = node # update dict
                    frontier.append(node) # update frontier




        return None







    def depth_first_search(self, target_location: Room, limit: int = MAX_DEPTH) -> Any:
        """Takes in a Room that represents the target location.
        Implements a Level Limited Depth First Search to find a path from the start location
        to the target location. Returns a Node for the target location if it is found, the cutoff
        if the depth limit is reach, or None if a path does not exist to the target location."""
        #TODO implement a level limited version of DFS.


        start_room = self.dungeon.start # starting room of dungeon
        start_node = Node(start_room, None, None, 0) # creating starting node
        frontier = [start_node] # add strating node to frontier
        reached = {} # keep track of reached nodes to avoid loops
        
        while len(frontier) != 0: 
            current_node = frontier.pop() # last node in frontier
            if current_node.state == target_location: # is it target location
                return current_node
            if current_node.how_many_parents > limit: # is it past max depth
                return limit
            elif current_node.state.name not in reached.keys(): # if it has not been reached
                for node in list(reversed(self.expand(current_node))): # every neighbor of node
                    frontier.append(node) # append it to frontier
                reached[current_node.state.name] = current_node # add current node to reached

        return None


    def iterative_deepening(self, target_location: Room) -> Node:
        """Takes in a Room that represents the target location.
        Implements Iterative Deepening to find a path from the start location
        to the target location. Uses the Level Limited Depth First Search.
        Returns a Node for the target location if it is found or None if a
        path does not exist to the target location."""
        # TODO implement ID using your DFS implementation
        for i in range(MAX_DEPTH):
            result = self.depth_first_search(target_location, i) # trying out all the different depths
            if result != i: # if result doesn't equal cutoff
                return result 





