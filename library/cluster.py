import numpy as np
import random

#Input: Two document vectors x and y
#Output: The cosine similarity of the two vectors
def cos_sim(x, y):
    assert len(x) == len(y),"Length of vectors differs"
    x_norm = np.linalg.norm(x)
    y_norm = np.linalg.norm(y)
    dot = np.dot(x,y)

    if dot == 0:
        return 0
    return dot / (x_norm * y_norm)

#Input: K, number of clusters to discover
#       documents, corpus of documents to cluster in the form of a
#       list of document vectors
#Output: A list of clusters, each cluster represented as a list of indices of the document vector in
#        documents
def K_means(K, documents):
    assert K > 0

    K = min(K,len(documents))

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
            if len(doc_vectors) > 0:
                centroids[i] = np.mean(doc_vectors, axis=0)
            else:
                centroids[i] = np.zeros(len(old_centroid))
            if (abs(old_centroid - centroids[i]) > 0.01).any():
                changed = True

    return clusters

#Cluster class for use with agglomerative_cluster() hierarchical clustering method
#Contains information on the clusters two children (which may be document vectors or other clusters)
#also contains information on the cluster's centroid (mean of all leaf document vectors)
class Cluster:
    def __init__(self, child1, child2, centroid):
        self.child1 = child1
        self.child2 = child2
        self.centroid = centroid

#Input: documents, corpus of documents to cluster in the form of a list of document vectors
#Output: A Cluster object which is the root of the hierarchical clustering. The clustering can be
#        obtained by traversing the tree structure.
#This method uses the average of the vectors in the cluster to compute similarity between clusters (as opposed to single or complete link or other techniques)
def agglomerative_cluster(documents):
    
    documents = list(documents)
    clusters = []    
    while(len(documents) > 1):
        d1 = documents[0]
        documents.pop(0)
        closest_id = -1
        closest_sim = -1
        for i, d in enumerate(documents):
            sim = cos_sim(d1, d)
            if sim > closest_sim:
                closest_sim = sim
                closest_id = i
                
        d2 = documents[i]
        documents.pop(i)
        centroid = np.mean([d1, d2], axis=0)
            
        clusters.append(Cluster(d1, d2, centroid))

    if len(documents) == 1:
        clusters.append(Cluster(documents[0], None, documents[0]))
        
    while(len(clusters) > 1):        
        current_clusters = clusters
        clusters = []

        while(len(current_clusters) > 1):
            c1 = current_clusters[0]
            current_clusters.pop(0)
            closest_id = -1
            closest_sim = -1
            for i, c in enumerate(current_clusters):
                sim = cos_sim(c1.centroid, c.centroid)
                if sim > closest_sim:
                    closest_sim = sim
                    closest_id = i
                    
            c2 = current_clusters[i]
            current_clusters.pop(i)
            centroid = np.mean([c1.centroid, c2.centroid], axis=0)
            clusters.append(Cluster(c1, c2, centroid))

        if(len(current_clusters) == 1):
            clusters.append(Cluster(current_clusters[0], None, current_clusters[0].centroid))

    return clusters[0]

#Input: A Cluster object
#Output: None
#Side-effects: Prints the hierarchical clustering to console.
def print_hierarchical(cluster, documents, level=0):
    if isinstance(cluster, Cluster):
        print('-' * level + "Level " + str(level))
        print_hierarchical(cluster.child1, documents, level+1)
        print_hierarchical(cluster.child2, documents, level+1)
    else:
        if(cluster is not None):
            for i, d in enumerate(documents):
                if d == cluster:
                    documents[i] = None
                    print('-' * level + "Doc" + str(i))
                
        
    

if __name__ == "__main__":
    doc1 = [5, 0, 3, 0, 2, 0, 0, 2, 0, 0]
    doc2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    doc3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    corpus = [doc1, doc2, doc3]

    print("K-means")
    clusters = K_means(2, corpus)
    for i, cluster in enumerate(clusters):
        print("Cluster " + str(i))
        for c in cluster:
            print(corpus[c])
    
    print("\n\nAgglomerative Hierarchical")
    clusters = agglomerative_cluster(corpus)
    print_hierarchical(clusters)

