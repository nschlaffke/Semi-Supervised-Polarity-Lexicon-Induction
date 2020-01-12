
import helper
import plotly.graph_objects as go

class FScore:
    def __init__(self, name, real_positives, real_negatives, predicted_positives, predicted_negatives):

        self.name = name

        true_positives = helper.intersection(real_positives, predicted_positives)
        true_negatives = helper.intersection(real_negatives, predicted_negatives)
        false_positives = helper.intersection(real_negatives, predicted_positives)
        false_negatives = helper.intersection(real_positives, predicted_negatives)

        self.precision = len(true_positives)/(len(true_positives) + len(false_positives))
        self.recall = len(true_positives)/(len(true_positives) + len(false_negatives))
        self.fscore = 2*self.precision*self.recall/(self.precision + self.recall)

        self.positive_hit_ratio = len(true_positives)/len(predicted_positives)
        self.negative_hit_ratio = len(true_negatives)/len(predicted_negatives)

        self.positive_found_ratio = len(true_positives)/len(real_positives)
        self.negative_found_ratio = len(true_negatives)/len(real_negatives)
    
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
 

def fscore(score_name, real_positives, real_negatives, predicted_positives, predicted_negatives):
    return FScore(score_name, real_positives, real_negatives, predicted_positives, predicted_negatives)

def correctedFscore(score_name, real_positives, real_negatives, predicted_positives, predicted_negatives, values):
    # we want to filter the values for actually the possible ones, if the graph wasn't covering all the words
    # it's normal we don't find them, they were not included in the graph in first place!
    real_positives = helper.intersection(real_positives, values)
    real_negatives = helper.intersection(real_negatives, values)

    return fscore(score_name, real_positives, real_negatives, predicted_positives, predicted_negatives)


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

def printFscores(fscores):
    for fscore in fscores:
        print(fscore.toDict())
