import itertools

def flatten_unique(matrix):
    return list(set(itertools.chain(*matrix)))

