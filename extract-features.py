#!/usr/bin/env python

"""
Steps:

1. Parse sentences
2. Chunk sentences into NPs
3. Identify features for each NP

CURRENT ISSUES:

news
- "a better EU policymaking system" seen as two NPs


techdoc
- "at the 400 / 100 mg twice daily dose" 
- "Generally , for SSRIs and SNRIs , these events are mild to moderate and self-limiting , however , in some patients they may be severe and / or prolonged ." is / tagged as NN?

paraweb
- "as his attorney who will provide the claimant with legal assistance either free of charge or for a reduced fee ." for a reduced fee NP identified as only "fee"

"""

#import re
import sys
import nltk

class Sentence(object):
    def __init__(self):
        self.label = None
        self.text = ""
        self.words = []
        self.nps = []
        self.tree = None
        
    #def get_word(index):
    #    return self.words[index]
        
class Word(object):
    def __init__(self):
        self.word = None
        self.lemma = None
        self.pos = None
        self.index = None
        self.head = None
        self.role = None
        self.sen = None
        self.preceded_by = None
        self.followed_by = None
    
    def __str__(self):
        return self.word
        
class NounPhrase(object):
    def __init__(self):
        self.words = []
        self.head = None
        self.pos_head = None
        self.core = "_"
        self.pos_core = "_"
        self.mod = "_"
        self.pos_mod = "_"
        self.string = "_"
        self.pos_string = "_"
        self.unigram_pre = "_"
        self.pos_unigram_pre = "_"
        self.unigram_post = "_"
        self.pos_unigram_post = "_"
        self.bigram_pre = "_"
        self.pos_bigram_pre = "_"
        self.bigram_post = "_"
        self.pos_bigram_post = "_"
        self.trigram_pre = "_"
        self.pos_trigram_pre = "_"
        self.trigram_post = "_"
        self.pos_trigram_post = "_"
        self.has_det = False
        self.sen = None

def get_sentences(c):
    raw = open(c).read().decode("utf8").split("\n\n")
    
    sentences = []
    
    for sentence in raw:
        sen = Sentence()
        sentence = sentence.split("\n")
        sen.label = sentence[0]
        for i in range(1, len(sentence)):
            w = Word()
            word = sentence[i].split("\t")
            w.word = word[0].encode('utf8')
            sen.text = sen.text + w.word + " "
            w.lemma = word[1].encode('utf8')
            w.pos = word[2].encode('utf8')
            w.index = int(word[3]) - 1
            w.head = int(word[4]) - 1
            w.role = word[5]
            w.sen = sen
            sen.words.append(w)
            if i > 1:
                w.preceded_by = w.sen.words[i - 2]
                w.preceded_by.followed_by = w

        if len(sen.words) > 0:
            sentences.append(sen)
               
    return sentences

def chunk(s):

    pattern = """
                  NP: {<DT|PRP\$|POS|CD>?(<RB>?<JJ.*>(<,>?<CC>?<RB>?<JJ.*>)*|<\`\`|\'\'>?)*<NN.*>+}
              """
    NPChunker = nltk.RegexpParser(pattern) 
    
    sen = []
    for w in s.words:
        sen.append((w, w.pos))
    s.tree = NPChunker.parse(sen)
    return s.tree

