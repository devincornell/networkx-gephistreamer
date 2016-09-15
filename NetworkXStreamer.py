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
        self.stream = streamer.Streamer(streamer.GephiWS(hostname="localhost", port=8080, workspace="workspace1"), auto_commit=True)

        # add aditional nodes
        nodeNames = baseGraph.nodes(data=False)
        numNodes = len(nodeNames)
        self.streamNodes = []
        for i in range(numNodes):
            self.streamNodes.append(graph.Node(str(i)))
            self.streamNodes[i].property['label'] = str(nodeNames[i])
            #self.streamNodes[i].property['size'] = 10.0

            #TODO WAS UPDATING THIS BEFORE I GOT TIRED
        
        self.stream.add_node(*(self.streamNodes))
        
        # add initial edges
        numEdges = len(baseGraph.edges(data=False))
        self.streamEdges = []
        for i in range(numNodes):
            for j in range(numNodes):
                #property_value = (self.streamNodes[i].property['weight'] + self.streamNodes[j].property['weight'])/2.0
                #self.streamEdges.append(graph.Edge(nodes[i],nodes[j], prop=property_value))
                self.streamEdges.append(graph.Edge(self.streamNodes[i],self.streamNodes[j],directed=False,label='',red=0.0,green=0.0,blue=0.0))

        self.stream.add_edge(*(self.streamEdges))

        # commit changes to visualization
        #self.stream.commit()

    def updateProperties(self, newGraph, nodeProperties, edgeProperties):
        '''Updates only the properties of the visualized graph with the newGraph properties.'''
        
        # update node properties
        for p in nodeProperties:
            nodeAttr = nx.get_node_attributes(newGraph, p)
            for k,v in nodeAttr.items():
                self.streamNodes[k].property[p] = v
        
        self.stream.change_node(*(self.streamNodes))
        
        # update edge properties
        for p in edgeProperties:
            edges = nx.get_edge_attributes(newGraph, p)
            for k,v in edges:
                self.streamEdges[k].property[p] = v
        
        self.stream.change_edge(*(self.streamEdges))

        # commit changes to visualization
        #self.stream.commit()

    def updateEdgeConnections(self, newGraph):
        '''Updates edge connections between nodes.'''

        # add/remove edges so they correspond to the ones in newGraph

        # commit changes to visualization
        self.stream.commit()


if __name__ == '__main__':
    import time
    
    G = nx.Graph()
    numNodes = 5
    
    # create nodes
    nodeAttr = ('r','g','b','x','y')
    for i in range(numNodes):
        xPos = numNodes*10*math.sin(2*math.pi*i/numNodes)
        yPos = numNodes*10*math.cos(2*math.pi*i/numNodes)
        G.add_node(i, {'r':0.5,'g':0.1,'b':0.1, 'x':xPos, 'y':yPos})

    # create edges
    edgeAttr = ('r','g','b','weight')
    for i in range(numNodes):
        for j in range(numNodes):
            G.add_edge(i, j, {'r':0.1,'g':0.1,'b':0.5, 'weight':1, 'directed':False})

    # start streaming
    nxs = NetworkXStreamer(G)

    # simulation loop
    for i in range(1):
        # update node attr
        for attr in nodeAttr:
            av = nx.get_node_attributes(G, attr)
            for k,v in av.items():
                av[k] = v + 0.01
            nx.set_node_attributes(G, attr, av)

        # update edge attr
        for attr in edgeAttr:
            av = nx.get_edge_attributes(G, attr)
            for k,v in av.items():
                av[k] = v + 0.01
            nx.set_edge_attributes(G, attr, av)

        # apply updates to streamer
        nxs.updateProperties(G,nodeAttr,edgeAttr)

        # pause
        print(i)
        time.sleep(5.0)





