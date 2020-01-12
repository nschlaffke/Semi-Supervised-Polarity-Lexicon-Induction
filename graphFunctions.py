import igraph as ig

def checkVertexNameExists(graph, name):
    return len(graph.vs().select(name=name)) > 0

def shortestPath(graph, s,t):
    return graph.get_shortest_paths(s, t)

def communityFastgreedy(graph):
    dendogram = graph.community_fastgreedy(graph)
    clusters = dendogram.as_clusters()
    return clusters

def createGraph(words):
    graph = ig.Graph()
    graph.add_vertices(words)
    return graph

def addEdgeIf(graph, base_lemma_name, synonym_name):
    if(base_lemma_name != synonym_name and checkVertexNameExists(graph, synonym_name) and 
            not graph.are_connected(base_lemma_name, synonym_name)):
        graph.add_edge(base_lemma_name, synonym_name)

def addNodeIfNotExists(graph, name):
    if(not checkVertexNameExists(graph, name)):
        graph.add_vertex(name)

def getMinCut(graph, s, t):
    s_id = graph.vs().find('good').index
    t_id = graph.vs().find('bad').index

    graph.es()["capacity"] = [1 for i in range(graph.ecount())]

    # we force that directly connected edges to one of the nodes should belong to the same node
    corner_edges_ids = graph.incident(s_id) + graph.incident(t_id)
    for edge_id in corner_edges_ids:
        graph.es()[edge_id]["capacity"] = 10000

    min_cut = graph.maxflow(s_id, t_id, "capacity")
    return min_cut


if __name__ == "__main__":
    False