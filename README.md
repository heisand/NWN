# mod-wordnet
This repository provides a wordnet resource for Norwegian, which is a modification of [Norwegian Wordnet - Bokmål](http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en).

## Summary of the project

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

A number of changes was made to the original resource:
- Correction of syntax errors
- Removal of proper nouns and multi word expressions
- Removal of structural and other errors

## Dataset
`synsets.rdf`:  Declares the synsets.

`wordsenses.rdf`: Connects synsets and words.

`words.rdf`:  Declares the words and their lexical form.

`hyponymOf.rdf`:  Connects synsets by hyponym relations.

## Scripts
`correct_syntax_errors.py`: Corrects the syntax errors found.

`new_hyponymy_relations.py`:  Creates hyponym relations for synsets.	

`parse_rdf.py`: Parses the rdf-files using the Python package RDFLib.

`remove_errors.py`: Removes structural and other errors from the wordnet.

`remove_ne+multi.py`: Removes proper nouns and multi word expressions from the wordnet.

## References
The Language Bank by the National Library of Norway has the origin of the resource, and the 
the original wordnet resource can be found at http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en.
