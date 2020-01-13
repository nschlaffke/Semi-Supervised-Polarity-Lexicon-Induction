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

NUMBER_OF_SEEDS = 100

real_positives = helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
real_negatives = helper.readCsvWords("./LMDictCsv/LMDnegative.csv")

negative_seed = np.random.choice(real_negatives, NUMBER_OF_SEEDS)
positive_seed = np.random.choice(real_positives, NUMBER_OF_SEEDS)

graph = generateGraph.getFullADJGraph()
(predicted_positives, predicted_negatives) = graphFunctions.getMinCut(graph, "good", "bad")

fscores = []
fscores.append(score.fscore("Simple Fscore", real_positives, real_negatives, predicted_positives, predicted_negatives))
fscores.append(score.correctedFscore("Corrected Fscore", real_positives, real_negatives, predicted_positives, predicted_negatives, graph.vs()["name"]))

score.saveFScoresTable(fscores, "good")
score.printFscores(fscores)

# Label prop
print("Label propagation")
(predicted_positives, predicted_negatives) = labelProp.performLabelProp(
    graph, 
    ["good"], 
    ["bad"])
fscores = []
fscores.append(score.fscore("Simple Fscore", real_positives, real_negatives, predicted_positives, predicted_negatives))
fscores.append(score.correctedFscore("Corrected Fscore", real_positives, real_negatives, predicted_positives, predicted_negatives, graph.vs()["name"]))

score.saveFScoresTable(fscores, "good")
score.printFscores(fscores)