def get_np(np, s):
    
    new_np = NounPhrase()
    new_np.sen = s
    for i in range(len(np)):
        w = np[i][0]
        pos = np[i][1]
        
        if i == 0 and pos == "DT":
            new_np.has_det = True
        else:
            new_np.words.append(w)
            
            new_np.string += w.lemma + "_"
            new_np.pos_string += w.pos + "_"
            
            if not pos.startswith("NN"):
                new_np.mod += w.lemma + "_"
                new_np.pos_mod += w.pos + "_"
                
            else:
                new_np.core += w.lemma + "_"
                new_np.pos_core += w.pos + "_"
        
        ## PRECEDING N-GRAMS
        if i == 0:
            if w.preceded_by:
                new_np.unigram_pre += w.preceded_by.word + "_"
                new_np.pos_unigram_pre += w.preceded_by.pos + "_"
                
                if w.preceded_by.preceded_by:
                    new_np.bigram_pre = "_" + w.preceded_by.preceded_by.word + new_np.unigram_pre
                    new_np.pos_bigram_pre = "_" + w.preceded_by.preceded_by.pos + new_np.pos_unigram_pre                    
                    
                    if w.preceded_by.preceded_by.preceded_by:
                        new_np.trigram_pre = "_" + w.preceded_by.preceded_by.preceded_by.word + new_np.bigram_pre
                        new_np.pos_trigram_pre = "_" + w.preceded_by.preceded_by.preceded_by.pos + new_np.pos_bigram_pre                        
                        
                    else:
                        new_np.trigram_pre = "_BOS" + new_np.bigram_pre
                        new_np.pos_trigram_pre = "_BOS" + new_np.pos_bigram_pre
                        
                else:
                    new_np.bigram_pre = "_BOS" + new_np.unigram_pre
                    new_np.trigram_pre = "_BOS_BOS" + new_np.unigram_pre
                    
                    new_np.pos_bigram_pre = "_BOS" + new_np.pos_unigram_pre
                    new_np.pos_trigram_pre = "_BOS_BOS" + new_np.pos_unigram_pre
                    
            else:
                new_np.unigram_pre = "_BOS_"
                new_np.bigram_pre = "_BOS_BOS"
                new_np.trigram_pre = "_BOS_BOS_BOS"

                new_np.pos_unigram_pre = "_BOS_"
                new_np.pos_bigram_pre = "_BOS_BOS"
                new_np.pos_trigram_pre = "_BOS_BOS_BOS" 

        # HEAD NOUN AND FOLLOWING N-GRAMS
        if i == (len(np) - 1):
            new_np.head = w.lemma
            new_np.pos_head = w.pos

            if w.followed_by:
                new_np.unigram_post += w.followed_by.word + "_"
                new_np.pos_unigram_post += w.followed_by.pos + "_"                
                
                if w.followed_by.followed_by:
                    new_np.bigram_post = new_np.unigram_post + w.followed_by.followed_by.word + "_"
                    new_np.pos_bigram_post = new_np.pos_unigram_post + w.followed_by.followed_by.pos + "_"
                    
                    if w.followed_by.followed_by.followed_by:
                        new_np.trigram_post = new_np.bigram_post + w.followed_by.followed_by.followed_by.word + "_"
                        new_np.pos_trigram_post = new_np.pos_bigram_post + w.followed_by.followed_by.followed_by.pos + "_"
                        
                    else:
                        new_np.trigram_post = new_np.bigram_post + "EOS_"
                        new_np.pos_trigram_post = new_np.pos_bigram_post + "EOS_"
                        
                else:
                    new_np.bigram_post = new_np.unigram_post + "EOS_"
                    new_np.trigram_post = new_np.unigram_post + "EOS_EOS_"
                    
                    new_np.pos_bigram_post = new_np.pos_unigram_post + "EOS_"
                    new_np.pos_trigram_post = new_np.pos_unigram_post + "EOS_EOS_"                    
                    
            else:
                new_np.unigram_post = "_EOS_"
                new_np.bigram_post = "_EOS_EOS"
                new_np.trigram_post = "_EOS_EOS_EOS"
           
                new_np.pos_unigram_post = "_EOS_"
                new_np.pos_bigram_post = "_EOS_EOS"
                new_np.pos_trigram_post = "_EOS_EOS_EOS"                
            
    return new_np


def main():
    if len(sys.argv) != 2:
        print "Usage: extract-features.py <src>"
        return 1
    
    src = sys.argv[1]
    sentences = get_sentences(src)
    nps = []
    
    for s in sentences:
        chunk(s)
        for np in s.tree.subtrees():
            if np.label() == "NP":
                nps.append(get_np(np, s))
    
