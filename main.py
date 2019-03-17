import os
import re
import signal
import sys
from os.path import join, isdir, isfile
from library import corpus, document, stopwords

def signal_handler(sig, frame):
  raise SystemExit

signal.signal(signal.SIGINT, signal_handler)

try:
  path = sys.argv[1]
except IndexError:
  path = None

files = []
while True:
  if path:
    if (path[:1] != '/'):
      path = os.getcwd() + '/' + path
    
    if isdir(path):
      for filename in os.listdir(path):
        filepath = join(path,filename)
        if re.search(r'(?i).te?xt$',filename) and isfile(filepath):
          files.append(filepath)

      if len(files):
        break
      else:
        print "No text(.txt) files in directory [%s]; Press <enter> to continue"%path,raw_input()
        path = None
    else:
      path = raw_input("Please provide a valid path for Corpus (user CTRL+C to terminate): ")
  else:
    path = raw_input("Please provide a path for Corpus (user CTRL+C to terminate): ")

words = stopwords("a about above after again against ain all am an and any are aren aren't as at be because been before being below between both but by can couldn couldn't d did didn didn't do does doesn doesn't doing don don't down during each few for from further had hadn hadn't has hasn hasn't have haven haven't having he her here hers herself him himself his how i if in into is isn isn't it it's its itself just ll m ma me mightn mightn't more most mustn mustn't my myself needn needn't no nor not now o of off on once only or other our ours ourselves out over own re s same shan shan't she she's should should've shouldn shouldn't so some such t than that that'll the their theirs them themselves then there these they this those through to too under until up ve very was wasn wasn't we were weren weren't what when where which while who whom why will with won won't wouldn wouldn't y you you'd you'll you're you've your yours yourself yourselves could he'd he'll he's here's how's i'd i'll i'm i've let's ought she'd she'll that's there's they'd they'll they're they've we'd we'll we're we've what's when's where's who's why's would")

mine = corpus(files)
mine.build(words.words)

print 'Processed %d documents; enter <space/comma-separated> list of words to evaluate (user CTRL+C to terminate):\n'%len(mine.documents)

while True:
  data = set()
  terms = re.split('[; ]',raw_input().strip().lower())

  for term in terms:
    if (len(term) > 1) and (term not in words.words):
      data.add(term)

  if len(data):
    result = mine.evaluate(data)
    print result
