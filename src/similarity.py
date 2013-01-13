'''
Created on Jan 13, 2013

@author: shelajev
'''

import operator, re
#number of jokes we have
N = 1972
from freqs import analyze, get_common_words

def get_words(text):
  words = re.split('\W+', text, flags=re.IGNORECASE)
  # we want non-empty and only alphabetic words
  words = map(lambda w: w.lower(), words)
  return filter(lambda w: w is not None and re.match('^[a-z]+$', w) is not None, words)

def get_idxs_similar_to(number, topN = 5):
  analyze()
  common = get_common_words()
  with open('../etc/jokes/%04d.txt' % number) as f:
    text = f.read()
    ratings = compute_similarity_ratings(text, common)
    similar = sorted(ratings.iteritems(), key=operator.itemgetter(1))[-topN:]
    similar.reverse()
    return similar

def compute_similarity_ratings(text, common):
  ratings = {}
  original_words = get_words(text)
  for i in range(N):
    with open('../etc/jokes/%04d.txt' % i) as f:
      joke = f.read()
      joke_words = get_words(joke)
      ratings[i] = get_text_similarity(original_words, joke_words, common)
  return ratings

def get_text_similarity(words, other_words, common):
  rating = 0.0
  for word in other_words:
    if word in words:
      rating = rating + 1.0 / common[word]
  return rating

def check_joke(n):
  top = get_idxs_similar_to(n)
  print 'Checking joke %s, top similar jokes: \n%s' % (n, top[1:])
  print '============================'
  with open('../etc/jokes/%04d.txt' % n) as f:
    print f.read()
  print '============================'
  for i, r in top:
    if i == n: 
      continue
    print "Joke %s has similarity rating %s:" % (i, r)
    with open('../etc/jokes/%04d.txt' % i) as f:
      print f.read()
    print '============================'

if __name__ == '__main__':
  check_joke(9)
    