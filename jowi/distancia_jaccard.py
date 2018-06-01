def jaccard_distance(string1, string2,k=2):
    """
    Dados dos textos calcula la distancia de jaccard.
    k es la longitud de los shingles
    """
    shingles1 = create_shingles(string1,k)
    shingles2 = create_shingles(string2,k)
    intersection = len(set(shingles1).intersection(shingles2))
    #print(list(set(shingles1).intersection(shingles2)))
    union = (len(shingles1) + len(shingles2)) - intersection
    return 1-float(intersection / union)

def create_shingles(string,k):
    """
    Dado un texto los shingles que tenga de longitud k
    """
    shingles_list = []
    for i in range(len(string)-k+1):
        shingle = ''
        for j in range(k):
            shingle = shingle + string[i+j]
        shingles_list.append(shingle)
    return shingles_list
