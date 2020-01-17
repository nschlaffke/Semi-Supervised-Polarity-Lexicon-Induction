
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

        self.p_precision = report["positive"]["precision"]
        self.p_recall = report["positive"]["recall"]
        self.p_f1 = report["positive"]["f1-score"]

        self.n_precision = report["negative"]["precision"]
        self.n_recall = report["negative"]["recall"]
        self.n_f1_score = report["negative"]["f1-score"]

        self.w_precision = report["weighted avg"]["precision"]
        self.w_recall = report["weighted avg"]["recall"]
        self.w_f1 = report["weighted avg"]["f1-score"]

        self.p_found = report['positive']['found']
        self.n_found = report['negative']['found']

        self.o_p_found = report['positive']['original_found']
        self.o_n_found = report['negative']['original_found']
    
    def setName(self, name):
        self.name = name

    def toDict(self):
        return vars(self)

    def toList(self):
        return list(self.toDict().values())

    def keys(self):
        return self.toDict().keys()
 

def fscore(score_name, realPos, realNeg, origPos, origNeg, predPos, predNeg):
    intersection = sorted(list(set(realPos + realNeg) & set(predPos + predNeg)))
    labelsPred = ['positive' if word in predPos else 'negative' for word in intersection]
    labelsReal = ['positive' if word in realPos else 'negative' for word in intersection]
    report = classification_report(labelsReal, labelsPred, output_dict=True)
    print(classification_report(labelsReal, labelsPred))

    # We might have leave some unlabeled, so we count found ratio
    positiveFound = 100*len(set(predPos) & set(realPos))/len(realPos)
    negativeFound = 100*len(set(predNeg) & set(realNeg))/len(realNeg)
    
    realPositiveFound = 100*len(set(predPos) & set(origPos))/len(origPos)
    realNegativeFound = 100*len(set(predPos) & set(origPos))/len(origPos)

    # print('Positives found: %.2f %%' % (positiveFound))
    # print('Negatives found: %.2f %%' % (negativeFound))
    report['positive']['found'] = '{0:.2f}'.format(positiveFound)
    report['negative']['found'] = '{0:.2f}'.format(negativeFound)
    report['positive']['original_found'] = '{0:.2f}'.format(realPositiveFound)
    report['negative']['original_found'] = '{0:.2f}'.format(realNegativeFound)

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

def clearOutputs(pred_pos, pred_neg):
    intersection = helper.intersection(pred_pos, pred_neg)
    pred_pos = helper.substract(pred_pos, intersection)
    pred_neg = helper.substract(pred_neg, intersection)

    return (pred_pos, pred_neg)


if __name__ == "__main__":
    pass
