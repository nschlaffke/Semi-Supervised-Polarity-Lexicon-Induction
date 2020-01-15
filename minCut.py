import graphFunctions

# Base function
def getMinCut(graph, s, t):
    s_id = graph.vs().find(s).index
    t_id = graph.vs().find(t).index

    min_cut = graph.st_mincut(s_id, t_id, "capacity")

    positive_names = graphFunctions.getVerticesNames(graph, min_cut[0])
    negative_names = graphFunctions.getVerticesNames(graph, min_cut[1])
    return (positive_names, negative_names, min_cut)

# Min Cuts
def getSimpleMinCut(graph, s, t):
    graph.es()["capacity"] = [1 for i in range(graph.ecount())]
    return getMinCut(graph, s, t)

def getNonNeighboursEdgesMinCut(graph, s, t):

    s_id = graph.vs().find(s).index
    t_id = graph.vs().find(t).index

    graph.es()["capacity"] = [1 for i in range(graph.ecount())]

    # we force that directly connected edges to one of the nodes should belong to the same cluster
    corner_edges_ids = graph.incident(s_id) + graph.incident(t_id)
    setBigcapacity(graph, corner_edges_ids)


    return getMinCut(graph, s, t)

def getNonSubgraphEdgesMinCut(graph, s, t):

    graph.es()["capacity"] = [1 for i in range(graph.ecount())]

    # we force that directly connected edges to one of the nodes should belong to the same cluster
    corner_edges_ids = graphFunctions.getEdgesBetween(graph, s) + graphFunctions.getEdgesBetween(graph, t)
    setBigcapacity(graph, corner_edges_ids)

    return getMinCut(graph, s[0], t[0])

def getNonSubgraphNonNeighboursEdgesMinCut(graph, s, t):

    graph.es()["capacity"] = [1 for i in range(graph.ecount())]

    corner_edges_ids = list()

    for i in s:
        i_id = graph.vs().find(i).index
        corner_edges_ids += graph.incident(i_id)

    for i in t:
        i_id = graph.vs().find(i).index
        corner_edges_ids += graph.incident(i_id)

    # we force that directly connected edges to one of the nodes should belong to the same cluster
    corner_edges_ids += graphFunctions.getEdgesBetween(graph, s) + graphFunctions.getEdgesBetween(graph, t)
    setBigcapacity(graph, corner_edges_ids)

    return getMinCut(graph, s[0], t[0])

def setBigcapacity(graph, edges_ids):
    for edge_id in edges_ids:
        graph.es()[edge_id]["capacity"] = 10000