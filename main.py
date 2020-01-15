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
import newScore


def performMinCut(graph, real_positives, real_negatives, fscores):

    # Use the simplest min cut
    (predicted_positives, predicted_negatives) = minCut.getSimpleMinCut(
        graph, "good", "bad")

    fscores.append(newScore.getScores("Simple min-cut", real_positives, real_negatives,
                       predicted_positives, predicted_negatives))

    
    # Try to improve min-cut, adding a high capacity to adjacent edges, so they don't get cut
    (predicted_positives, predicted_negatives) = minCut.getNonNeighboursEdgesMinCut(
        graph, "good", "bad")

    fscores.append(newScore.getScores("Non Neighbours min-cut", real_positives, real_negatives,
                       predicted_positives, predicted_negatives))                   


    NUMBER_OF_SEEDS = 50
    negative_seed = np.random.choice(real_negatives, NUMBER_OF_SEEDS)
    positive_seed = np.random.choice(real_positives, NUMBER_OF_SEEDS)

    # Try to improve min-cut, adding a subgraph of connected edges so they don't get cut
    (predicted_positives, predicted_negatives) = minCut.getNonSubgraphEdgesMinCut(
        graph, positive_seed, negative_seed)

    fscores.append(newScore.getScores("Non Subgraph min-cut", real_positives, real_negatives, predicted_positives,
                                         predicted_negatives))
    
    # Add both formulas
    (predicted_positives, predicted_negatives) = minCut.getNonSubgraphNonNeighboursEdgesMinCut(
        graph, positive_seed, negative_seed)

    fscores.append(newScore.getScores("Non Neig-Sub min-cut", real_positives, real_negatives, predicted_positives,
                                         predicted_negatives))


def performLabelProp(graph, real_positives, real_negatives, fscores):
    NUMBER_OF_SEEDS = 50
    print("Label propagation")
    negative_seed = np.random.choice(real_negatives, NUMBER_OF_SEEDS)
    positive_seed = np.random.choice(real_positives, NUMBER_OF_SEEDS)

    (predicted_positives, predicted_negatives) = labelProp.performLabelProp(
        graph,
        negative_seed,
        positive_seed)

    fscores.append(newScore.getScores("LP", real_positives, real_negatives,
                       predicted_positives, predicted_negatives))

# MAIN

# set the name outputs will have
graph_name = "FullAdj"

graph = generateGraph.getFullADJGraph()
graph = graphFunctions.removeDisconnectedVertices(graph)

used_dictionary = graphFunctions.getVerticesNames(
    graph, range(len(graph.vs())))
real_positives = [word for word in helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
                  if word in used_dictionary]
real_negatives = [word for word in helper.readCsvWords("./LMDictCsv/LMDnegative.csv")
                  if word in used_dictionary]

fscores = []

performMinCut(graph, real_positives, real_negatives, fscores)
performLabelProp(graph, real_positives, real_negatives, fscores)