from sklearn.metrics import classification_report

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