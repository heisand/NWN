# coding=utf8

import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF
import os

synsets = rdflib.Graph()
wordsenses = rdflib.Graph()
words = rdflib.Graph()
hyponymy = rdflib.Graph()
wordsenses = rdflib.Graph()

synsets.parse("reduced_synsets.rdf")
wordsenses.parse("reduced_wordsenses2.rdf")
words.parse("reduced_words2.rdf")
hyponymy.parse("reduced_hyponymOf.rdf")
synsets.parse("reduced_hyponymOf.rdf") # merging synsets and hyponymOf     

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
		

