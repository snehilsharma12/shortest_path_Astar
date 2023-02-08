"""
node.py

Is a node class that stores:
rgb value of the pixel, x and y coordinates of the pixel,
elevation value of the pixel, terrain penalty of the pixel, neighbors of pixel

@author: Snehil Sharma
"""
class node:

    def __init__(self, pixel_rgb: tuple, x_coord, y_coord, elevation, terrain_cost: int):

        self.pixel_rgb = pixel_rgb
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.elevation = elevation
        self.terrain_cost = terrain_cost
        self.neighbors = {}

    
    def add_nbr(self, nbr, cost):

        self.neighbors[nbr] = cost


    def get_nbrs(self):
        
        return self.neighbors.keys()

    
    def get_nbr_cost(self, nbr):

        return self.neighbors[nbr]


    def __str__(self):
        
        return str(self.pixel_rgb) + " " + str(self.x_coord) + " " + str(self.y_coord) + " " + str(self.elevation) + " " + str(self.terrain_cost) + " " + str(self.neighbors)

