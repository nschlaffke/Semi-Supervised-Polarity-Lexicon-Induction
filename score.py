
import helper
import plotly.graph_objects as go
import pandas as pd


class FScore:
    def __init__(self, precision, recall, name = ""):
        self.name = name
        self.precision = precision
        self.recall = recall
        self.fscore = 2*precision*recall/(precision + recall)
    
    def setName(self, name):
        self.name = name

    def toDict(self):
        return {
            'name': self.name,
            'precision': self.precision,
            'recall': self.recall,
            'fscore': self.fscore
        }

    def toList(self):
        return [self.name, self.precision, self.recall, self.fscore]

    def print(self):
        print(self.toDict())
        

def fscore(score_name, real_positives, real_negatives, predicted_positives, predicted_negatives):
    true_positives = helper.intersection(real_positives, predicted_positives)
    false_positives = helper.intersection(real_negatives, predicted_positives)
    false_negatives = helper.intersection(real_positives, predicted_negatives)

    precision = len(true_positives)/(len(true_positives) + len(false_positives))
    recall = len(true_positives)/(len(true_positives) + len(false_negatives))

    return FScore(precision, recall, score_name)


def saveFScoresTable(fscores, image_name):

    fscores_dict = { fscores[i].name : fscores[i].toList() for i in range(0, len(fscores) ) }
    fscores_DF = pd.DataFrame.from_dict(fscores_dict, orient='index', columns=['Name', 'Precision', 'Recall', 'Fscore'])

    table = go.Table(header=dict(values=list(fscores_DF.columns)), cells=dict(values=[fscores_DF.Name,
        fscores_DF.Precision, fscores_DF.Recall, fscores_DF.Fscore]))

    fig = go.Figure(table)
    fig.write_image("./results/"+ image_name + ".png")
