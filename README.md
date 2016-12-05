# mod-wordnet
This repository provides a wordnet resource for Norwegian. It is a modification of [Norwegian Wordnet - Bokmål](http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en), which is supplied in an extension of the 
W3C's RDF/OWL Representation of wordnets ([RDF/OWL Representation of WordNet](http://www.w3.org/TR/wordnet-rdf/)).

## Statistics over the wordnet

| PoS | Lexical forms        | Synsets          | Senses  |
|:----- | ---------: |--------:| -----:|
| Noun | 38,440     | 43,112 | 48,865 |
| Verb | 2,816      | 4,967      |   5,580 |
| Adjective | 2,877 | 3,179      |    3,571 |
| Total | 44,133 | 55,258      |    58,016 |

## Summary of the project
### Modifying the wordnet
A number of changes was made to the original resource:
- Correction of syntax errors
- Removal of proper nouns and multi word expressions
- Removal of structural and other errors

### Extending the wordnet by discovering new hypernym relations based on word embeddings and a scoring function for hypernyms

## Using the wordnet
It is possible to navigate the resource in the Protégé software. The software is
available from the web site http://protege.stanford.edu/. The wordnet can be loaded by 
opening NWN.owl from the file menu. Note that the owl format is an instance model and it is
therefore not immediately possible to view the resource as a tree structure.


The Python package RDFLib can be used to work with the RDF format. RDFLib contains most things you need to work with RDF, 
including: 
- parsers and serializers for RDF/XML, N3, NTriples, N-Quads, Turtle, TriX, RDFa and Microdata.
- a Graph interface which can be backed by any one of a number of Store implementations.
store implementations for in memory storage and persistent storage on top of the Berkeley DB.
- a SPARQL 1.1 implementation - supporting SPARQL 1.1 Queries and Update statements.

https://rdflib.readthedocs.io/en/stable/index.html provides a guide of how to use RDFLib.

## Dataset
`synsets.rdf`:  Declares the synsets.

`wordsenses.rdf`: Connects synsets and words.

`words.rdf`:  Declares the words and their lexical form.

`hyponymOf.rdf`:  Connects synsets by hyponym relations.

`NWN.owl`: 

## Scripts
The following scripts where used to create the modified version of the Norwegian Wordnet:

`correct_syntax_errors.py`: The original wordnet contained different kinds of xml syntax errors. The script these syntax errors throughout the rdf files. 

`new_hyponymy_relations.py`:  Synsets were removed during the removal of proper nouns and multi word expressions, as well as other synsets which were a part of other types of errors. This removed intermediate hypernym relations, and hence also transitive hypernym relations to other ancestors. This script then creates transitive hypernym relations for the synsets that are left behind. 

`parse_rdf.py`: To work with the wordnet, this script parses the necessary rdf-files using the Python package RDFLib.

`remove_errors.py`: Some structural errors according to a wordnet, as well as some other errors in the rdf-files, occured. This script removes these errors from the wordnet. 

`remove_ne+multi.py`: The original wordnet contains a quantity of proper nouns and multi word expressions. This script removes the instances of these.

## References
The Language Bank by the National Library of Norway has the origin of the resource, and the 
the original wordnet resource can be found at http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en.
