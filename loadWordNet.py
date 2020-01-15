from nltk.corpus import wordnet as wn
import helper

def getName(value):
    return value.name()

def getNames(values):
    return helper.unique(map(getName, values))

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

def findRelatedSynsets(synset):
    return synset.similar_tos() + synset._related('n') + synset.also_sees()

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

def getSynset(lemma):
    return wn.synsets(lemma)[0]

def getSynsets(lemma):
    return wn.synsets(lemma)

def fromSynsetsToLemmas(synsets):
    lemmas = set()
    for synset in synsets:
        try:
            lemmas = lemmas | set(getSynsetLemmas(wn.synset(synset)))
        except ValueError:
            continue
        
    return getNames(list(lemmas))

def convertIf(words, needsSynset):
    if(needsSynset):
        words = list(map(getSynset, words))
    return words

if __name__ == "__main__":
    good = wn.synset('good.a.01')
    lemmas = findSynsetSynonymsSynset(good)
    print(getNames(lemmas))
