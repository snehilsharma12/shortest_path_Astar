"""
mapgraph.py

This is a graph that stores nodes, and dimensions of the graph

@author: Snehil Sharma
"""


from node import node

class mapgraph:

    def __init__(self, width, height):

        self.node_list = {}
        self.width = width
        self.height = height



    def add_node(self, node: node):
        self.node_list[(node.x_coord, node.y_coord)] = node


    def add_edge(self, start_coord: tuple, end_coord: tuple, cost):

        self.node_list[start_coord].add_nbr(self.node_list[end_coord], cost)
