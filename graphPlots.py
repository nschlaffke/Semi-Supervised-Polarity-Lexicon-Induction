import igraph as ig

def plotWithLabels(graph):
    graph.vs()["label"] = graph.vs()["name"]
    ig.plot(graph)

def simplePlot(graph):
    ig.plot(graph)

def plotCommunity(communities):
    ig.plot(communities, mark_groups = True)
