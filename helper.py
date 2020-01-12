import itertools

def flatten_unique(matrix):
    return list(set(itertools.chain(*matrix)))

def unique(matrix):
    return list(set(matrix))

