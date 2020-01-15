import igraph as ig
import numpy as np
import loadWordNet
import helper

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

def getEdgesBetween(graph, vertices_names):
    edges_index = list()
    
    for base_vertex_name in vertices_names:
        for vertex_name in vertices_names:
            if base_vertex_name != vertex_name:
                edge_index = graph.get_eid(base_vertex_name, vertex_name, directed=False, error=False)
                if(edge_index != -1):
                    edges_index.append(edges_index)
    return edges_index

def getVerticesNames(graph, vertices_ids):
    return ig.VertexSeq(graph, vertices_ids)["name"]

def getId(value):
    return value.index

def getIds(values):
    return helper.unique(map(getId, values))

def removeDisconnectedVertices(graph):
    graph.vs()['degree'] = graph.outdegree() # = graph.indegree()
    to_remove = graph.vs().select(degree=0)
    graph.delete_vertices(to_remove)
    return graph

def getLargerConnectedComponent(graph):
    cl = graph.clusters()
    lcc = cl.giant()
    return lcc


if __name__ == "__main__":
    False