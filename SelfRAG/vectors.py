from openai import OpenAI

def getVector(text):
    client = OpenAI()
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model="text-embedding-ada-002").data[0].embedding
   
def cosineSimilarity(vec1, vec2):
    return sum([vec1[i] * vec2[i] for i in range(len(vec1))])

def getNearestNeighbors(vec, vecs, numNeighbors):
    neighbors = []
    for i in range(len(vecs)):
        neighbors.append((cosineSimilarity(vec, vecs[i]), i))
    neighbors.sort(reverse=True)
    return neighbors[:numNeighbors]
    