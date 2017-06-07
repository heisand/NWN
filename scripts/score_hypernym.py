# coding=utf8

# Under revision
 
import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF
import os
import gensim

synsets = rdflib.Graph()
wordsenses = rdflib.Graph()
words = rdflib.Graph()
hyponymy = rdflib.Graph()
wordsenses = rdflib.Graph()

synsets.parse("path to synsets.rdf")
wordsenses.parse("path to wordsenses.rdf")
words.parse("path to words.rdf")
hyponymy.parse("path to hyponymy.rdf")
synsets.parse("path to synsets.rdf") # merging synsets and hyponymOf

hyp = URIRef("http://www.wordnet.dk/owl/instance/2009/03/schema/hyponymOf")

lookup_id = {}
lookup_string = {}
unique_lex = set()

word = "http://www.w3.org/2006/03/wn/wn20/schema/word"
wordsense = "http://www.w3.org/2006/03/wn/wn20/schema/containsWordSense"
lexform = "http://www.w3.org/2006/03/wn/wn20/schema/lexicalForm"
nounURI = "http://www.w3.org/2006/03/wn/wn20/schema/NounWordSense"
verbURI = "http://www.w3.org/2006/03/wn/wn20/schema/VerbWordSense"
adjURI = "http://www.w3.org/2006/03/wn/wn20/schema/AdjectiveWordSense"
t = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

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
        
def lookup_ID(word):
    return lookup_id[word]

def lookup_str(ID):
    return lookup_string[ID]

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
	for line in open(self.dirname):
		yield line.split()

# sentences = MySentences('path to tagged corpus') 
# model = gensim.models.Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
# model.save('path to directory')
model = gensim.models.Word2Vec.load('path to model')

def filter(w, k_sim, k, smin): 
	suffix = w[w.index("_"):]
        words=[]
	n=0
	for a in k_sim:
		found = False
		if a[0] in lookup_id and a[0].endswith(suffix) and n<int(k) and a[1]>=float(smin) and a[0] != w:
			for i in lookup_id[a[0]]:
				for s, p, o in wordsenses.triples((None, None, URIRef(i))):
					for s2, p2, o2 in wordsenses.triples((None, None, s)):
						if (s2, None, None) in hyponymy:
							found = True

			if found == True:
			  words.append(a[0])
				n+=1
	return words

# Computing scores for the hypernyms of the k similar words,
# and discovering the appropriate hypernym for the target word. 

def score(ntrg, k_similar, d):
	count=0
	score = 0
	hyper_score = {}
	suffix = ntrg[ntrg.index("_"):]
	for k in k_similar:
    hypo = lookup_ID(k)
    for ids in hypo:
      for s, p, o in wordsenses.triples((None, URIRef(word), URIRef(ids))):  
			  if ("_subst" in suffix and (s, None, URIRef(nounURI)) in wordsenses) or ("_verb" in suffix and (s, None, URIRef(verbURI)) 
        in wordsenses) or ("_adj" in suffix and (s, None, URIRef(adjURI)) in wordsenses):
          for s2, p2, o2 in wordsenses.triples((None, URIRef(wordsense), s)): 
            wordset = set()
            count = -1
            score = 0
						times = 0
						seen_hyp = set()
						hyp_rel = {}
						level = 0
						hypernym_level = {}
            for i in synsets.transitive_objects(s2, hyp):
              count += 1
							seen_hyp.add(i)
							if i not in hypernym_level and count == 0:
							  hypernym_level[i] = 0	
              for s3, p3, o3 in wordsenses.triples((i, URIRef(wordsense), None)):  
                for s4, p4, o4 in wordsenses.triples((o3, URIRef(word), None)):  
                  wordset.add(o4)
                  if count == 0 or ((i, None, None)) not in wordsenses or lookup_ID(ntrg) in wordset:
								    wordset = set()
                    continue 						
							level += 1
							if i not in hypernym_level:  
								hypernym_level[i] = level
							level = hypernym_level[i]
							for s in seen_hyp:
								if (s, None, i) in hyponymy: 
									if s not in hyp_rel:
										hyp_rel[s] = 0
									hyp_rel[s] += 1
									if hyp_rel[s] > 1:
										hypernym_level[i] = hypernym_level[s] + 1
										level = hypernym_level[s] + 1
              if i not in hyper_score:
                hyper_score[i] = 0
              score = float(d)**(level-1)*model.similarity(ntrg, k)
              hyper_score[i]+=score          

	if len(hyper_score)>0:
		best = max(hyper_score, key=hyper_score.get)
		hyper_scores.write(ntrg + "\t" + str(best) + "\t" + str(hyper_score[best]) + "\n")

k = <value for k>
s = <value for s>
d = <value for d>
path = ""
title = ""
hyper_scores=open(title, "w") #+ str(k) +"_"+ str(s) +"_"+ str(d), "w")
with open(path) as file
  for l in file:
    k_sim = model.most_similar(positive=[l.strip("\n")], negative=[], topn=1000)
	  score(l.strip("\n"),filter(l.strip("\n"), k_sim, k, s), d)
