
def permutations(elements):
    if not elements:
        return [[]]
    res = []
    for i in range(len(elements)):
        reste = elements[:i] + elements[i+1:]
        for p in permutations(reste):
            res.append([elements[i]] + p)
    return res

#methode heuristque
def glouton(G,start):
    ch = [start]
    while len(ch) != len(G)+1:
        #voisin de s de poids min
        vtot = G[ch[-1]]
        v = [t for t in vtot if t[0] not in ch]
        if len(ch) == len(G):
            s_min, p_min = vtot[0]
            for som, p_som in vtot:
                if som == start :
                    s_min = som
                    p_min = p_som
        elif len(ch) != len(G):
            s_min, p_min = v[0]
            for som,p_som in v :
                if som not in ch and p_som <= p_min:
                    s_min = som
                    p_min = p_som

        ch.append(s_min)
    return ch

#methode exacte
def force_brute(M, d):
    n = len(M)
    R = [i for i in range(n) if i != d]
    # Fonction pour générer toutes les permutations de la liste L
    def perm(L):
        if len(L) <= 1:
            return [L]
        res = []
        for i in range(len(L)):
            p = L[i]
            reste = L[:i] + L[i + 1:]
            for pr in perm(reste):
                res.append([p] + pr)
        return res
    cycles = [[d] + p + [d] for p in perm(R)]
    best_c = float('inf')
    best_p = None
    for c in cycles:
        cout = 0
        for i in range(n):
            u = c[i]
            v = c[i + 1]
            cout += M[u][v]
        if cout < best_c:
            best_c = cout
            best_p = c

    return best_p, best_c

def branch_and_bound(G, depart=0):
    nombre_sommets = len(G)

    def poids_arete(u, v):
        for voisin, poids in G[u]:
            if voisin == v:
                return poids
        return float('inf')

    # poids minimum sortant de chaque sommet
    arete_min = []
    for u in range(nombre_sommets):
        minimum = float('inf')
        for _, poids in G[u]:
            if poids < minimum:
                minimum = poids
        arete_min.append(minimum)

    def borne_inferieure(chemin, cout):
        non_visites = []
        for i in range(nombre_sommets):
            if i not in chemin:
                non_visites.append(i)

        somme = cout
        for sommet in non_visites:
            somme += arete_min[sommet]

        return somme

    meilleur_cout = float('inf')
    meilleur_chemin = None

    pile = [(depart, [depart], 0)]

    while pile:
        sommet, chemin, cout = pile.pop()

        if len(chemin) == nombre_sommets:
            w = poids_arete(sommet, depart)
            if w != float('inf'):
                total = cout + w
                if total < meilleur_cout:
                    meilleur_cout = total
                    meilleur_chemin = chemin + [depart]
            continue

        borne = borne_inferieure(chemin, cout)
        if borne >= meilleur_cout:
            continue

        for voisin, poids in G[sommet]:
            if voisin not in chemin:
                pile.append((voisin, chemin + [voisin], cout + poids))

    meilleur_chemin = [(meilleur_chemin[i], meilleur_chemin[i+1])
                       for i in range(len(meilleur_chemin)-1)]

    return meilleur_chemin, meilleur_cout

def held_karp(M, d=0):
    nb_sommets = len(M)
    memoire = {}

    def chemin_opti(sommets_restants, sommet_actuel):
        if len(sommets_restants) == 0:
            return (M[sommet_actuel][d], [d])

        etat = (sommets_restants, sommet_actuel)
        if etat in memoire:
            return memoire[etat]

        cout_min = float('inf')
        meilleur_chemin = []

        for prochain_sommet in sommets_restants:
            nouveaux_restants = tuple(s for s in sommets_restants if s != prochain_sommet)
            cout_suite, chemin_suite = chemin_opti(nouveaux_restants, prochain_sommet)
            cout_total = M[sommet_actuel][prochain_sommet] + cout_suite
            if cout_total < cout_min:
                cout_min = cout_total
                meilleur_chemin = [prochain_sommet] + chemin_suite
        memoire[etat] = (cout_min, meilleur_chemin)
        return memoire[etat]

    sommets = tuple(s for s in range(nb_sommets) if s != d)
    cout_final, chemin_final = chemin_opti(sommets, d)
    cycle = [d] + chemin_final

    cycle_complet = [(cycle[i],cycle[i+1]) for i in range(len(cycle)-1)] + [(cycle[0],cycle[1])]
    return cout_final, cycle_complet