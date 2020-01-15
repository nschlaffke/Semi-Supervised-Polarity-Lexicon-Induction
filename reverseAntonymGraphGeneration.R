library(igraph)
rm(list = ls())
GENERATE_ANTONYMS <- TRUE

graph <- read_graph("getAntonymADJONLYGraph.graphml", format = "graphml")
degrees <- degree(graph)
small_graph <- delete_vertices(graph, V(graph)[degrees==0])

if (GENERATE_ANTONYMS) {
  for (i in 1:10) {
    print(i)
    dist <- distances(small_graph)
    ans <- which(dist != Inf & dist%%2 & dist != 1, arr.ind = TRUE)
    len <- dim(ans)[1]
    if (len == 0)
      break
    for(j in 1:len) {
      small_graph <- add_edges(small_graph, ans[j,])
    }
  }
}

dist <- distances(small_graph)
inverted_edges <- which(dist != Inf & !(dist%%2) & dist != 0, arr.ind = TRUE)
graph <- delete_edges(graph, E(graph))
len <- dim(inverted_edges)[1]
for(j in 1:len) {
  graph <- add_edges(graph, inverted_edges[j,])
}
hist(degree(graph))
