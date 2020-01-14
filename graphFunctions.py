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

def getVerticesNames(graph, vertices_ids):
    return ig.VertexSeq(graph, vertices_ids)["name"]

if __name__ == "__main__":
    False