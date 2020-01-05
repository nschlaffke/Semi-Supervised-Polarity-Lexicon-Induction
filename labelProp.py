import numpy as np
from scipy import sparse

def performLabelProp(graph, seeds1, seeds2, n_iter=10000):
    LABELS = 3 # 2 classes + default class
    s1_id = [graph.vs().find(word).index for word in seeds1]
    s2_id = [graph.vs().find(word).index for word in seeds2]

    # Generate trainsition matrix
    W = getW(graph)
    row_sums = W.sum(axis=1, keepdims=True)
    row_sums[row_sums==0] = 1
    T = W / row_sums
    del W
    del row_sums    
    T = sparse.csr_matrix(T)
    # Step 1 - initialize
    V = len(graph.vs())
    Y = np.zeros((V, LABELS))
    Y[:,2] = 1 # Set all nodes to default label
    for _ in range(n_iter):
        print(_)
        Y[s1_id] = np.array([1,0,0])
        Y[s2_id,:] = np.array([0,1,0])

        # Step 2 - propagate
        Y = T@Y
        
        # Step 3 - row-normalize
        row_sums = Y.sum(axis=1, keepdims=True)
        row_sums[row_sums==0] = 1
        Y /= row_sums
        
    return np.argmax(Y, axis=1)

def getW(graph, undirected=True):
    V = len(graph.vs())
    W = np.zeros((V, V))

    for edge, weight in zip(graph.get_edgelist(), graph.es['weight']):
        W[edge[0], edge[1]] = weight
        if(undirected):
            W[edge[1], edge[0]] = weight
    return W