'''
Created on Jan 13, 2013

@author: shelajev
'''
import re
start_line = ['PREFACE', 'INTRODUCTION', 'BUDGET OF FUN', 'TOASTER\'S HANDBOOK', 'JOKES FOR ALL OCCASIONS'] 
end_line = ['INDEX', 'End of the Project Gutenberg']

def parse_jokes_book_file(filename, pattern_string):
  with open(filename) as f:
    content = f.readlines()
    a, b = -1, -1
    i = 0
    while i < len(content):
      line = content[i]
      def my_starts_with(x):
        return line.startswith(x)
      if any(map(my_starts_with, start_line)):
        a = i
      if any(map(my_starts_with, end_line)):
        b = i
        break
      i += 1
    body = ''.join(content[a+1:b])
  
  global counter
  for joke in re.findall(pattern_string, body, re.MULTILINE | re.DOTALL):
    joke_file = '../etc/jokes/%04d.txt' % counter
    with open(joke_file, 'w') as f:
      f.write(joke)
    counter = counter + 1

if __name__ == '__main__':
  patterns = {1: r'^[A-Z][A-Z ]*\n\n.*?\n\n\n\n', 
              2: r'[ *]*\n\n.*?\n\n              ',
              3: r'^[A-Z][A-Z \.]*\n\n.*?\n\n\n'
             }
  global counter
  counter = 0
  old_counter = 0
  for i in range(1, 4):
    parse_jokes_book_file('../etc/%s.txt' % i, patterns[i])
    print 'done with book %s, there were %s jokes' % (i, counter - old_counter)
    print 'bounds = (%s, %s)' % (old_counter, counter)
    old_counter = counter
    