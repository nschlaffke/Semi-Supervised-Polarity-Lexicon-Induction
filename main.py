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
import graphPlots
import loadWordNet


def performMinCut(graph, real_positives, real_negatives, fscores, isSynsetGraph):
    positive_seed, negative_seed = helper.getSeed(graph, SEED_SIZE, real_positives, real_negatives)
    # Use the simplest min cut

    (predicted_positives, predicted_negatives, cluster) = minCut.getSimpleMinCut(
        graph, loadWordNet.convertIf(["good"], isSynsetGraph), loadWordNet.convertIf(["bad"], isSynsetGraph))

    fscores.append(newScore.getScores("Simple min-cut", real_positives, real_negatives,
                                      predicted_positives, predicted_negatives))

    # Try to improve min-cut, adding a high capacity to adjacent edges, so they don't get cut
    (predicted_positives, predicted_negatives, cluster) = minCut.getNonNeighboursEdgesMinCut(
        graph, loadWordNet.convertIf(["good"], isSynsetGraph), loadWordNet.convertIf(["bad"], isSynsetGraph))

    fscores.append(newScore.getScores("Non Neighbours min-cut", real_positives, real_negatives,
                                      predicted_positives, predicted_negatives))

    # Try to improve min-cut, adding a subgraph of connected edges so they don't get cut
    (predicted_positives, predicted_negatives, cluster) = minCut.getNonSubgraphEdgesMinCut(
        graph, positive_seed, negative_seed)

    fscores.append(newScore.getScores("Non Subgraph min-cut", real_positives, real_negatives, predicted_positives,
                                      predicted_negatives))

    # Add both formulas
    (predicted_positives, predicted_negatives, cluster) = minCut.getNonSubgraphNonNeighboursEdgesMinCut(
        graph, positive_seed, negative_seed)

    fscores.append(newScore.getScores("Non Neig-Sub min-cut", real_positives, real_negatives, predicted_positives,
                                      predicted_negatives))


def performLabelProp(graph, real_positives, real_negatives, fscores, synsetGraph):
    print("Label propagation")
    positive_seed, negative_seed = helper.getSeed(graph, SEED_SIZE, real_positives, real_negatives)

    (predicted_positives, predicted_negatives) = labelProp.performLabelProp(
        graph,
        negative_seed,
        positive_seed)

    fscores.append(newScore.getScores("LP", real_positives, real_negatives,
                                      predicted_positives, predicted_negatives))


# MAIN

def performAllTests(graph_name, synsetGraph=False):
    graph = getattr(generateGraph, graph_name)()
    graph = graphFunctions.removeDisconnectedVertices(graph)

    used_dictionary = graphFunctions.getVerticesNames(
        graph, range(len(graph.vs())))

    real_positives = [word for word in helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
                      if word in used_dictionary]
    real_negatives = [word for word in helper.readCsvWords("./LMDictCsv/LMDnegative.csv")
                      if word in used_dictionary]

    fscores = []

    performMinCut(graph, real_positives, real_negatives, fscores, synsetGraph)
    performLabelProp(graph, real_positives, real_negatives, fscores, synsetGraph)

SEED_SIZE = 10
performAllTests("getFullAdjAdvAntExtGraph")