import igraph as ig

def createGraph(words):
    graph = ig.Graph()
    graph.add_vertices(words)
    return graph

def addEdgeIf(graph, base_lemma_name, synonym_name):
    if(len(graph.vs().select(synonym_name)) > 0 and not graph.are_connected(base_lemma_name, synonym_name)):
        graph.add_edge(base_lemma_name, synonym_name)

def getMinCut(graph, s, t):
    s_id = graph.vs().find('good').index
    t_id = graph.vs().find('bad').index

    graph.es()["capacity"] = [1 for i in range(graph.ecount())]
    min_cut = graph.maxflow(s_id, t_id, "capacity")
    return min_cut


if __name__ == "__main__":
    False