### Printing ###

    print "sentence\thas_det\tstring\tpos_string\thead\tpos_head\tcore\tpos_core\tmod\tpos_mod\tunigram_pre\tpos_unigram_pre\tbigram_pre\tpos_bigram_pre\ttrigram_pre\tpos_trigram_pre\tunigram_post\tpos_unigram_post\tbigram_post\tpos_bigram_post\ttrigram_post\tpos_trigram_post"
    for np in nps:
        print np.sen.text + "\t" + str(np.has_det) + "\t" + np.string + "\t" + np.pos_string + "\t" + np.head + "\t" + np.pos_head + "\t" + np.core + "\t" + np.pos_core + "\t" + np.mod + "\t" + np.pos_mod + "\t" + np.unigram_pre + "\t" + np.pos_unigram_pre + "\t" + np.bigram_pre + "\t" + np.pos_bigram_pre + "\t" + np.trigram_pre + "\t" + np.pos_trigram_pre + "\t" + np.unigram_post + "\t" + np.pos_unigram_post + "\t" + np.bigram_post + "\t" + np.pos_bigram_post + "\t" + np.trigram_post + "\t" + np.pos_trigram_post
    
    
### TESTING ###
"""
    for np in nps:
        print np.sen.text
        if np.has_det:
            print "DETERMINER"
        for w in np.words:
            print w.word, w.lemma, w.pos
        print "HEAD: ", np.head, np.pos_head
        print "CORE: ", np.core, np.pos_core
        print "MOD: ", np.mod, np.pos_mod
        print "STRING: ", np.string, np.pos_string
        print "PRE UNI: ", np.unigram_pre, np.pos_unigram_pre
        print "PRE BI: ", np.bigram_pre, np.pos_bigram_pre
        print "PRE TRI: ", np.trigram_pre, np.pos_trigram_pre
        print "POST UNI: ", np.unigram_post, np.pos_unigram_post
        print "POST BI: ", np.bigram_post, np.pos_bigram_post
        print "POST TRI: ", np.trigram_post, np.pos_trigram_post
        print ""
"""        
        

"""
    for s in sentences:
        for np in s.tree.subtrees():
            if np.label() == "NP":
                for i in range(len(np)):
                    print np[i][0], np[i][0].lemma, np[i][1]
            print ""
            
"""


      
if __name__ == "__main__":
    main()
    
    



"""
def has_det(n):
    
    if n.sen.words[n.index - 2].pos == "DT":
        return True
    elif n.sen.words[n.index - 2].pos in mod and n.sen.words[n.index - 3].pos == "DT":
        return True
    #elif n.sen.words[n.index - 2].pos in mod and n.sen.words[n.index - 4].pos == "DT":
    #    return True
    

def build_nps(nouns, sentences):
    
    mod = ["JJ", "JJR", "JJS", "RB", "RBR", "RBS", "VBN", "DT", "CC", ",", "POS", "PRP$"]
    nps = []
    
    for s in sentences:
        for i in range(len(s.words), 0, -1):
            w = s.words[i - 1]
            if w.pos.startswith("NN") and w.in_np == False:
                np = NounPhrase()
                np.head = w
                np.core = w.word
                np.string = w.word
                np.pos_string = w.pos
                np.pos_core = w.pos
                w.in_np = True
                #np.trigram_post =
                for j in range(i - 2, 0, -1):
                    pre = s.words[j]
                    if pre.pos.startswith("NN") and np.core_found == False:
                        np.core = pre.word + "_" + np.core
                        np.pos_core = pre.pos + "_" + np.pos_core
                        np.string = pre.word + "_" + np.string
                        np.pos_string = pre.pos + "_" + np.pos_string
                        pre.in_np = True
                    elif pre.pos in mod:
                        np.mod = (pre.word + "_" + np.mod) if np.mod else pre.word
                        np.pos_mod = (pre.pos + "_" + np.pos_mod) if np.pos_mod else pre.pos                        
                        np.string = pre.word + "_" + np.string
                        np.pos_string = pre.pos + "_" + np.pos_string
                        pre.in_np = True
                        np.core_found = True
                        if pre.pos == "DT":
                            np.has_det = True
                            break
                    else:
                        break
                nps.append(np)
    
    return nps    
    
"""    