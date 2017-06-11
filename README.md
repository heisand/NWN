# NWN
This repository provides a wordnet resource for Norwegian. It is a modification of [Norwegian Wordnet - Bokmål](http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en), which is supplied in an extension of the 
W3C's RDF/OWL Representation of wordnets ([RDF/OWL Representation of WordNet](http://www.w3.org/TR/wordnet-rdf/)).

A wordnet can be useful in many NLP tasks, e.g.:

- Word sense disambiguation: assigning the correct sense to a word according to the wordnet and a given corpus. 
- Query expansion or reformulation: expand or reformulate queries with synonyms and related words from the wordnet.

See section 'Summary of the project' for more information of the projet.

## Dataset
The dataset of NWN consists of several rdf-files. RDF is the world Wide Web Consortium standard for encoding knowledge and is expressed using triples of subjects, objects and predicates.

The WordNet schema has three main classes: Synset, WordSense and Word. Synset and Wordsense also have subclasses for the parts of speech in WordNet. A synset contains one or more word senses, but each word sense only belongs to one synset. Each word has in turn exactly one word to represent its lexical form, but one word can be represented by one or more word senses. 

`synsets.rdf`:  Declares the synsets.

`wordsenses.rdf`: Connects synsets and words.

`words.rdf`:  Declares the words and their lexical form.

`hyponymOf.rdf`:  Connects synsets by hyponym relations.

`NWN.owl`: OWL-file to build the ontology in Protégé.

## Scripts
### Modification
The following scripts where used to create the modified version of NWN:

`correct_syntax_errors.py`: The original resource contained different kinds of xml syntax errors. The script corrects these syntax errors throughout the rdf-files. 

`new_hyponymy_relations.py`:  Synsets were removed during the removal of proper nouns and multi word expressions, as well as other synsets which were a part of other types of errors. This removed intermediate hypernym relations, and hence also transitive hypernym relations to other ancestors. This script then creates transitive hypernym relations for the synsets that are left behind. 

`parse_rdf.py`: To work with NWN, this script parses the necessary rdf-files using the Python package RDFLib.

`remove_errors.py`: Some structural errors according to the structure of a wordnet, as well as some other errors in the rdf-files, occured. This script removes these errors from NWN. 

`remove_ne+multi.py`: The original resource contained a quantity of proper nouns and multi word expressions. This script removes the instances of these.

### Scoring hypernyms for new words

`score_hypernym.py`: Calculates scores for hypernym candidates of a target word and yields the highest scoring hypernym for each target word.

### Running the scripts

## Navigating NWN

