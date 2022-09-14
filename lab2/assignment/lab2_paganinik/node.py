#
# CS2400 Introduction to AI
# Node.py
#
# Spring, 2022
#
# Author: Roby Velez
#
# This class creates a Node object that can be used to traverse
# a state graph or tree

# Note: Instance variables with a single preceeding underscore are intended
# to be protected, so setters and getters are included to enable this convention.
#
# Note: The -> notation in the function definition line is a type hint.  This
# will make identifying the appropriate return type easier, but they are not
# enforced by Python.
#
from dungeon import Room, Direction
from typing import *

class Node:
    """
    Represents a Node for graph and tree traversal.

    Attributes:
        state(Room) Room this node represents being in
        parent(Node) Parent Node of this node. None if this is the root.
        action(Direction) Direction traveled from parent to this node. None if root.
        cost(float) Cost to travel up to this node

    """
    def __init__(self, state: Room, parent: Any = None, action: Direction = None, cost: float = 0):
        """ This constructor stores the references when the Node is
        initialized. """
        self._state = state
        self._parent = parent
        self._action = action
        self._cost = cost
    @property
    def state(self):
        """state this node represents"""
        return self._state
    @property
    def parent(self):
        """returns the parent of this node"""
        return self._parent
    @property
    def cost(self):
        """returns the cost to get to this node"""
        return self._cost

    
    #########################################
    # Added this to check what the depth is
    #########################################
    
    @property
    def how_many_parents(self):
        num_parents = 0
        temp_parent = self._parent
        while temp_parent is not None:
            num_parents += 1
            temp_parent = temp_parent.parent
        return num_parents

    def __str__(self) -> str:
        """String representation of the node"""
        if self.parent is None:
            return str(self.state) + ":" + str(None) + ":" + str(self._action) + ":" + str(self.cost)
        else:
            return str(self.state) + ":" + str(self.parent.state) + ":" + str(self._action) + ":" + str(self.cost)

    #You shouldn't need either of these
    #def __eq__(self, other):
    #    """returns true is two nodes have the same state"""
    #    return self.state == other.state

    #def __repr__(self) -> str:
    #    """String representation when in a list"""
    #    return self.__str__()
