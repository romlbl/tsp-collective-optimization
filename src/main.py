from graphe_generation import graphe
from tsp_algorithms import held_karp
import matplotlib.pyplot as plt
import seaborn as sns
from share_network import methode1, methode2

m = 5
data = [[0 for _ in range(10)] for _ in range(10)]
for n in range(5,15):
    for nb in range(1,10+1):
        subdata = []
        for _ in range(5):
            G = graphe(n,m)
            while True:
                try:
                    p, cycle = held_karp(G, 0)
                    t_nul = p * nb
                    groupes = [[[i for i in range(nb)], cycle, 1]]
                    t_opti = methode2(groupes, G)
                    subdata.append((t_nul - t_opti) / t_nul)
                    break
                except:
                    G = graphe(n, m)
        val = round(sum(subdata)/len(subdata),2)
        print(n,nb,val)
        data[nb-1][n-5] = val


index_colonnes = list(range(5, 5 + len(data[0])))
index_ligne = list(range(1, 1 + len(data)))

plt.figure(figsize=(6, 5))
ax = sns.heatmap(data, cmap="YlGn",xticklabels=index_colonnes,yticklabels=index_ligne, annot=True,annot_kws={"alpha": 0.7},vmax=0.7)
ax.invert_yaxis()
plt.title("Réseau partagé")
plt.ylabel("Nombre de colis")
plt.xlabel("Ordre du graphe")
plt.show()