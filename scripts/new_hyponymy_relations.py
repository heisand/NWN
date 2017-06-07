#coding="utf-8"

# Under revision

import parse_rdf
import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF
import sys

file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]
file4 = sys.argv[4]

hyponymy = rdflib.Graph()
synsets = rdflib.Graph()

hyponymy.parse(file1)
synsets.parse(file2)
synsets.parse(file1)  # Merging synsets and hyponymOf

hypernym_set = {}

# Mapping every synsets to their immediate hypernyms. 

for s, p, o in synsets:
	for s2, p2, o2 in hyponymy.triples((s, None, None)):
		if s not in hypernym_set:
			hypernym_set[s] = set()
		hypernym_set[s].add(o2)

added = set()

# Iterating over the original synsets, and adding new hyponymy relations
# where removing the immediate one has removed link to hypernym ancestors. 

for s, p, o in synsets:
	count = 0
	synset.add(s)
	if (s, None, None) not in parse_rdf.wordsenses:
		continue
	for i in synsets.transitive_objects(s, parse_rdf.hyp):
		count += 1
		if count == 1:
			continue
		if (i, None, None) not in parse_rdf.wordsenses and (s, None, i) in hyponymy:
			if i in hypernym_set:
				for a in hypernym_set[i]:
					if (a, None, None) in parse_rdf.wordsenses and str([s, a]) not in added:
						hyponymy.add((s, URIRef("http://www.wordnet.dk/owl/instance/2009/03/schema/hyponymOf"), a))
						added.add(str([s, a]))
					elif (a, None, None) not in parse_rdf.wordsenses and (a, None, None) in hyponymy:
						for b in hypernym_set[a]:
							if (b, None, None) in parse_rdf.wordsenses and str([s, b]) not in added:
								hyponymy.add((s, URIRef("http://www.wordnet.dk/owl/instance/2009/03/schema/hyponymOf"), b))
								added.add(str([s, b]))
			break

# Iterating over hyponymy relations and removing relations for 
# synsets that have been removed. 

for s, p, o in hyponymy:
	if (s, None, None) not in parse_rdf.wordsenses:
		hyponymy.remove((s, None, None))
		hyponymy.remove((None, None, s))
	if (o, None, None) not in parse_rdf.wordsenses:
		hyponymy.remove((o, None, None))
		hyponymy.remove((None, None, o))

hyponymy.serialize(destination="reduced_hyponymOf.rdf")
