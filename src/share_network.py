from simulation import simulation
from tsp_algorithms import held_karp

def repartition(liste, d):
    n = len(liste)
    taille_de_base = n // d
    reste = n % d

    listes_finales = []
    index = 0

    for i in range(d):
        taille_actuelle = taille_de_base + (1 if i < reste else 0)
        listes_finales.append(liste[index : index + taille_actuelle])
        index += taille_actuelle

    return listes_finales

def methode1(groupes,G,nb):
    arretes_bannie = []
    div = 2
    t_deb,t_fin = float('inf'), 0
    meilleur_tps = t_deb
    while t_fin < t_deb:
        rslt_deb,art_mx,pd_mx = simulation(groupes, G)
        t_deb = max(rslt_deb)
        arretes_bannie.append((art_mx,pd_mx))
        #modif graphe
        M = [l.copy() for l in G]
        for ar,pd in arretes_bannie:
            M[ar[0]][ar[1]] = pd
        #nouveau cycle
        _,cycle_opti = held_karp(M,0)
        #essai
        grp_tmp = []
        sous_grp = repartition([i for i in range(nb)],div)[::-1]
        if [] not in sous_grp:
            for k in range(len(sous_grp)-1):
                grp_tmp.append([sous_grp[k],groupes[k][1],1])
            grp_tmp.append([sous_grp[-1], cycle_opti, 1])
            rslt_fin,_,_ = simulation(grp_tmp, G)
            t_fin = max(rslt_fin)
            groupes = grp_tmp
            div += 1
        else:
            break
        if t_fin <= meilleur_tps:
            meilleur_tps = t_fin

    return meilleur_tps

def methode2(groupes,G):
    t_deb,t_fin = float('inf'), max(simulation(groupes,G)[0])
    meilleur_tps = t_deb
    while t_fin < t_deb:
        t_deb = max(simulation(groupes,G)[0])
        stock = groupes.copy()
        for g in range(len(stock)):
            lst,c,_ = stock[g]
            M = [l.copy() for l in G]
            k = len(lst)
            if k >= 2:
                # modif du graphe (methode calcul poids nouveau cycle)
                for i in range(len(c)-1):
                    a,d = c[i]
                    val = G[a][d] + k - 1
                    M[a][d] = val
                    M[d][a] = val
                #calcule nouveau cycle
                _,cycle_opti = held_karp(M,0)
                #essai
                essai_grp = [[lst[:k//2],c,1],[lst[k//2:],cycle_opti,1]] + groupes[:g] + groupes[g+1:]
                t_essai = max(simulation(essai_grp,G)[0])
                if t_essai < t_deb:
                    groupes = essai_grp

        t_fin = max(simulation(groupes, G)[0])
        # print(groupes,t_fin)
        # print("-----")
        if t_fin <= meilleur_tps:
            meilleur_tps = t_fin

    return meilleur_tps