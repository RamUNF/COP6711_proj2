class stopwords:
  words = set()

  def __init__(self,stop_words):
    if (type(stop_words) not in [list,tuple]):
      stop_words = stop_words.split(' ')

    for (i,k) in enumerate(stop_words):
      self.words.add(k.lower())
