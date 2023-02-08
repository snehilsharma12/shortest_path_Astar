"""
main.py

Finds and draws the shortest path between given coordinates,
on the given map image image.

@author: Snehil Sharma (ss7696)
"""


import heapq
from math import sqrt
import sys
from node import node
from mapgraph import mapgraph
from PIL import Image


"""Lookup for terrain colors and penalties"""
map_legend = {

    (248,148,18) : [4, "open land"],
    (255,192,0): [5, "rough meadow"],
    (255,255,255) : [6, "easy movement forest"],
    (2,208,60) : [7, "slow run forest"],
    (2,136,40) : [8, "walk forest"],
    (5,73,24) : [15, "impassable vegetarian"],
    (0,0,255) : [20, "lake/swamp/marsh"],
    (71,51,3) : [2, "paved road"],
    (0,0,0) : [3, "footpath"],
    (205,0,101): [100, "out of bounds"]

}


"""builds and returns a graph representation
 of the map along with elevation values"""
def give_graph(map_file, ele_file):

    #reads map
    image = Image.open(map_file)
    rgb_image = image.convert("RGB")

    pixel_value = rgb_image.load()
    width, height = image.size

    elevation_values = []

    #reads elevation values
    with open (ele_file) as f:
        for line in f:
            line.strip()
            row = line.split()[0:-5]

            for i in range(len(row)):

                row[i] = float(row[i])
                

            elevation_values.append(row)
    

    new_map = mapgraph(width, height)

    #builds the graph
    for i in range(height):

        for j in range(width):

            new_map.add_node( node( pixel_value[j, i], j, i, elevation_values[i][j], map_legend[pixel_value[j, i]][0] ))



    new_map = make_graph(new_map)

    return new_map


"""Cost function for adjacent pixels"""
def adjacent_cost(node_a: tuple, node_b: tuple, map: mapgraph):

    e1 = map.node_list[node_a].elevation
    e2 = map.node_list[node_b].elevation

    b_cost = map.node_list[node_b].terrain_cost

    cost = (sqrt( 1 + (e1 - e2)**2))*b_cost

    return cost


"""builds edges between adjacent pixels using cost function"""
def make_graph(map: mapgraph):

    adj_coord = [(1,0), (0, 1), (-1, 0), (0, -1)]

    for i in range(map.height):

        for j in range(map.width):  

            for k in range(len(adj_coord)):

                next_node = (j + adj_coord[k][0], i + adj_coord[k][1])

                #edge cases
                if( next_node[0] >= 0) and (next_node[0] <= map.width-1) and \
                (next_node[1] >= 0) and (next_node[1] <= map.height-1):

                    cost = adjacent_cost((j, i), next_node, map )

                    map.add_edge((j, i), next_node, cost)

    return map


"""Calculates the heuristic value between two pixels"""
def get_hrstk(node_a: tuple, node_b: tuple, map: mapgraph):

    x1 = node_a[0]
    y1 = node_a[1]
    e1 = map.node_list[node_a].elevation

    x2 = node_b[0]
    y2 = node_b[1]
    e2 = map.node_list[node_b].elevation

    cost = sqrt((x1-x2)**2 + (y1-y2)**2 + (e1-e2)**2)

    return cost


"""finds shortest path between the pixels"""
def a_star(start_node, end_node, map: mapgraph):

    pqueue = []

    #heapq used as a priority queue
    heapq.heappush(pqueue, (0, start_node))
    predecessor = dict()
    g_cost = dict()

    predecessor[start_node] = None
    g_cost[start_node] = 0.0

    while len(pqueue) > 0:

        p, current_coord = heapq.heappop(pqueue)
        current_node = map.node_list[current_coord]

        #if target found
        if current_coord == end_node:
            path = []

            while predecessor[current_coord]!= None:
                path.append(current_coord)
                current_coord = predecessor[current_coord]
            
            path.append(start_node)
            path.reverse()

            return path

        #adjacent pixels of current 
        for nbr_node in current_node.get_nbrs():
            
            #getting x,y coordinates
            nbr = (nbr_node.x_coord, nbr_node.y_coord)

            #calculating g-value
            new_cost = g_cost[current_coord] + current_node.get_nbr_cost(nbr_node)

            #if new pixel or better estimate
            if nbr not in g_cost or new_cost < g_cost[nbr]:

                g_cost[nbr] = new_cost
                #calculating f-value
                queue_priority = new_cost + get_hrstk(nbr, end_node, map)
                #push to heapq
                heapq.heappush(pqueue, (queue_priority, nbr))
                predecessor[nbr] = current_coord


"""finds the paths between the coordinates"""
def get_path_list(visit_order, graph):

    print("finding paths")

    full_path = []

    for i in range (len(visit_order)-1):

        start_coord = (visit_order[i][0], visit_order[i][1])
        end_coord = (visit_order[i+1][0], visit_order[i+1][1]) 

        #perform A* seatch
        current_path = a_star(start_coord, end_coord, graph)

        full_path.extend(current_path)


    return full_path



"""driver function that takes the map, elevation and path_file info
 and outputs the image with the path drawn on it and 
 prints the distance of the path to terminal"""
def make_path(map_img, elevation_file, path_file, op_name):

    graph = give_graph(map_img, elevation_file)

    print("graph made")

    visitation_order = []

    #extracting coordinates from path file 
    with open(path_file) as f:

        for line in f:

            line.strip()
            coord = line.split()
            coord[0] = int(coord[0])
            coord[1] = int(coord[1])
            visitation_order.append(coord)

    #find the full path
    full_path = get_path_list(visitation_order, graph)

    dist = 0
    #calculate total distance of the path
    for i in range(len(full_path)-1):

        x1 = full_path[i][0]
        x2 = full_path[i+1][0]

        y1 = full_path[i][1]
        y2 = full_path[i+1][1]

        dx = abs(x1-x2)
        dy = abs(y1-y2)

        if(dy == 0):

            dist += dx*10.29

        if(dx == 0):

            dist += dy*7.55

    image = Image.open(map_img)
    rgb_image = image.convert("RGB")
    pixel_value = rgb_image.load()

    for i in full_path:
       pixel_value[i[0], i[1]] = (206,50,76)

    #generate output image
    rgb_image.save(op_name)

    print("Total Distance on path generated = " + str(dist) + "m")

    print("o/p generated")


def main():

    map_img = sys.argv[1]
    elevation_file = sys.argv[2]
    path_file = sys.argv[3]
    op_name = sys.argv[4]

    make_path(map_img, elevation_file, path_file, op_name)

    
if __name__ == "__main__":

    main()

