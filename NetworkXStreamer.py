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

class NetworkXStreamer():
    def __init__(self, baseGraph):
        # init streamer
        self.stream = streamer.Streamer(streamer.GephiWS(hostname="localhost", port=8080, workspace="workspace1"), auto_commit=False)

        # add aditional nodes
        numNodes = 10
        self.nodes = []
        for i in range(numNodes):
            nodes.append(graph.Node(str(i)))
            #self.nodes[i].property['weight'] = i/2.0
            #self.nodes[i].property['size'] = 10.0
            #TODO WAS UPDATING THIS BEFORE I GOT TIRED
        
        self.stream.add_node(*self.nodes)
        
        # add initial edges
        self.edges = []
        for i in range(10):
            for j in range(10):
                property_value = (self.nodes[i].property['weight'] + self.nodes[j].property['weight'])/2.0
                self.edges.append(graph.Edge(nodes[i],nodes[j], prop=property_value))

        self.stream.add_edge(*edges)

        # commit changes to visualization
        self.stream.commit()

    def updateProperties(self, newGraph, nodeProperties, edgeProperties):
        '''Updates only the properties of the visualized graph with the newGraph properties.'''
        
        # update nodes
        for p in nodeProperties:
            nodes = nx.get_node_attributes(newGraph, p)
            for k,v in nodes:
                self.nodes[k] = v
        
        self.stream.change_node(*self.nodes)
        
        # update edges
        for p in edgeProperties:
            edges = nx.get_edge_attributes(newGraph, p)
            for k,v in edges:
                self.edges[k] = v
        
        self.stream.change_edge(*self.edges)

        # commit changes to visualization
        self.stream.commit()

    def updateEdgeConnections(self, newGraph):
        '''Updates edge connections between nodes.'''

        # add/remove edges so they correspond to the ones in newGraph

        # commit changes to visualization
        self.stream.commit()


if __name__ == '__main__':
    import time
    
    G = nx.Graph()
    numNodes = 10
    
    # create nodes
    for i in range(numNodes):
        xPos = numNodes*10*math.sin(2*math.pi*i/numNodes)
        yPos = numNodes*10*math.cos(2*math.pi*i/numNodes)
        G.add_node(i, {'r':0.5,'g':0.1,'b':0.1, 'x':xPos, 'y':yPos})
    nodeAttr = ('r','g','b','x','y')

    # create edges
    edgeAttr = ('r','g','b','weight')
    for i in range(numNodes):
        for j in range(numNodes):
            G.add_edge(i, j, {'r':0.1,'g':0.1,'b':0.5, 'weight':1, 'directed':False})

    
    # start streaming
    nxs = NetworkXStreamer(G)

    # simulation loop
    for i in range(50):
        # update node attr
        for attr in nodeAttr:
            av = nx.get_node_attributes(G, attr)
            for k,v in av:
                av[k] = v + 0.01
            nx.set_node_attributes(G, attr, av)

        # update edge attr
        for attr in edgeAttr:
            av = nx.get_edge_attributes(G, attr)
            for k,v in av:
                av[k] = v + 0.01
            nx.set_edge_attributes(G, attr, av)

        # apply updates to streamer
        nxs.updateProperties(G,nodeAttr,edgeAttr)

        # pause
        time.sleep(0.01)
#
#
