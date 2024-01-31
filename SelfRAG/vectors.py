from settings import EMBEDDINGS_MODEL

def cosine_similarity(vec1, vec2):
    return sum([vec1[i] * vec2[i] for i in range(len(vec1))])

def get_nearest_neighbors(vec, vecs, numNeighbors):
    neighbors = []
    for i in range(len(vecs)):
        neighbors.append((cosine_similarity(vec, vecs[i]), i))
    neighbors.sort(reverse=True)
    return neighbors[:numNeighbors]
    