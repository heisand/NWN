# coding=utf8
# Should be run with 4 arguments: synsets.rdf, wordsenses.rdf, words.rdf and hyponymOf.rdf (in that order).

import sys
file1 = sys.argv[1] # synsets.rdf
file2 = sys.argv[2] # wordsenses.rdf
file3 = sys.argv[3] # words.rdf
file4 = sys.argv[4] # hyponymOf.rdf

import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF

synsets = rdflib.Graph()
wordsenses = rdflib.Graph()
words = rdflib.Graph()
hyponymy = rdflib.Graph()
wordsenses = rdflib.Graph()

synsets.parse(file1)
wordsenses.parse(file2)
words.parse(file3)
hyponymy.parse(file4)
synsets.parse(file4) # merging synsets and hyponymOf     

# Some useful URIs.

hyp = URIRef("http://www.wordnet.dk/owl/instance/2009/03/schema/hyponymOf")
word = "http://www.w3.org/2006/03/wn/wn20/schema/word"
wordsense = "http://www.w3.org/2006/03/wn/wn20/schema/containsWordSense"
lexform = "http://www.w3.org/2006/03/wn/wn20/schema/lexicalForm"
nounURI = "http://www.w3.org/2006/03/wn/wn20/schema/NounWordSense"
verbURI = "http://www.w3.org/2006/03/wn/wn20/schema/VerbWordSense"
adjURI = "http://www.w3.org/2006/03/wn/wn20/schema/AdjectiveWordSense"
lexform = "http://www.w3.org/2006/03/wn/wn20/schema/lexicalForm"
word = "http://www.w3.org/2006/03/wn/wn20/schema/word"

lookup_id = {}
lookup_string ={}
unique_lex = set()

# Iterating over the words and their wordsenses, 
# and map word IDs to the lexical forms and vice versa.

for s, p, o in words.triples((None, URIRef(lexform), None)):
	for s2, p2, o2 in wordsenses.triples((None, URIRef(word), s)):
		if " " in o:
			a = "_".join(o.encode("utf-8").split())
    		else:
			a = o.encode("utf-8")
		if (s2, None, URIRef(nounURI)) in wordsenses:
			a += "_" + "subst"
		elif (s2, None, URIRef(verbURI)) in wordsenses:
			a += "_" + "verb"
		elif (s2, None, URIRef(adjURI)) in wordsenses:
			a += "_" + "adj"
			
    		if a not in unique_lex:
        		unique_lex.add(a)
        		lookup_id[a] = set()
    		lookup_id[a].add(s)
    		lookup_string[s] = a
		

