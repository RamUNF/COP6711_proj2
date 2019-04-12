import numpy as np
import os
import re
import signal
import sys
from os.path import basename, join, isdir, isfile
from library import corpus, document, stopwords
from library.cluster import agglomerative_cluster, K_means, print_hierarchical

def signal_handler(sig, frame):
  raise SystemExit

signal.signal(signal.SIGINT, signal_handler)

try:
  printdata = not(re.match('([Yy](es)?)|([Tt](rue)?)',sys.argv[1]) == None)
except IndexError:
  printdata = False

try:
  path = sys.argv[1]
except IndexError:
  path = None

k_value = 2
freq = 15

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
size = len(mine.documents)

print 'Processed %d documents; enter K#: <space/comma-separated> list of words to evaluate (user CTRL+C to terminate):\n'%len(mine.documents)

while True:
  data = set()
  terms = re.split('[,; ]',raw_input().strip().lower())
  fetch_common = False

  for i,term in enumerate(terms):
    if not(i):
      if re.match('^[fk][1-9][0-9]*:',term):
        pos = term.find(':')
        if term[:1] == 'f':
          freq = int(re.sub('[^0-9]','',term[:pos]))
          print "Frequency set to %d" % freq
        else:
          k_value = int(re.sub('[^0-9]','',term[:pos]))
          print "K-value set to %d" % k_value

        term = term[(pos + 1):]

      if (term == '*'):
        fetch_common = True
        break;

    if (len(term) > 1) and (term not in words.words):
      data.add(term)

  if len(data) or fetch_common:
    result = mine.evaluate(None if fetch_common else data,freq)
    if result:
      vectors = {
        'TF': [[] for y in range(size)],
        'TF-IDF': [[] for y in range(size)]
      }

      for vector in result['TF-IDF'].values():
        for (i,j) in enumerate(vector['TF']):
          vectors['TF'][i].append(j)
          vectors['TF-IDF'][i].append(vector['TF-IDF'][i])

          tf = map(lambda (i,j): j['TF'],enumerate(result['TF-IDF'].values()))
          tf_idf = map(lambda (i,j): j['TF-IDF'],enumerate(result['TF-IDF'].values()))

      if printdata:
        print "<==================================================>"
        print 'MK: %.6f, SF %.6f'%(result['MK'],result['SF'])

        print "TF     :\n",np.matrix(tf),"\n--"
        print "IDF-TF :\n",np.matrix(tf_idf),"\n--"
        print "IDF-TF :\n",np.matrix(tf_idf),"\n--"
        print "VECTORS:\n",np.matrix(vectors['TF']),"\n",np.matrix(vectors['TF-IDF']),"\n--"

      print "<==================================================>"
      clusters = K_means(k_value, vectors['TF'])
      for i, cluster in enumerate(clusters):
          print("Cluster[TF] " + str(i))
          for c in cluster:
              print "Doc%-2d: %s"%(c,basename(corpus.documents[c].filepath))

      print "<==================================================>"
      clusters = K_means(k_value, vectors['TF-IDF'])
      for i, cluster in enumerate(clusters):
          print("Cluster[TF-IDF] " + str(i))
          for c in cluster:
              print "Doc%-2d: %s"%(c,basename(corpus.documents[c].filepath))

      clusters = agglomerative_cluster(vectors['TF'])
      print "<==================================================>"
      print_hierarchical(clusters)
    else:
      print "<==================================================>"
      print "No can do amigo"
