import networkx as nx
import random
import matplotlib.pyplot as plt
#import randomgraph
G = nx.Graph()
G.add_edges_from([(0,1, {'weight': 6}), (1,3, {'weight': 11}), (3,4, {'weight': 7}), (4,2, {'weight': 10}), (4,0, {'weight': 9})])
random_graph = nx.erdos_renyi_graph(60, 0.05, seed=42)
new_roads = [(0,2), (0,3), (1,2), (1,4), (2,3)]

class graphNode:
    def __init__(self):
        self.trips = 0
        self.distance = 0
        self.benefit = 0

rows = 5
cols = 5

graphNodes = [[graphNode() for _ in range(cols)] for _ in range(rows)]

highest_benefit = 0
node1 = 0
node2 = 0
def find_benefits(G, graphNodes):
    for node in new_roads:
            x = node[0]
            y = node[-1]
            if x == y or graphNodes[x][y].distance == 0:
                continue
            spd = nx.astar_path_length(G,x,y)
            d = graphNodes[x][y].distance
            nt = graphNodes[x][y].trips + graphNodes[y][x].trips
            graphNodes[x][y].benefit = ((spd-d)*nt)

            for n1 in G.neighbors(y):
                n1Benefit = nx.astar_path_length(G,x,n1) - (d + graphNodes[y][n1].distance)
                if n1Benefit<0:
                    n1Benefit = 0
                graphNodes[x][y].benefit += n1Benefit*(graphNodes[x][n1].trips)
            
            for n2 in G.neighbors(x):
                n2Benefit = nx.astar_path_length(G,y,n2) - (d + graphNodes[x][n2].distance)
                if n2Benefit<0:
                    n2Benefit = 0
                graphNodes[x][y].benefit += n1Benefit*(graphNodes[y][n2].trips)
            
            if graphNodes[x][y].benefit > highest_benefit:
                highest_benefit = graphNodes[x][y].benefit
                node1 = x
                node2 = y



def build_road(G, graphNodes):
    k = 2
    for i in range(2):
        dist = random.randint(1,26)
        G.add_edge(node1, node2, distance=dist)
        find_benefits(G, graphNodes)



def print_graph(G):
 print("Graph with edge weights:")
 print(G.edges(data=True))
 
 # Visualize the graph
 pos = nx.spring_layout(G)  # You can choose a different layout if needed
 nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, edge_color='gray', width=1, edge_cmap=plt.cm.Blues)
 
 # Add edge labels with rounded weights
 edge_labels = {(edge[0], edge[1]): edge[2]['weight'] for edge in G.edges(data=True)}


 nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
 
 # Save the graph as an image (e.g., PNG or PDF)
 plt.savefig("erdos_renyi_graph.png", format="PNG")
 plt.show()




print_graph(G)
