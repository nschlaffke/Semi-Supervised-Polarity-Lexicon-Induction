import itertools
import csv
import numpy as np
import graphFunctions

def flatten_unique(matrix):
    return list(set(itertools.chain(*matrix)))

def unique(matrix):
    return list(set(matrix))

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2))

def substract(lst1, lst2):
    return list(set(lst1) - set(lst2))

def readCsvWords(filepath):
    readed = []

    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # skip headers
            if line_count > 0:
                readed.append(row[1].lower())
            line_count += 1
    return readed 

def getSeed(graph, size, real_positives, real_negatives):
    """
        Return the same words for same graph and same
    """
    if size == 2 and 'good' in real_positives and 'bad' in real_negatives:
        return ['good'], ['bad']

    np.random.seed(size)
    used_dictionary = graphFunctions.getVerticesNames(
        graph, range(len(graph.vs())))

    chosen_pos = np.random.choice(real_positives, size=size)
    chosen_neg = np.random.choice(real_negatives, size=size)

    return chosen_pos.tolist(), chosen_neg.tolist()