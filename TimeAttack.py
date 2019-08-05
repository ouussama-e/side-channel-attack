#!/usr/bin/env python3

import random
import time

DEBUG = True

def rand():
    return random.randint(0, 2147483647)


calcul = [0 for i in range(100)]  # int calcul[100];


# Fonction puissance
def puissance(a, b):
    if b == 0:
        return 1
    if b == 1:
        return a
    tmp = puissance(a, b//2)
    if b % 2 == 0:
        return tmp*tmp
    else:
        return tmp*tmp*a


# Génération d'un nombre premier entre 5 et 199
# avec l'algorithme de Miller-Rabin
def premier(q):
    while True:
        m = rand() % 200
        if (m < 5) or (m == q):
            continue

        # ecriture de m : m=2^s*t
        s = 0
        m2 = m - 1
        while m2 % 2 == 0:
            m2 /= 2
            s += 1

        t = (m-1) // puissance(2, s)
        # test de primalite
        cpt = 0
        while cpt < 20:
            a = rand() % (m-1) + 1
            u = (puissance(a,t)) % m
            if u == 1:
                b = True
            else:
                i = 0
                b = False
                while (i < s) and (b == 0):
                    if (u == m-1) or (u == -1):
                        b = True
                    else:
                        b = False
                    u = (u*u) % m
                    i += 1
            if not b:
                cpt = 21
            else:
                cpt += 1
        if cpt <= 20:
            break
    return m


#/* test la validite de e */
def check(phi, e):
    # test 1: imparite
    if e % 2 == 0:
        return False
    # test 2: primalite avec phi
    i = 3
    while i <= e:
        if e % i == 0 and phi % i == 0:
            return False
        i += 2
    return True


#/* chiffrement */
def encrypte(M, e, n):
    C = 1
    #i = 0
    for i in range(e):
    #while i < e:
        C = C * M % n
    #    i += 1
    C = C % n

    # Make M printable.
    if M < 32:
        M = 32
    print("\tCaractere %c chiffre : %d" % (chr(M), C))
    return C


#/* dechiffrement */
def decrypte(C, d_lg, n, clef):
    # pour l'exponentiation modulaire
    s = []
    R = []


    data_list = []

    s.append(1)
    for i in range(d_lg):
        # *********** CALCUL DE TEMPS ****************
        start = time.perf_counter()

        repeat_count = 1000
        alea = rand()
        for j in range(repeat_count):
            if clef[d_lg-1-i] == 1:
                if alea < 2147483647/2:
                    Ri = s[i]
                else:
                    for k in range(11):
                        pass
                Ri = s[i] * C % n
            else:
                if alea < 2147483647/2:
                    Ri = s[i] * C % n
                else:
                    for k in range(11):
                        pass
                Ri = s[i]

        # *********** CALCUL DE TEMPS ****************
        end = time.perf_counter()

        R.append(Ri)


        tm = (end - start) * 1000000000 // repeat_count  # nanoseconds
        # affichage du temps
        print("temps de l'iteration %d: %d nsec" % (i, tm))

        s.append((Ri * Ri) % n)
        data_list.append( (tm, i) )

    data_list.sort(key = lambda x: x[0])

    ecart = 0
    ecart_bis = 0

    # calcul du plus grand écart et indices correspondants
    j = 0
    for d in data_list:
        # hypothèse: il y a au moins environ 30% de zéros et de uns
        if (j >= (d_lg/3)-1 and j <= d_lg-(d_lg/3) and
           j+1 < len(data_list) and (data_list[j+1][0] - d[0]) > ecart):
            ecart = data_list[j+1][0] - d[0]
            ind_ecart = j
        elif j+1 < len(data_list) and (data_list[j+1][0] - d[0]) > ecart:
            ecart_bis = data_list[j+1][0] - d[0]
            ind_ecart_bis = j
        j += 1


    # si l'ecart est nul
    if ecart == 0:
        ecart = ecart_bis
        ind_ecart = ind_ecart_bis

    # impression de la clef
    clef_estimee = [0 for i in range(100)]  # int clef_estimee[100];

    # attribution des zéros
    for j in range(ind_ecart+1):
        d = data_list[j]
        clef_estimee[d[1]] = 0
        if d[1] == 0:
            # la clef est impaire
            clef_estimee[d[1]] = 1
            calcul[d[1]] += 1

    # attribution des uns
    for i in range(ind_ecart+1, len(data_list)):
        d = data_list[i]
        clef_estimee[d[1]] = 1
        calcul[d[1]] += 1

    print("Clef estimee:\t ", end="")
    for j in range(1, d_lg):
        print(clef_estimee[j], end=" ")

    M = R[d_lg - 1]
    print("\tCaractere decrypte : %c" % M)



#/* Conversion de d en binaire */
def convert(d):
    clef = []
    q = 1
    i = 0
    while q != 0:
        q = d // 2
        r = d % 2
        d = q
        clef.append(r)
        i += 1
        j = i
    print("\tClef en binaire\t: ", end="")
    i = j-1
    while i >= 0:
        #printf("%d ", clef[i]);
        print(clef[i], end=" ")
        i -= 1
    print()
    return (j, clef)


#/* Fonction principale */
def main():
    # Generation des nombres premiers pour la clef
    if DEBUG:
        p = 193
        q = 13
    else:
        p = premier(0)
        q = premier(p)
    print("\nNombres premiers:\np=%d\tq=%d" % (p, q))

    # Calculs de n et phi
    n = p*q
    phi = (p-1)*(q-1)
    print("Phi(n)= %d\n" % phi)

    # verification du 'e' entre
    while True:
        e = int(input("Entrez e: "))
        if check(phi, e):
            break

    # recherche de d
    d = 1
    while ((d*e) % phi) != 1:
        d += 1

    # affichage des clefs
    print("\tClef publique\t: {%d,%d}" % (e, n))
    print("\tClef privee\t: {%d,%d}" % (d, n))

    clef = []  #[100];

    # conversion de la clef en binaire
    d_lg, clef = convert(d)
    # recuperation du message a chiffrer
    print("\nEntrez le message a crypter:")

    # message a crypter
    pt = input()  # input() strips a trailing newline.

    code = [ encrypte(ord(m), e, n) for m in pt ]

    print()

    for c in code:
        decrypte(c, d_lg, n, clef)

    # affichage de la clef estimee
    print("\tClef finale estimee:\t", end="")
    for i in range(d_lg):
        if calcul[i] > (len(pt)/2):
            print("1", end="")
        else:
            print("0", end="")

    print()
    return 0


if __name__ == "__main__":
    main()