- [Protégé](http://protege.stanford.edu/)
- [RDFLib](https://rdflib.readthedocs.io/en/stable/index.html)

It is possible to navigate the resource in the Protégé software. The software is
available from the web site http://protege.stanford.edu/. The wordnet can be loaded by 
opening `NWN.owl` from the file menu. Note that the owl format is an instance model and it is
therefore not immediately possible to view the resource as a tree structure.

The Python package RDFLib can further be used to work with the RDF format. RDFLib contains most things needed to work with RDF, 
including: 
- parsers and serializers for RDF/XML, N3, NTriples, N-Quads, Turtle, TriX, RDFa and Microdata.
- a Graph interface which can be backed by any one of a number of Store implementations.
store implementations for in memory storage and persistent storage on top of the Berkeley DB.
- a SPARQL 1.1 implementation - supporting SPARQL 1.1 Queries and Update statements.

https://rdflib.readthedocs.io/en/stable/index.html provides a guide of how to install and use RDFLib.

The following code snippet illustrates how to parse a rdf file with RDFLib, iterate over the contained triples, adding/removing triples and serializing the graph in a given format.

*import rdflib*

*g = Graph()*

*someGraph = g.parse("some.rdf")*

*for subject, predicate, object in someGraph:*
  *#do something*
  
*someGraph.add((subject, predicate, object))*

*someGraph.remove((subject, predicate, object))*

*s = someGraph.serialize(format='nt')*

## Summary of the project
### Modifying NWN
A number of changes was made to the original resource:
- Correction of syntax errors.
- Removal of proper nouns and multi word expressions.
- Removal of structural and other errors.

Scripts for modifying the original resource are provided in this repository. 

#### Statistics for the modified NWN

| PoS | Lexical forms        | Synsets          | Senses  |
|:----- | ---------: |--------:| -----:|
| Noun | 38,440     | 43,112 | 48,865 |
| Verb | 2,816      | 4,967      |   5,580 |
| Adjective | 2,877 | 3,179      |    3,571 |
| Total | 44,133 | 51,258      |    58,016 |

### Experiments on extending NWN
New words are constantly formed, but it is highly expensive to manually extend and maintain such taxonomies. Wordnets then tend to suffer from inefficient coverage. An attempt to extend the Norwegian Wordnet was performed by discovering new hypernym relations based on word embeddings and a scoring function for hypernyms (based on [Yamada et al. 2009](http://www.aclweb.org/anthology/D09-1097)).

For a target word, a set of the _k_ most similar words are computed. The hypernyms in the wordnet for these words are possible hypernyms for the target word. The hypernym with the highest score is selected as the hypernym of the target word, where the score is based on a combination distributional similarity and the hierarchical structure of the wordnet. 

A script for scoring hypernyms is provided in this repository.

Note that 47,914 of the 51,258 synsets actually are top nodes, i.e. NWN-reduced has a very flat structure.          

#### Computing word embeddings

- [Word2vec](https://code.google.com/archive/p/word2vec/)
- [Gensim](https://radimrehurek.com/gensim/)

Word2vec through the free Python library Gensim can be used to compute word embeddings, which was used in this project. Tutorials for using word2vec with genism are found at https://radimrehurek.com/gensim/models/word2vec.html and https://rare-technologies.com/word2vec-tutorial/.
The input to word2vec is a text corpus, and the word embeddings are produced as output. 

#### Example of predictions

| Score| Target word  | Predicted hypernym  |
|-----: | :--------- |:--------|
| 5.29 | smårolling *toddler*      | \{barn *child*; menneskebarn *human child*\} | 
| 4.74 | utskudd *bully*  | \{person *person*; menneske *human*; individ *individual*\}  |   
| 4.41 | kulturprodukt *culture product* | \{effekt *effect*; gjenstand *object*; ting *thing*\}  |   
| 3.59 | venezuelaner *Venezualian* |  \{statsborger *citizen*\}  |    
| 2.41 | zoonose *zoonosis*  | \{syke *illness*; sykdom *disease*; lidelse *suffering*\} |  
| 2.38 | målscorer *goalscorer* |  \{ballspiller *ball player*; spiller *player*\} |  
| 2.20 | rev *fox*  | \{dyr *animal*; dyreart *animal specie*\} |  
| 1.78 | mateple *food apple*  | \{eple *apple*\}    |  
| 1.75 | rekordavling *record harvest* | \{handelsvare *commodity*\}   |  
| 1.64 | funn  *find*  | \{skip *ship*; skute *ship*\} |  
| 1.62 | tippoldebarn  *great-grandchild* |  \{barn *child*\}    |  
| 1.50 | dykker  *diver* | \{fartøy *vessel*\} |  

## References
The Language Bank by the National Library of Norway has the origin of the resource, and the 
the original wordnet resource can be found at http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en.

Please cite the following paper if you use the data sets or scripts in academic works:
>Sand, H., Velldal, E., Øvrelid, L. (2017). [Wordnet extension via word embeddings:
>Experiments on the Norwegian Wordnet](http://aclweb.org/anthology/W/W17/W17-0242.pdf). 
>In *Proceedings of the 21st Nordic Conference on
>Computational Linguistics (NoDaLiDa)* (pp. 298-302). Gothenburg, Sweden.
