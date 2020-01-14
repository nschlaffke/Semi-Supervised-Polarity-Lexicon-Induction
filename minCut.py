import graphFunctions

# Base function
def getMinCut(graph, s, t):
    s_id = graph.vs().find('good').index
    t_id = graph.vs().find('bad').index

    min_cut = graph.maxflow(s_id, t_id, "capacity")

    positive_names = graphFunctions.getVerticesNames(graph, min_cut[0])
    negative_names = graphFunctions.getVerticesNames(graph, min_cut[1])
    return (positive_names, negative_names)


# Min Cuts
def getSimpleMinCut(graph, s, t):
    graph.es()["capacity"] = [1 for i in range(graph.ecount())]
    return getMinCut(graph, s, t)

def getNonNeighboursEdgesMinCut(graph, s, t):

    s_id = graph.vs().find('good').index
    t_id = graph.vs().find('bad').index

    graph.es()["capacity"] = [1 for i in range(graph.ecount())]

    # we force that directly connected edges to one of the nodes should belong to the same node
    corner_edges_ids = graph.incident(s_id) + graph.incident(t_id)
    for edge_id in corner_edges_ids:
        graph.es()[edge_id]["capacity"] = 10000

    return getMinCut(graph, s, t)