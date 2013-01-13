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
dicts = [defaultdict(lambda: 0), defaultdict(lambda: 0), defaultdict(lambda: 0)]

def parse(joke_file, book_id):
  global common, dicts
  with open(joke_file) as f:
    text = f.read()
    words = re.split('\W+', text, flags=re.IGNORECASE)
    for word in words:
      word = word.lower()
      if not word or re.match('^[a-z]+$', word) is None:
        continue
      common[word] += 1
      dicts[book_id][word] += 1

def main():
  for i in [0, 1, 2]:
    bounds = book_boundaries[i]
    for n in range(bounds[0], bounds[1]):
      parse('../etc/jokes/%04d.txt' % n, i)
      
def dump_dict_top(dictionary, filename, number_of_entries=100):
  tuples = sorted(dictionary.iteritems(), key=operator.itemgetter(1))[-number_of_entries:]
  tuples.reverse()
  with open(filename, 'w') as f:
    for k, v in tuples:
      f.write('%s:%s\n' % (k, v))
  
if __name__ == '__main__':
  main()
  dump_dict_top(common, '../etc/common.dict', 25)
  dump_dict_top(dicts[0], '../etc/book1.dict', 25)
  dump_dict_top(dicts[1], '../etc/book2.dict', 25)
  dump_dict_top(dicts[2], '../etc/book3.dict', 25)
  