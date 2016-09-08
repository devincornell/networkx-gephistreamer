## Note ##
# This code is taken from the GephiStreamer GitHub page. I'm using it as a staring place.
# https://github.com/totetmatt/GephiStreamer

# to get node properties, try to find member variable names in the java docs.
# https://gephi.org/docs/api/org/gephi/graph/api/NodeData.html

# to get edge properties, try to find member variable names in the java docs.
# https://

# all java docs are here

import networkx as nx
from gephistreamer import graph
from gephistreamer import streamer
import math

# Create a Streamer
# adapt if needed : streamer.GephiWS(hostname="localhost", port=8080, workspace="workspace0")
# You can also use REST call with GephiREST (a little bit slower than Websocket)
stream = streamer.Streamer(streamer.GephiWS(hostname="localhost", port=8080, workspace="workspace1"))

nodes = []
for i in range(10):
    nodes.append(graph.Node(str(i)))
    nodes[i].property['weight'] = i/2.0
    nodes[i].property['size'] = 10.0
    nodes[i].property['x'] = 100*math.sin(2*math.pi*i/10)
    nodes[i].property['y'] = 100*math.cos(2*math.pi*i/10)
    nodes[i].property['r'] = 0.5
    nodes[i].property['g'] = 0.1
    nodes[i].property['b'] = 0.1
    #nodes[i].color_hex(0,127,0)

# Add the node to the stream
# you can also do it one by one or via a list
# l = [node_a,node_b]
# stream.add_node(*l)
stream.add_node(*nodes)

# Create edge 
# You can also use the id of the node :  graph.Edge("A","B",custom_property="hello")
edges = []
for i in range(10):
    for j in range(10):
        property_value = (nodes[i].property['weight'] + nodes[j].property['weight'])/2.0
        edges.append(graph.Edge(nodes[i],nodes[j], prop=property_value))

stream.add_edge(*edges)

#import time
#time.sleep(60)
