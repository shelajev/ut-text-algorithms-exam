'''
Created on Jan 13, 2013

@author: shelajev
'''
import operator
import re
from collections import defaultdict

book_boundaries = [(0, 684), (684, 1352), (1352, 1972)]

#global dict
common = defaultdict(lambda: 0)
# lists for each book
dicts = [defaultdict(lambda: 0), defaultdict(lambda: 0), defaultdict(lambda: 0), defaultdict(lambda: 0)]

def parse(joke_file, book_id, add_to_common=True):
  global common, dicts
  with open(joke_file) as f:
    text = f.read()
    words = re.split('\W+', text, flags=re.IGNORECASE)
    for word in words:
      word = word.lower()
      if not word or re.match('^[a-z]+$', word) is None:
        continue
      if add_to_common:
        common[word] += 1
      dicts[book_id][word] += 1

def analyze():
  for i in [0, 1, 2]:
    bounds = book_boundaries[i]
    for n in range(bounds[0], bounds[1]):
      parse('../etc/jokes/%04d.txt' % n, i)
      
def get_common_words():
  return common
      
def dump_dict_top(dictionary, filename, number_of_entries=100):
  tuples = sorted(dictionary.iteritems(), key=operator.itemgetter(1))[-number_of_entries:]
  tuples.reverse()
  with open(filename, 'w') as f:
    for k, v in tuples:
      f.write('%s:%s\n' % (k, v))
      
def get_words_specific_to_jokes(jokes_dict, general_dict):
  limit_jokes_words = 100
  limit_general_words = 150
  joke_words = sorted(jokes_dict.iteritems(), key=operator.itemgetter(1))[-limit_jokes_words:]
  joke_words = set([pair[0] for pair in joke_words])
  general_words = sorted(general_dict.iteritems(), key=operator.itemgetter(1))[-limit_general_words:]
  general_words = set([pair[0] for pair in general_words])
  return joke_words - general_words
  
if __name__ == '__main__':
  analyze()
  dump_dict_top(common, '../etc/common.dict', 25)
  dump_dict_top(dicts[0], '../etc/book1.dict', 25)
  dump_dict_top(dicts[1], '../etc/book2.dict', 25)
  dump_dict_top(dicts[2], '../etc/book3.dict', 25)
  parse('../etc/alice.txt', 3, add_to_common=False)
  dump_dict_top(dicts[3], '../etc/alice.dict', 25)
  
  joke_specific_words = get_words_specific_to_jokes(common, dicts[3])
  for word in joke_specific_words:
    print word
  