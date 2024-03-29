from flask import Flask
import pickle

app = Flask(__name__)


import pandas as pd
import numpy as np

import gensim
model = gensim.models.KeyedVectors.load_word2vec_format(r"C:\Users\Harshit\Downloads\GoogleNews-vectors-negative300.bin.gz", 
                                                        binary=True)

words = model.index2word

w_rank = {}
for i,word in enumerate(words):
    w_rank[word] = i

WORDS = w_rank



import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

def P(word): 
    "Probability of `word`."
    # use inverse of rank as proxy
    # returns 0 if the word isn't in the dictionary
    return - WORDS.get(word, 0)

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)
  

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# In[22]:


#import pickle
pickle.dump(correction, open('model.pkl','wb'))


# In[23]:


#model = pickle.load(open('model.pkl','rb'))


# In[26]:


#def hello(word):
#    model = pickle.load(open('model.pkl','rb'))
 #   return model(word)
#hello("quikly")   



@app.route('/')
def hello():

	model = pickle.load(open('model.pkl','rb'))
	return model(word)



if __name__ == '__main__':

    app.run(port=5000)


