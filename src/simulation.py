
def simulation(groupes,G):
    #initialisation
    resultat = [0 for _ in range(len(groupes))]
    D_init = {}
    arret_max,encomb_max = (0,1),1
    for i in range(len(groupes)):
        cycle = groupes[i][1]
        arrete = cycle[0]
        if arrete in D_init:
            D_init[arrete].append(i)
        else:
            D_init[arrete] = [i]
    T = {0:D_init}
    #ecoulement du temps
    t = 0
    while 0 in resultat:
        D = T.get(t, {})
        for arrete in D:
            lst = D[arrete]
            k = sum([len(groupes[i][0]) for i in lst]) - 1
            if k >= encomb_max :
                encomb_max = G[arrete[0]][arrete[1]] + k
                arret_max = arrete
            tps_add = G[arrete[0]][arrete[1]] + k
            for g in lst:
                avance = groupes[g][-1]
                if avance == len(G)+1:
                    resultat[g] = t
                    groupes[g][-1] = 1
                else:
                    arr_suiv = groupes[g][1][avance]
                    t_future = t + tps_add
                    if t_future not in T:
                        T[t_future] = {}
                    if arr_suiv in T[t_future]:
                        T[t_future][arr_suiv].append(g)
                    else:
                        T[t_future][arr_suiv] = [g]
                    groupes[g][-1] += 1
        t += 1
    return resultat,arret_max,encomb_max