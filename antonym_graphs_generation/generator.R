library(igraph)
rm(list = ls())

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
GRAPH <- "../graphs/getFullAdjAdvAntonymGraph.graphml"
SIM_GRAPH <- "../graphs/getFullADJADVGraph.graphml"
OUTPUT_GRAPH <- "../graphs/getFullADJADVANTGraph.graphml"

graph <- read_graph(GRAPH, format = "graphml")
degrees <- degree(graph)
small_graph <- delete_vertices(graph, V(graph)[degrees==0])

dist <- distances(small_graph)
inverted_edges <- which(dist != Inf & !(dist%%2) & dist != 0, arr.ind = TRUE)

sim_graph <- read_graph(SIM_GRAPH, format = "graphml")
n1 <- length(E(sim_graph))
edges <- c()
for(j in 1:len) {
  a <- inverted_edges[j,1]
  b <- inverted_edges[j,2]
  if(a != b) {
    v1 <- V(small_graph)[[a]]$name
    v2 <- V(small_graph)[[b]]$name
    e <- edge(V(sim_graph)[v1], V(sim_graph)[v2])
    sim_graph <- sim_graph + edge(e)
  }
}

n2 <- length(E(sim_graph))

write_graph(sim_graph, OUTPUT_GRAPH, format = "graphml")
print("Number of edges difference: ")
print(n2-n1)
