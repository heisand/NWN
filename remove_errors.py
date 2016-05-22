#coding="utf-8"

import re
import rdflib
from rdflib import URIRef, Literal
from rdflib.namespace import RDF
import parse_rdf

# Using rdflib's Graph to parse the rdf data

synsets = rdflib.Graph()
wordsenses = rdflib.Graph()
words = rdflib.Graph()

words.parse("reduced_words.rdf")
wordsenses.parse("reduced_wordsenses.rdf")
synsets.parse("reduced_synsets.rdf")

# Some useful URIs

nounSense = "http://www.w3.org/2006/03/wn/wn20/schema/NounWordSense"
verbSense = "http://www.w3.org/2006/03/wn/wn20/schema/VerbWordSense"
adjSense = "http://www.w3.org/2006/03/wn/wn20/schema/AdjectiveWordSense"
nounSynset = "http://www.w3.org/2006/03/wn/wn20/schema/NounSynset"
verbSynset = "http://www.w3.org/2006/03/wn/wn20/schema/VerbSynset"
adjSynset = "http://www.w3.org/2006/03/wn/wn20/schema/AdjectiveSynset"
contains = "http://www.w3.org/2006/03/wn/wn20/schema/containsWordSense"
lexform = "http://www.w3.org/2006/03/wn/wn20/schema/lexicalForm"
label = "http://www.w3.org/2000/01/rdf-schema#label"
word = "http://www.w3.org/2006/03/wn/wn20/schema/word"

non_syn_removed = set()
non_wordsen_removed = set()
syn_removed = set()
wordsen_removed = set()
unique_synsets = set()

# Creating a dictionary for the mapping between word id and word form.

lookup = {}
for s, p, o in words.triples((None, URIRef(lexform), None)):
	if s not in lookup:
		lookup[s] = set()
	lookup[s] = o.encode("utf-8")


# Locating and removing NoneSynsets and the wordsenses (hence also the
# NoneSenses) that belong to these synsets.

for s, p, o in synsets.triples((None, RDF.type, None)):
    unique_synsets.add(s)
    if "None" in o:
        for s2, p2, o2 in wordsenses.triples((s, None, None)):  # synset-id -> containsWordsense -> wordsense-id                
		non_wordsen_removed.add(o2)  
		wordsenses.remove((o2, None, None))
		wordsenses.remove((s2, None, None))
        non_syn_removed.add(s)
        synsets.remove((s, None, None))

misplaced_wordsen = set()
misplaced_wordid = set()
misplaced_lexform = set()
wrong_syn = set()

word_ids_removed = set()
lexform_removed = set()
unique_word_ids = set()
unique_lexform = set()


# Performing a check to find out if there are wordsenses
# that are misplaced according to their pos-tag and 
# the pos-tag of their synsets, if so, then removing both
# the word id, wordsense and synset.

def add_mismatch(a, b, c, d):
	misplaced_wordsen.add(a)
	misplaced_wordid.add(b)
	if b in  lookup:
		misplaced_lexform.add(lookup[b])	
	wrong_syn.add(d)

for s2, p2, o2 in wordsenses.triples((None, URIRef(word), None)):  # wordsense-id -> word -> word-id
	for s3, p3, o3 in wordsenses.triples((None, None, s2)):  # synset-id -> containswordsense -> wordsense-id
		if (s2, None, URIRef(nounSense)) in wordsenses and (s3, None, None) in synsets and (s3, None, URIRef(nounSynset)) not in synsets:
			add_mismatch(s2, o2, o, s3)
                elif (s2, None, URIRef(verbSense)) in wordsenses and (s3, None, None) in synsets and (s3, None, URIRef(verbSynset)) not in synsets:
 		  	add_mismatch(s2, o2, o, s3)
                elif (s2, None, URIRef(adjSense)) in wordsenses and (s3, None, None) in synsets and (s3, None, URIRef(adjSynset)) not in synsets:
			add_mismatch(s2, o2, o, s3)

for x in misplaced_wordsen:
	for s, p, o in wordsenses.triples((x, URIRef(word), None)):  # wordsense-id -> word word-id
		words.remove((o, None, None))
		for s2, p2, o2 in wordsenses.triples((None, None, x)):  # synset-id -> cointainswordsense -> wordsense-id
			synsets.remove((s2, None, None))
			wordsenses.remove((s2, None, None))
	wordsenses.remove((x, None, None))


# Checking if there are any synsets from wordsense.rdf which are not in synsets.rdf,
# and removing those. 

