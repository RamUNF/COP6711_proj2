import math
from .document import document

class corpus:
  documents = []
  files = None
  matrix = {}

  def __init__(self,files):
    self.files = files
  
  def build(self,words):
    for p in self.files:
      self.documents.append(document(p,words))

  def evaluate(self,terms):
    Nd = 0                                #total number of documents
    Ns = 0                                #total number of sentences across all documents
    Nt = 0                                #total number of distinct terms across all documents
    Td = []

    for (i,term) in enumerate(terms):
      if i:
        for j in reversed(range(len(Td))):
          document = Td[j]
          if not document.data['terms'].get(term,0):
            del(Td[j])

      else:
        for document in self.documents:
          Nd += 1
          Ns += document.data['ns']
          Nt += len(document.data['terms'])

          if document.data['terms'].get(term,0):
            Td.append(document)

    ns = 0                                #number of sentences containing all terms being evaluated (t1 ... tK)
    nd = len(Td)                          #number of documents containing all terms being evaluated (t1 ... tK)

    for document in Td:
      for sentence in document.sentences:
        try:
          for term in terms:
            if term not in sentence:
              raise Exception
          ns += 1
        except Exception:
          pass

    DF = nd/float(Nd)                     #document frequency for (t1 ... tK)
    SF = ns/float(Ns)                     #sentence frequency for (t1 ... tK)
    MK = SF                               #start calculating Measure for association for (t1 ... tK)

    data = {}
    for term in terms:
      try:
        self.matrix[term]
      except KeyError:
        self.tf_idf(term)

      data[term] = self.matrix[term]

      MK *= data[term]['IDF']

    return { 'DF': DF, 'SF': SF, 'MK': MK, 'TF-IDF': data }

  def tf_idf(self,term):
    Nd = len(self.documents)
    nd = 0
    tf = 0
    for document in self.documents:
      dtf = document.data['terms'].get(term,0)
      if dtf:
        nd += 1                           #number of documents containing term T
        tf += dtf                         #number of occurrences for T across all documents

    try: 
      idf = math.log(Nd/float(nd),10)     #IDF for term T
    except ZeroDivisionError:
      idf = math.log(Nd)
    ctf = tf/float(document.data['nt'])   #TF for term T

    self.matrix[term] = {
      #'nd': nd,
      'DF': nd/float(Nd),
      #'dtf': tf,
      'IDF': idf,
      'TF': ctf,
      'TF-IDF': idf * ctf 
    }
