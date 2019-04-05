import numpy as np
import random

#Input: Two document vectors x and y
#Output: The cosine similarity of the two vectors
def cos_sim(x, y):
    assert len(x) == len(y)
    x_norm = np.linalg.norm(x)
    y_norm = np.linalg.norm(y)
    dot = np.dot(x,y)
    return dot / (x_norm * y_norm)

#Input: K, number of clusters to discover
#       documents, corpus of documents to cluster in the form of a
#       list of document vectors
#Output: A list of clusters, each cluster represented as a list of indices of the document vector in
#        documents
def K_means(K, documents):
    assert K > 0
    centroids = random.sample(documents, K)
    clusters = [[] for i in range(K)]
    changed = True
    while(changed):
        clusters = [[] for i in range(K)]
        changed = False
        for i in range(len(documents)):
            max_sim = -1
            nearest_c = -1
            for c in range(K):
                sim = cos_sim(documents[i], centroids[c])
                if sim > max_sim:
                    max_sim = sim
                    nearest_c = c
            clusters[nearest_c].append(i)

        for i in range(K):
            old_centroid = centroids[i]
            doc_vectors = []
            for d in clusters[i]:
                doc_vectors.append(documents[d])
            centroids[i] = np.mean(doc_vectors, axis=0)
            if (abs(old_centroid - centroids[i]) > 0.01).any():
                changed = True

    return clusters



if __name__ == "__main__":
    doc1 = [5, 0, 3, 0, 2, 0, 0, 2, 0, 0]
    doc2 = [3, 0, 2, 0, 1, 1, 0, 1, 0, 1]
    doc3 = [0, 7, 0, 2, 1, 0, 0, 3, 0, 0]
    doc4 = [0, 1, 0, 0, 1, 2, 2, 0, 3, 0]
    corpus = [doc1, doc2, doc3, doc4]
    clusters = K_means(2, corpus)
    for i, cluster in enumerate(clusters):
        print("Cluster " + str(i))
        for c in cluster:
            print(corpus[c])
