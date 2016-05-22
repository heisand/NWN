#coding:utf-8

import rdflib
from rdflib import URIRef, Literal

# Using rdflib's Graph to parse the rdf data

synsets = rdflib.Graph()
synsets_out = rdflib.Graph()
wordsenses = rdflib.Graph()
wordsenses_out = rdflib.Graph()
words = rdflib.Graph()
words_out = rdflib.Graph()

synsets.parse("synsets.rdf")
wordsenses.parse("wordsenses.rdf")
words.parse("words.rdf")

out = open("ouput_process2.txt", "w")

# Some useful URIs

label = "http://www.w3.org/2000/01/rdf-schema#label"
lexform = "http://www.w3.org/2006/03/wn/wn20/schema/lexicalForm"
word = "http://www.w3.org/2006/03/wn/wn20/schema/word"

# Creating a dictionary for a mapping between word ids and 
# word form.

lookup = {}

for h, i, j in words.triples((None, URIRef(lexform), None)):
	if h not in lookup:
		lookup[h] = set()
	lookup[h] = j.encode("utf-8")



#for s, p, o in synsets.triples((None, URIRef(label), None)):
	#if (s, None, None) not in wordsenses:
		#print s
		


ne_syn_removed = set()
ne_wordsen_removed = set()
ne_wordid_removed = set()
ne_wordform_removed = set()
multi_syn_removed = set()
multi_wordsen_removed = set()
multi_wordid_removed = set()
multi_wordform_removed = set()
multiwords = set()
find=1
ne_diff=set()
multi_diff=set()

# Looping over the synsets and locating and 
# removing named entities by checking for an upper-case letter 
# in the label. Synsets that have more than one word, and 
# have words with no upper-case letters as well as words with upper-case 
# letters, are not removed, i.e. are not treated named entities. 

# Also locating and removing multi-words. Though, if the synset contains
# both multi-words and single-words, the synset or multi-word will not be removed.

for s, p, o in synsets.triples((None, URIRef(label), None)):
    ne=0
    if any(x.isupper() for x in o) and "_" not in o:
	if "; " in o and "&amp;" not in o :  # The synset contains more than one word
		l = o.split("; ")
		for i in l:
			if any(y.isupper() for y in i):
				ne+=1
		if ne==len(l):
			ne_syn_removed.add(s)
							
	else:  
		ne_syn_removed.add(s)

for s in ne_syn_removed:
	for a, b, c in wordsenses.triples((s, None, None)):
		ne_wordsen_removed.add(c)
		for d, e, f in wordsenses.triples((c, URIRef(word), None)):
			if f in lookup: 
				ne_wordform_removed.add(lookup[f])
			else:
				ne_diff.add(f)  # Some words from wordsenses.rdf are apparently not in words.rdf
			ne_wordid_removed.add(f)
			words.remove((f, None, None))
		wordsenses.remove((c, None, None))
	wordsenses.remove((s, None, None))
	synsets.remove((s, None, None))
	

for s, p, o in synsets.triples((None, URIRef(label), None)): 
    multi=0
    test=False
    if "; " in o:
	l = o.split("; ")
        for i in l:
		if (" " in i):
			test = True
                        multi += 1
	if test == True and multi < len(l):
		find+=1  # If one wants to do something with the synsets like {spise opp; spise}
	elif test == True and multi == len(l):
		multi_syn_removed.add(s)			

    elif " " in o:
	multi_syn_removed.add(s)

for s in multi_syn_removed:
	for a, b, c in wordsenses.triples((s, None, None)):
		multi_wordsen_removed.add(c)
		for d, e, f in wordsenses.triples((c, URIRef(word), None)):
			if f in lookup: 
				multi_wordform_removed.add(lookup[f])
			else:
				multi_diff.add(f)  # Some words from wordsenses.rdf are apparently not in words.rdf
			multi_wordid_removed.add(f)
			words.remove((f, None, None))
		wordsenses.remove((c, None, None))
	wordsenses.remove((s, None, None))
	synsets.remove((s, None, None))


# If there are any empty synsets remaining, they will be removed. There won't be now, since I remove synsets when I remove wordsenses.

empty = set()

for s, p, o in synsets.triples((None, URIRef(label), None)):
	if (s, None, None) not in wordsenses:
		empty.add(s)
		#synsets.remove((s, None, None))
		

#synsets.serialize(destination='reduced_synsets.rdf')
#wordsenses.serialize(destination='reduced_wordsenses.rdf')
#words.serialize(destination='reduced_words.rdf')

#syn = open("reduced_synsets.rdf", "r").read()

#for s in multiword:
   # syn = syn.replace(s, "")
   # syn = syn.replace(" ; ", "")

#syn.close()

#newout = open("reduced_synsets.rdf", "w")
#newout.write(syn)
#newout.close()

