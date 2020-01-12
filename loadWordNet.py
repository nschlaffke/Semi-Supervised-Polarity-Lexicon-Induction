from nltk.corpus import wordnet as wn
import helper

def getName(value):
    return value.name()

def getNames(values):
    return list(map(getName, values))

def getSynsetLemmas(synset):
    return synset.lemmas()

def getSynsetNames(synset):
    lemmas = synset.lemmas()
    return lemmas

def findSynsetSynonymsSynset(synset):
    synonyms = []
    for lemma in synset.lemmas():
        synonyms.append(wn.synsets(lemma.name()))
    
    return helper.flatten_unique(synonyms)

def findSynonymsSynset(synset):
    synonyms = []
    for lemma in synset.lemmas():
        synonyms.append(findSynonymsLemma(lemma))
    return helper.flatten_unique(synonyms)

def findSynonymsLemma(lemma):
    synonymsSynset = wn.synsets(lemma.name())
    return helper.flatten_unique(list(map(getSynsetLemmas, synonymsSynset)))

def getAllLemmas(words_synsets):
    lemmas = []
    for word_synset in words_synsets:
        lemmas = lemmas + getSynsetNames(word_synset)
    return lemmas

if __name__ == "__main__":
    good = wn.synset('good.a.01')
    lemmas = findSynsetSynonymsSynset(good)
    print(getNames(lemmas))
