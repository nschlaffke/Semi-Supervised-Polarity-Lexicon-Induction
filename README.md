# Semi-Supervised-Polarity-Lexicon-Induction
Implementation of the paper: https://pdfs.semanticscholar.org/841c/52958004893b21bee9d6f8373e8a279f76c7.pdf


# Professor notes
Regarding the project that you are developing I am sending you here a .zip containing several vectors of words with different sentiment emotions and more linked to financial texts. It is the Loughran-McDonald Sentiment Word Lists - which I am sending to you in vectors compressed in .rda format which you can easily load into R.   the LM sentiment words are classified in the following  categories Negative, Positive, Uncertainty, Litigious, Strong Modal, Weak Modal, Constraining. I would like you to test the effectiveness of the graph-based dictionary finding algorithm that you are to developed on this dataset. This means to embed say the negative and positive dictionaries (LMDnegative, LMDpositive) into WordNEt and starting from a seed of each see if it correctly finds the rests or others. Same, and more interestingly, will be to do similar exploration with the other categories (LMDuncertainty, LMDsuperfluous, etc) as these emotions are not so clear as positive negative, it would be interesting to see if other words carrying those particular emotions are found in WordNet through the links of synonyms and hypernyms.
Here is a page that explains the Loughran-McDonald dictionary with link to their original paper
https://sraf.nd.edu/textual-analysis/resources/

A further extension of this project, which I think you can explore without much extra effort is the possibility of using antonyms relations in the graph. As the authors of the paper you are studying propose at the end,  beware that 
"Antonym edges cannot be added in a straight-forward way to the graph for label propagation as antonymy encodes negative similarity (or dissimilarity) and the dissimilarity relation is not transitive.”
Can you think of a way of adding antonym edges? One idea , but I am not sure if it works, would be to define the graph of antonym edges and then work with the complementary graph (a non-edge becomes an edge and vice versa).. but this might be too simple.

Other ideas is to explore/propose other relatives finding algorithms besides label propagation (any of the clustering algorithms seen in class)

do a good job!