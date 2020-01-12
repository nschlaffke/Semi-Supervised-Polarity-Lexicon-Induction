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
fscore = score.fscore("Simple Fscore", real_positives, real_negatives, predicted_positives, predicted_negatives)
score.saveFScoresTable([fscore], "good")
# label_prop = labelProp.performLabelProp(graph, ['abaxial'], ['abducent'])