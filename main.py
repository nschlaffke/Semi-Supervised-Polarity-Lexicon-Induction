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
import graphPlots
import loadWordNet

def lemmasVsSynsetsGraph():

    verySmallLemmasGraph = generateGraph.getVerySmallGoodBadDepthGraph()
    graphPlot = graphPlots.plotWithLabels(verySmallLemmasGraph)
    graphPlots.savePlot(graphPlot, "verySmallLemmasGraph")

    verySmallSynsetGraph = generateGraph.getVerySmallGoodBadDepthSynsetGraph()
    graphPlot = graphPlots.plotWithLabels(verySmallSynsetGraph)
    graphPlots.savePlot(graphPlot, "verySmallSynsetGraph")

    smallLemmasGraph = generateGraph.getSmallGoodBadDepthGraph()
    graphPlot = graphPlots.plotWithLabels(smallLemmasGraph)
    graphPlots.savePlot(graphPlot, "smallLemmasGraph")

    synsets = loadWordNet.findSynonymsSynsetsLemmaName("bad")
    for synset in synsets:
        lemmas = loadWordNet.getNames(loadWordNet.getSynsetLemmas(synset))
        if('big' in lemmas):
            print(loadWordNet.getName(synset))
            print(lemmas)

    smallSynsetGraph = generateGraph.getSmallGoodBadDepthSynsetGraph()
    graphPlot = graphPlots.plotWithLabels(smallSynsetGraph)
    graphPlots.savePlot(graphPlot, "smallSynsetGraph")

    lemmasGraph = generateGraph.getFullADJGraph()
    shortestPathLemmasGraph = lemmasGraph.subgraph(graphFunctions.shortestPath(lemmasGraph, "good", "bad")[0])
    graphPlot = graphPlots.plotWithLabels(shortestPathLemmasGraph)
    graphPlots.savePlot(graphPlot, "shortestPathLemmasGraph")

    synsetGraph = generateGraph.getFullADJSynsetGraph()
    shortestPathSynsetGraph = synsetGraph.subgraph(graphFunctions.shortestPath(synsetGraph, "good.a.01", "bad.a.01")[0])
    graphPlot = graphPlots.plotWithLabels(shortestPathSynsetGraph)
    graphPlots.savePlot(graphPlot, "shortestPathSynsetGraph")


def performMinCut(graph, real_positives, real_negatives, original_positives, original_negatives, fscores, isSynsetGraph):
    positive_seed, negative_seed = helper.getSeed(graph, SEED_SIZE, real_positives, real_negatives)

    good = loadWordNet.convertIf(["good"], isSynsetGraph)
    bad = loadWordNet.convertIf(["bad"], isSynsetGraph)

    if(isSynsetGraph):
        # this only works for graphs that contain adjectives
        good = ["good.a.01"]
        bad = ["bad.a.01"]

    # Use the simplest min cut

    (predicted_positives, predicted_negatives, cluster) = minCut.getSimpleMinCut(
        graph, good, bad)

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)

    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(score.fscore("Simple min-cut", real_positives, real_negatives, original_positives, original_negatives,
                                      predicted_positives, predicted_negatives))

    # Try to improve min-cut, adding a high capacity to adjacent edges, so they don't get cut
    (predicted_positives, predicted_negatives, cluster) = minCut.getNonNeighboursEdgesMinCut(
        graph, good, bad)

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)
    
    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(score.fscore("Non Neighbours min-cut", real_positives, real_negatives, original_positives, original_negatives,
                                      predicted_positives, predicted_negatives))

    # Try to improve min-cut, adding a subgraph of connected edges so they don't get cut
    (predicted_positives, predicted_negatives, cluster) = minCut.getNonSubgraphEdgesMinCut(
        graph, positive_seed, negative_seed)

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)
    
    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(score.fscore("Non Subgraph min-cut", real_positives, real_negatives, original_positives, original_negatives, predicted_positives,
                                      predicted_negatives))

    # Add both formulas
    (predicted_positives, predicted_negatives, cluster) = minCut.getNonSubgraphNonNeighboursEdgesMinCut(
        graph, positive_seed, negative_seed)

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)
    
    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(score.fscore("Non Neig-Sub min-cut", real_positives, real_negatives, original_positives, original_negatives, predicted_positives,
                                      predicted_negatives))

def performLabelProp(graph, real_positives, real_negatives, original_positives, original_negatives, fscores, isSynsetGraph):
    print("Label propagation")
    positive_seed, negative_seed = helper.getSeed(graph, SEED_SIZE, real_positives, real_negatives)

    (predicted_positives, predicted_negatives) = labelProp.performLabelProp(
        graph,
        loadWordNet.convertIf(negative_seed, isSynsetGraph),
        loadWordNet.convertIf(positive_seed, isSynsetGraph))

    if(isSynsetGraph):
        predicted_positives = loadWordNet.fromSynsetsToLemmas(predicted_positives)
        predicted_negatives = loadWordNet.fromSynsetsToLemmas(predicted_negatives)
    
    (predicted_positives, predicted_negatives) = score.clearOutputs(predicted_positives, predicted_negatives)

    fscores.append(score.fscore("LP", real_positives, real_negatives, original_positives, original_negatives,
                                      predicted_positives, predicted_negatives))


# MAIN

def performAllTests(graph_name, synsetGraph=False):
    graph = getattr(generateGraph, graph_name)()
    graph = graphFunctions.removeDisconnectedVertices(graph)

    original_positives = helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
    original_negatives = helper.readCsvWords("./LMDictCsv/LMDnegative.csv")

    if(not synsetGraph):
        used_dictionary = graphFunctions.getVerticesNames(
            graph, range(len(graph.vs())))
        
        real_positives = [word for word in helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
                        if word in used_dictionary]
        real_negatives = [word for word in helper.readCsvWords("./LMDictCsv/LMDnegative.csv")
                        if word in used_dictionary]
    else:
        real_positives = helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
        real_negatives = helper.readCsvWords("./LMDictCsv/LMDnegative.csv")

    fscores = []

    performMinCut(graph, real_positives, real_negatives, original_positives, original_negatives, fscores, synsetGraph)
    performLabelProp(graph, real_positives, real_negatives, original_positives, original_negatives, fscores, synsetGraph)

    score.saveFScoresTable(fscores, graph_name)

SEED_SIZE = 20
# performAllTests("getFullADJADVGraph")
# lemmasVsSynsetsGraph()

