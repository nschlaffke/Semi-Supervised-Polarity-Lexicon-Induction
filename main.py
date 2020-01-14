# First time, uncomment this to install wordnet
# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import igraph as ig
import numpy as np

import graphFunctions
import generateGraph
import score
import helper
import labelProp
import minCut

def performMinCut(graph, real_positives, real_negatives, fscores):

    # Use the simplest min cut
    (predicted_positives, predicted_negatives) = minCut.getSimpleMinCut(graph, "good", "bad")

    fscores.append(score.correctedFscore("Simple min-cut", real_positives, real_negatives, predicted_positives, 
        predicted_negatives, graph.vs()["name"]))

    # Try to improve min-cut, adding a high capacity to adjacent edges, so they don't get cut
    (predicted_positives, predicted_negatives) = minCut.getNonNeighboursEdgesMinCut(graph, "good", "bad")

    fscores.append(score.correctedFscore("Non Neighbours min-cut", real_positives, real_negatives, predicted_positives, 
        predicted_negatives, graph.vs()["name"]))

    # Try to improve min-cut, adding a subgraph of connected edges so they don't get cut
    (predicted_positives, predicted_negatives) = minCut.getNonNeighboursEdgesMinCut(graph, "good", "bad")

    fscores.append(score.correctedFscore("Non Neighbours min-cut", real_positives, real_negatives, predicted_positives, 
        predicted_negatives, graph.vs()["name"]))

    # Try with only the words 

def performLabelProp(graph, real_positives, real_negatives, fscores):
    # Label prop
    print("Label propagation")
    (predicted_positives, predicted_negatives) = labelProp.performLabelProp(
        graph, 
        ["good"], 
        ["bad"])

    fscores.append(score.fscore("S LP", real_positives, real_negatives, predicted_positives, predicted_negatives))
    fscores.append(score.correctedFscore("C LP", real_positives, real_negatives, predicted_positives, 
        predicted_negatives, graph.vs()["name"]))


# MAIN

NUMBER_OF_SEEDS = 100

real_positives = helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
real_negatives = helper.readCsvWords("./LMDictCsv/LMDnegative.csv")

negative_seed = np.random.choice(real_negatives, NUMBER_OF_SEEDS)
positive_seed = np.random.choice(real_positives, NUMBER_OF_SEEDS)

graph = generateGraph.getFullADJGraph()
fscores = []

performMinCut(graph, real_positives, real_negatives, fscores)
performLabelProp(graph, real_positives, real_negatives, fscores)

score.saveFScoresTable(fscores, "good")
score.printFscores(fscores)