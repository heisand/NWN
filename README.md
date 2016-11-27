# mod-wordnet
This repository provides a wordnet resource for Norwegian, which is a modification of [Norwegian Wordnet - Bokmål](http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en)

## Summary of the project
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
`correct_syntax_errors.py`

`new_hyponymy_relations.py`	

`parse_rdf.py`	

`remove_errors.py`	

`remove_ne+multi.py`

## References
The Language Bank by the National Library of Norway has the origin of the resource, and the 
the original wordnet resource can be found at http://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-27&lang=en
