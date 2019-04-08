import numpy as np

#Input: index, Index of word in the document vector to find rate it is associated with other words
#        documents, list of document vectors
#Output: Returns a numpy array containing the rate the word is associated with other words in documents.
def word_association(index, documents):
    assert len(documents) > 0
    association_vector = [0] * len(documents[0])

    for d in documents:
        if d[index] > 0:
            for i, value in enumerate(d):
                if value > 0:
                    association_vector[i] += 1

    return np.array(association_vector) / association_vector[index]


if __name__ == "__main__":
    #usage example
    doc1 = [5, 0, 3, 0, 2, 0, 0, 2, 0, 0]
    doc2 = [3, 0, 2, 0, 1, 1, 0, 1, 0, 1]
    doc3 = [0, 7, 0, 2, 1, 0, 0, 3, 0, 0]
    doc4 = [0, 1, 0, 0, 1, 2, 2, 0, 3, 0]
    doc5 = [1, 0, 0, 0, 1, 2, 2, 0, 3, 0]
    corpus = [doc1, doc2, doc3, doc4, doc5]

    print(word_association(0, corpus))
            
