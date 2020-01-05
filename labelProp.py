import numpy as np

def performLabelProp(graph, seeds1, seeds2):
    LABELS = 3 # 2 classes + default class
    s1_id = [graph.vs().find(word).index for word in seeds1]
    s2_id = [graph.vs().find(word).index for word in seeds2]

    # Generate trainsition matrix
    W = getW(graph)
    row_sums = W.sum(axis=1)
    T = W / row_sums[:, np.newaxis]
    T = np.nan_to_num(T, 0) # TODO nans are converted to 0 because of vertices with no connections

    # Step 1 - initialize
    V = len(graph.vs())
    Y = np.zeros((V, LABELS))
    Y[:,2] = 1 # Set all nodes to default label
    for _ in range(100):
        for s_id in s1_id:
            Y[s_id,:] = np.array([1,0,0])
        for s_id in s2_id:
            Y[s_id,:] = np.array([0,1,0])

        # Step 2 - propagate
        Y = T@Y
        
        # Step 3 - row-normalize
        row_sums = Y.sum(axis=1)
        Y /= row_sums[:, np.newaxis]
        Y = np.nan_to_num(Y, 0) # TODO nans are converted to 0 because of vertices with no connections
    return Y

def getW(graph, undirected=True):
    V = len(graph.vs())
    W = np.zeros((V, V))

    for edge, weight in zip(graph.get_edgelist(), graph.es['weight']):
        W[edge[0], edge[1]] = weight
        if(undirected):
            W[edge[1], edge[0]] = weight
    return W