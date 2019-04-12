import copy, math
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

  def evaluate(self,termset,freq):
    nd = 0                                #total number of documents
    ns = 0                                #total number of sentences across all documents
    nt = 0                                #total number of distinct terms across all documents
    Td = []
    reveal = False

    if termset == None:
      termset = copy.copy(next(iter(self.documents)).data['terms'])
      reveal = True

    Tf = [0 for y in range(len(termset))]
    terms = []

    for (i,term) in enumerate(termset):
      for document in self.documents:
        Tf[i] += document.data['terms'].get(term,0)

    consider = True
    for (i,term) in enumerate(termset):
      if Tf[i] < freq:
        continue

      if reveal:
        print term,Tf[i]

      terms.append(term)

      if consider:
        consider = False
        for document in self.documents:
          nd += 1
          ns += document.data['ns']
          nt += len(document.data['terms'])

          if document.data['terms'].get(term,0):
            Td.append(document)

      else:
        for j in reversed(range(len(Td))):
          document = Td[j]

          if not document.data['terms'].get(term,0):
            del(Td[j])

    Ns = 0                                #number of sentences containing all terms being evaluated (t1 ... tK)
    Nd = len(Td)                          #number of documents containing all terms being evaluated (t1 ... tK)

    if not Nd:
      return None

    for document in Td:
      for sentence in document.sentences:
        try:
          for term in terms:
            if term not in sentence:
              raise Exception
          Ns += 1
        except Exception:
          pass

    DF = Nd/float(nd)                     #document frequency for (t1 ... tK)
    SF = Ns/float(ns)                     #sentence frequency for (t1 ... tK)
    MK = SF                               #start calculating Measure for association for (t1 ... tK)

    data = {}
    for term in terms:
      try:
        self.matrix[term]
      except KeyError:
        self.tf_idf(term)

      data[term] = self.matrix[term]

      MK *= data[term]['IDF']

    return { 'DF': DF, 'MK': MK, 'SF': SF, 'TF-IDF': data }

  def tf_idf(self,term):
    tf = []
    tf_idf = []
    Nd = len(self.documents)
    nd = 0
    for (i,document) in enumerate(self.documents):
      dtf = document.data['terms'].get(term,0)
      if dtf:
        nd += 1                           #number of documents containing term T
      tf.append(dtf)

    try: 
      idf = math.log(Nd/float(nd),10)     #IDF for term T
    except ZeroDivisionError:
      idf = math.log(Nd,10)

    for i in range(0,Nd):
      tf_idf.append(idf * tf[i])

    self.matrix[term] = {
      'DF': nd,
      'TF': tf,
      'IDF': idf,
      'TF-IDF': tf_idf
    }
