# NWN
This repository provides a wordnet resource for Norwegian. It is a modification of [Norwegian Wordnet - Bokmål](http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en), which is supplied in an extension of the 
W3C's RDF/OWL Representation of wordnets ([RDF/OWL Representation of WordNet](http://www.w3.org/TR/wordnet-rdf/)).

A wordnet can be useful in many NLP tasks, e.g.:

- Word sense disambiguation: assigning the correct sense to a word according to the wordnet and a given corpus. 
- Query expansion or reformulation: expand or reformulate queries with synonyms and related words from the wordnet.

## Statistics over the wordnet

| PoS | Lexical forms        | Synsets          | Senses  |
|:----- | ---------: |--------:| -----:|
| Noun | 38,440     | 43,112 | 48,865 |
| Verb | 2,816      | 4,967      |   5,580 |
| Adjective | 2,877 | 3,179      |    3,571 |
| Total | 44,133 | 51,258      |    58,016 |

## Summary of the project
### Modifying the wordnet
A number of changes was made to the original resource:
- Correction of syntax errors, e.g. mismatches between start and end tags in the xml-syntax.
- Removal of proper nouns and multi word expressions, mostly due to problems with parsing the big amount of data when proper nouns and multi words were included. 
- Removal of structural and other errors, e.g. synsets with duplicate occurrences of words.

Scripts for modifying the original resource are provided in this repository. 

