# First time, uncomment this to install wordnet
# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import igraph as ig

import graphFunctions
import generateGraph
import score
import helper

real_positives = helper.readCsvWords("./LMDictCsv/LMDpositive.csv")
real_negatives = helper.readCsvWords("./LMDictCsv/LMDnegative.csv")

graph = generateGraph.getFullADJGraph()
(predicted_positives, predicted_negatives) = graphFunctions.getMinCut(graph, "good", "bad")

fscores = []
fscores.append(score.fscore("Simple Fscore", real_positives, real_negatives, predicted_positives, predicted_negatives))
fscores.append(score.correctedFscore("Corrected Fscore", real_positives, real_negatives, predicted_positives, predicted_negatives, graph.vs()["name"]))

score.saveFScoresTable(fscores, "good")
score.printFscores(fscores)
# label_prop = labelProp.performLabelProp(graph, ['abaxial'], ['abducent'])