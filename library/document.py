import re

class document:
  filepath = None
  stop_characters = '!;.?'
  data = None
  sentences = None

  def _strip_html(func):
    def _stripper(*args,**kwargs):
      return func(
        args[0],
        re.sub(r'<[^>\r\n]+>','',args[1]),
        args[2]
      )

    return _stripper

  def __init__(self,filepath,words):
    self.filepath = filepath
    with open(filepath,'r') as filehandler:
      self.evaluateSentences(self.prepareSentences(filehandler.read(),words))

  @_strip_html
  def prepareSentences(self,data,words):
    re_s = re.compile('[%s]\W+'%self.stop_characters)
    re_w = re.compile('[,\s:]')
    re_c = re.compile('[^\d\w\']')

    sentences = []

    for sentence in re_s.split(data.rstrip(self.stop_characters).lower()):
      s = []
      for word in re_w.split(sentence):
        word = re_c.sub('',word)
        if (len(word) > 1) and (word not in words):
          s.append(word)

      if len(s):
        sentences.append(s)

    return sentences

  def evaluateSentences(self,sentences):
    ns = 0
    nt = 0
    terms = {}

    self.sentences = sentences

    for sentence in sentences:
      ns += 1
      for term in sentence:
        nt += 1
        terms[term] = terms.get(term,0) + 1

    self.data = {
      'ns': ns,
      'nt': nt,
      'terms': terms
    }