for s, p, o in wordsenses.triples((None, URIRef(contains), None)):  # synset-id -> containsWordSense -> wordsense-id
	if (s, None, None) not in synsets:
		syn_removed.add(s)
		synsets.remove((s, None, None))
		wordsen_removed.add(o)
		wordsenses.remove((o, None, None))
		wordsenses.remove((s, None, None))


# Checking if there are any words in wordsenses.rdf which are not in words.rdf,
# then removing them. And wordsenses that are not in a synset anymore.

no_word=set()
no_word_lexform=set()
no_word_wordsen=set()
no_synset=set()

for s6, p6, o6 in wordsenses.triples((None, URIRef(word), None)):
	if (o6, None, None) not in words:
		no_word_wordsen.add(s6)
		no_word.add(o6)
		wordsenses.remove((s6, None, None))
		wordsenses.remove((None, None, s6))
	if (None, None, s6) not in wordsenses and (s6, None, None) in wordsenses:
		wordsenses.remove((s6, None, None))
		no_synset.add(s6)


# Checking if there are any words which do not have a wordsense,   
# and removing those. 

no_sense=set()
no_sense_lexform=set()

#for s5, p5, o5 in words.triples((None, URIRef(lexform), None)):  
	#if (None, None, s5) not in wordsenses:
		#no_sense.add(s5)
		#no_sense_lexform.add(lookup[s5])
		#words.remove((s5, None, None))  
		
# Checking if there are any empty synsets, and removing those, i.e. synsets in synsets.rdf which are not in wordsenses.rdf

empty_syn = set()  

for s7, p7, o7 in synsets.triples((None, URIRef(label), None)):
	if (s7, None, None) not in wordsenses:
		empty_syn.add(s7)
		synsets.remove((s7, None, None))

synset = {}
synset_id = {}

# Looping over the words and their synsets, and
# providing each synset with a list of their word forms,
# to be able to count how many words there are in each synset.

for s8, p8, o8 in words.triples((None, URIRef(lexform), None)):
	for s9, p9, o9 in wordsenses.triples((None, None, s8)):  # wordsense-id -> word -> word-id
		for s10, p10, o10 in wordsenses.triples((None, None, s9)):  # synset-id -> containswordsense -> wordsense-id
			if (s10, None, None) in synsets:
				if s10 not in synset:
					synset[s10] = []
					synset_id[s10] = []
				synset[s10].append(lookup[s8])
				synset_id[s10].append(s8)

# Counting how many synsets that only have one word,
# have several words, and even have duplicates or more occurrences
# of the same word form. 

dupl_wordsen=set()

from collections import Counter
count_single = set()
count_multi = set()
count_dupl = set()
for k, v in synset.iteritems():
	if len(v)>1:
                a = dict(Counter(v))
                for i,j in a.iteritems():
                        if j>1:
                             count_dupl.add(k)
			     synsets.remove((k, None, None))
			     for s, p, o in wordsenses.triples((k, None, None)):
			        wordsenses.remove((o, None, None))
				dupl_wordsen.add(o)
			     wordsenses.remove((k, None, None))
				
                             #dupl_synsets.write("\n" + str(k) + " " + str(synset_id[k]) + " " + str(v))
                             break
                #print v
		count_multi.add(k)
                #multi_synsets.write("\n" + str(v))
                #multi_synsets.write("\n" + str(dict(Counter(v))))
	elif len(v)==1:
		#single_synsets.write("\n" + str(v))
                #print v
                count_single.add(k)

no_sen=set()
no_sen_lex=set()

for s5, p5, o5 in words.triples((None, URIRef(lexform), None)):  
	if (None, None, s5) not in wordsenses:
		no_sen.add(s5)
		no_sen_lex.add(lookup[s5])
		words.remove((s5, None, None))  
               

#single_synsets.write("\n" + str(count_single))
#multi_synsets.write("\n" + str(count_multi))
#dupl_synsets.write("\n" + str(count_dupl))

print "Results"

print len(words), len(wordsenses), len(synsets)

print len(count_single), len(count_multi), len(count_dupl)


print len(no_sen), len(no_sen_lex), len(no_sense), len(no_sense_lexform), len(no_word_wordsen), len(no_word)
print len(non_syn_removed), len(non_wordsen_removed), len(syn_removed), len(empty_syn), len(wordsen_removed), len(misplaced_wordsen), len(misplaced_wordid), len(misplaced_lexform), len(wrong_syn), len(no_synset), len(dupl_wordsen)
    
#synsets.serialize(destination="reduced_synsets2.rdf")
#wordsenses.serialize(destination="reduced_wordsenses2.rdf")
#words.serialize(destination="reduced_words2.rdf")