### Experiments on extending the wordnet 
New words are constantly formed, but it is highly expensive to manually extend and maintain such taxonomies. Wordnets then tend to suffer from inefficient coverage. An attempt to extend the Norwegian Wordnet was performed by discovering new hypernym relations based on word embeddings and a scoring function for hypernyms (based on [Yamada et al. 2009](http://www.aclweb.org/anthology/D09-1097)).

For a target word, a set of the _k_ most similar words are computed. The hypernyms in the wordnet for these words are possible hypernyms for the target word. The hypernym with the highest score is selected as the hypernym of the target word, where the score is based on a combination distributional similarity and the hierarchical structure of the wordnet. 

A script for scoring hypernyms is provided in this repository.

Note that 47,914 of the 51,258 synsets actually are top nodes, i.e. NWN-reduced has a very flat structure. 
                                    
## Using the wordnet

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

The following illustrates how to parse a rdf file with RDFLib, iterate over the contained triples, adding/removing triples and serializing the graph in a given format.

*import rdflib*

*g = Graph()*

*someGraph = g.parse("some.rdf")*

*for subject, predicate object in someGraph:*
  *#do something*
  
*someGraph.add((subject, predicate, object))*

*someGraph.remove((subject, predicate, object))*

*s = someGraph.serialize(format='nt')*

## Cmputing word embeddings

- [Word2vec](https://code.google.com/archive/p/word2vec/)
- [Gensim](https://radimrehurek.com/gensim/)

Word2vec through the free Python library Gensim can be used to compute word embeddings, which was used in this project. Tutorials for using word2vec with genism are found at https://radimrehurek.com/gensim/models/word2vec.html and https://rare-technologies.com/word2vec-tutorial/.
The input to word2vec is a text corpus, and the word embeddings are produced as output. 

## Dataset
The dataset of NWN consists of several rdf-files. RDF is the world Wide Web Consortium standard for encoding knowledge, 
where almost everything is defined as a resource. The resources are identified by Uniform Resource Identifiers, e.g. a synset with URI http://www.wordnet.dk/owl/instance/2009/03/instances/synset-60504. The information in RDF is expressed using triples of subjects, objects and predicates, where a predicate for instane could be a hyponym relationship or property between two synsets.

The WordNet schema has three main classes: Synset, WordSense and Word. Synset and Wordsense also have subclasses for the parts of speech in WordNet. A synset contains one or more word senses, but each word sense only belongs to one synset. Each word has in turn exactly one word to represent its lexical form, but one word can be represented by one or more word senses. 


`synsets.rdf`:  Declares the synsets.

`wordsenses.rdf`: Connects synsets and words.

`words.rdf`:  Declares the words and their lexical form.

`hyponymOf.rdf`:  Connects synsets by hyponym relations.

`NWN.owl`: OWL-file to build the ontology in Protégé.

## Scripts
### Modification
The following scripts where used to create the modified version of the Norwegian Wordnet:

`correct_syntax_errors.py`: The original wordnet contained different kinds of xml syntax errors. The script corrects these syntax errors throughout the rdf-files. 

`new_hyponymy_relations.py`:  Synsets were removed during the removal of proper nouns and multi word expressions, as well as other synsets which were a part of other types of errors. This removed intermediate hypernym relations, and hence also transitive hypernym relations to other ancestors. This script then creates transitive hypernym relations for the synsets that are left behind. 

`parse_rdf.py`: To work with the wordnet, this script parses the necessary rdf-files using the Python package RDFLib.

`remove_errors.py`: Some structural errors according to the structure of a wordnet, as well as some other errors in the rdf-files, occured. This script removes these errors from the wordnet. 

`remove_ne+multi.py`: The original wordnet contains a quantity of proper nouns and multi word expressions. This script removes the instances of these.

### Scoring hypernyms for new words

`score_hypernym.py`: Calculates scores for hypernym candidates of a target word and yields the highest scoring hypernym for each target word.

## Manual inspection of results

| Score| Target word  | Predicted hypernym  |
|:----- | ---------: |--------:|
| 5.29 | sm{\aa}rolling \textit{toddler}      | \{barn \textit{child}; menneskebarn \textit{human child}\} | 
| 4.74 | utskudd      | \textit{bully} &\{person \textit{person}; menneske \textit{human}; individ\textit{individual}\}  |   
| 4.41 | kulturprodukt | \textit{culture product} &\{effekt \textit{effect}; gjenstand \textit{object}; ting \textit{thing}\}  |   
| 3.59 | venezuelaner | \textit{Venezualian} &\{statsborger \textit{citizen}\}  |    
| 2.41 | zoonose | \textit{zoonosis} &\{syke \textit{illness}; sykdom \textit{disease}; lidelse \textit{suffering}\} |  
| 2.38 | m{\aa}lscorer | \textit{goalscorer} &\{ballspiller \textit{ball player}; spiller \textit{player}\} |  
| 2.20 | rev | \textit{fox} &\{dyr \textit{animal}; dyreart \textit{animal specie}\} |  
| 1.78 | mateple | \textit{food apple} &\{eple \textit{apple}\}    |  
| 1.75 | rekordavling | \textit{record harvest} &\underline{\{handelsvare \textit{commodity}\}}   |  
| 1.64 | funn | \textit{find} &\underline{\{skip \textit{ship}; skute \textit{ship}\}} |  
| 1.62 | tippoldebarn |  \textit{great-grandchild} &\{barn \textit{child}\}    |  
| 1.50 |  dykker | \textit{god mother}&\{mor \textit{mother}; moder \textit{mother}; mamma \textit{mom}\} |  


#### Emples of correct predictions:

- Slagvåpen ’hitting weapon’

 Predicted:
 {håndvåpen ’hand weapon’; handvåpen ’hand weapon’}

 Correct:
 {håndvåpen ’hand weapon’; handvåpen ’hand weapon’}

- Superstjerne ’super star’

 Predicted:
 {person ’person’; hode ’head’; menneske ’human’; individ ’individual’}

 Correct:
 {person ’person’; hode ’head’; menneske ’human’; individ ’individual’}
 
#### Examples of predictions that are not completely correct, but not entirely wrong either:

- svigermor ’mother in law’

 Predicted:
 {mor ’mother’; moder ’mother’; mamma ’mum’}

 Correct:
 {dame ’woman’; kvinne ’woman’; kvinnemenneske ’woman’; hunkjønn ’female’; fruentimmer ’woman’; hokjønn ’female’}
 
- stesønn ’step son’

 Predicted:
 {hr. ’mr.’; mann ’man’; herre ’man’; mannsperson ’man person’; hannkjønn ’male’; herr ’mister’}
 
 Correct:
 {sønn ’son’}
 
- skolebarn ’school child’

 Predicted:
 {elev ’student’}
 
 Correct:
 {barn ’child’; menneskebarn ’human child’}
 
 - forsvarsspiller ’defense player’
 
 Predicted:
 {fotballspiller ’football player’; fotballspeller ’football player’}
 
 Correct:
 {ballspiller ’ball player’; spiller ’player’; speller ’player’}

## References
The Language Bank by the National Library of Norway has the origin of the resource, and the 
the original wordnet resource can be found at http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en.
