import random as rd

def graphe(n, m):
    matrice = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            poids = rd.randint(1, m)
            poids = poids if rd.random() <= 0.6 else float("inf")
            matrice[i][j] = poids
            matrice[j][i] = poids
    return matrice