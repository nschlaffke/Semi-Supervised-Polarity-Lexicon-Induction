
import plotly.graph_objects as go

import graphFunctions
import generateGraph
import labelProp
import minCut
import helper
from sklearn.metrics import classification_report

class FScore:
    def __init__(self, name, report):

        self.name = name

        true_positives = 1
        true_negatives = 1
        false_positives = 1
        false_negatives =1 

        self.precision = len(true_positives)/(len(true_positives) + len(false_positives))
        self.recall = len(true_positives)/(len(true_positives) + len(false_negatives))
        self.fscore = 2*self.precision*self.recall/(self.precision + self.recall)

        self.positive_hit_ratio = 1
        self.negative_hit_ratio = 1

        self.positive_found_ratio = 1
        self.negative_found_ratio = 1
    
    def setName(self, name):
        self.name = name

    def toDict(self):
        return vars(self)

    def toList(self):
        return list(self.toDict().values())

    def keys(self):
        return self.toDict().keys()

    def print(self):
        print(self.toDict())
 

def fscore(score_name, name, realPos, realNeg, predPos, predNeg):
    intersection = sorted(list(set(realPos + realNeg) & set(predPos + predNeg)))
    labelsPred = ['positive' if word in predPos else 'negative' for word in intersection]
    labelsReal = ['positive' if word in realPos else 'negative' for word in intersection]
    report = classification_report(labelsReal, labelsPred, output_dict=True)
    print(classification_report(labelsReal, labelsPred))

    # We might have leave some unlabeled, so we count found ratio
    positiveFound = 100*len(set(predPos) & set(realPos))/len(realPos)
    negativeFound = 100*len(set(predNeg) & set(realNeg))/len(realNeg)
    print('Positives found: %.2f %%' % (positiveFound))
    print('Negatives found: %.2f %%' % (negativeFound))
    report['positive']['found'] = positiveFound
    report['negative']['found'] = negativeFound

    return FScore(score_name, report)

def getValues(fscores, column):
    return list(map(lambda x: '%.4f' % x.toDict()[column] if type(x.toDict()[column]) is float else x.toDict()[column], fscores))

def saveFScoresTable(fscores, image_name):

    if(len(fscores) == 0):
        print("Empty fscores provided")
        return

    keys = list(fscores[0].keys())

    matrix = [getValues(fscores, i) for i in keys]

    table = go.Table(header=dict(values=keys), cells=dict(values=matrix))

    layout = dict(width=1200)

    fig = go.Figure(table, layout=layout)
    fig.write_image("./results/"+ image_name + ".png")

def getScores(name, realPos, realNeg, predPos, predNeg):
    print(name)
    intersection = sorted(list(set(realPos + realNeg) & set(predPos + predNeg)))
    labelsPred = ['positive' if word in predPos else 'negative' for word in intersection]
    labelsReal = ['positive' if word in realPos else 'negative' for word in intersection]
    report = classification_report(labelsReal, labelsPred, output_dict=True)
    print(classification_report(labelsReal, labelsPred))

    # We might have leave some unlabeled, so we count found ratio
    positiveFound = 100*len(set(predPos) & set(realPos))/len(realPos)
    negativeFound = 100*len(set(predNeg) & set(realNeg))/len(realNeg)
    print('Positives found: %.2f %%' % (positiveFound))
    print('Negatives found: %.2f %%' % (negativeFound))
    report['positive']['found'] = positiveFound
    report['negative']['found'] = negativeFound
    entry = {}
    entry[name] = report
    return entry


def clearOutputs(pred_pos, pred_neg):
    intersection = helper.intersection(pred_pos, pred_neg)
    pred_pos = helper.substract(pred_pos, intersection)
    pred_neg = helper.substract(pred_neg, intersection)

    return (pred_pos, pred_neg)

def printFscores(fscores):
    for fscore in fscores:
        print(fscore.toDict())

if __name__ == "__main__":
    pass
