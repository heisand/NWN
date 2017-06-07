#coding=utf-8

# Under revision

import sys
import re

synsets = sys.argv[1]
wordsenses = sys.argv[2]
words = sys.argv[3]

s = open(synsets, "r")
s2 = open(wordsenses, "r")
s3 = open(words, "r")
f = s.read()
f2 = s2.read()
f3 = s3.read()

Synset = re.findall(r'<wn20schema:Synset rdf[^<]+<[^<]+</[^<]+</wn20schema:NounSynset>', f)
VerbSynset = re.findall(r'<wn20schema:VerbSynset rdf[^<]+<[^<]+</[^<]+</wn20schema:NounSynset>', f)
AdjectiveSynset = re.findall(r'<wn20schema:AdjectiveSynset rdf[^<]+<[^<]+</[^<]+</wn20schema:NounSynset>', f)
NoneSynset = re.findall(r'<wn20schema:NoneSynset rdf[^<]+<[^<]+</[^<]+</wn20schema:NounSynset>', f)   

def replace(g, h:
	for i in g:
    		f = f.replace(i, i.replace("NounSynset", h))


replace(Synset, "Synset")
replace(VerbSynset, "VerbSynset")
replace(AdjectiveSynset, "AdjectiveSynset")
replace(NoneSynset, "NoneSynset")

f = f.replace("eMbalenhle", "Embalenhle")

f = re.sub(r' & ', " &amp; ", f)
f2 = re.sub(r' & ', " &amp; ", f2)
f3 = re.sub(r'>,<', '><', f3)
f3 = re.sub(r' & ', " &amp; ", f3)

s.close()
s2.close()
s3.close()

s = open("synsets.rdf", "w")
s2 = open("words.rdf", "w")
s3 = open("wordsenses.rdf", "w")

s.write(f)
s2.write(f2)
s3.write(f3)

s.close()
s2.close()
s3.close()
