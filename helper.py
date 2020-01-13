import itertools
import csv

def flatten_unique(matrix):
    return list(set(itertools.chain(*matrix)))

def unique(matrix):
    return list(set(matrix))

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2))

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
