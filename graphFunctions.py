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

def getMinCut(graph, s, t):
    s_id = graph.vs().find('good').index
    t_id = graph.vs().find('bad').index

    graph.es()["capacity"] = [1 for i in range(graph.ecount())]
    min_cut = graph.maxflow(s_id, t_id, "capacity")
    return min_cut


if __name__ == "__main__":
    False