Finds the shortest path between two points and drows the path on a given map image.
Can also draw a path if given a set of destinations to visit on the way, with the shortest path taken between them.
Takes elevation into consideration if an elevation file is provided.

Design decision: A pixel’s neighbors are 4 pixels that share an edge. 

Each terrain type is represented by a unique color. 
Terrain penalties are as follows:

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
 
Note that, the higher the number, the higher the penalty.
