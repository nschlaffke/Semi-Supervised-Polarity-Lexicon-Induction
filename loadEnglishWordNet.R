library(wordnet)

if(initDict()) {
  # get related terms
  filter <- getTermFilter("StartsWithFilter", "car", TRUE)
  terms <- getIndexTerms("NOUN", 5, filter)
  sapply(terms, getLemma)
  
  # get antonym
  filter <- getTermFilter("ExactMatchFilter", "hot", TRUE)
  terms <- getIndexTerms("ADJECTIVE", 5, filter)
  synsets <- getSynsets(terms[[1]])
  # this gets synonymous
  related <- getRelatedSynsets(synsets[[1]], "!")
  sapply(related, getWord)
  
  
}
