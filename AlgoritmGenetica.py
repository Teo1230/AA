import random
from math import ceil, log2

def valoareinfunctiex(a, b, c, x):
    return a * x ** 2 + b * x + c

def conv(bin,ia,ib):
    nr = int(bin, 2)
    l = len(bin)
    d = (ib - ia) / (2 ** l)
    st = ia + nr * d
    return st

def binary_search(intervale, prob):
    left = 0
    right = len(intervale)-1

    while left <= right:
        mid = (left + right) // 2

        if prob < intervale[mid][0]:
            right = mid - 1
        elif prob >= intervale[mid][1]:
            left = mid + 1
        else:
            return mid

    return -1
with open('input.txt', 'r') as f:
    dimensiuneapop = int(f.readline().strip())
    ia, ib = map(int, f.readline().strip().split())
    a, b, c = map(int, f.readline().strip().split())
    precizie = float(f.readline().strip())
    probRecombinare = float(f.readline().strip()) / 100
    probMutatie = float(f.readline().strip()) / 100
    nrEtape = int(f.readline().strip())
f.close()
ls=[]
F = 0
populatie = {}
for i in range(1, 1 + dimensiuneapop):
    # print(i)
    x = random.uniform(ia, ib)
    val = valoareinfunctiex(a, b, c, x)
    F += val
    l = ceil(log2((ib - ia) * (10 ** precizie)))
    d = (ib - ia) / (2 ** l)
    st = ia + int((x - ia) / d) * d
    dr = int((x - ia) / d)
    binary_repr = format(dr, f"0{l}b")
    if i not in populatie.keys():
        populatie[i]=[i,binary_repr,x,val,0]

individetilist=[0,"",a-1,0]
with open('output.txt', 'w') as f:
    f.write("Populatie initiala: \n")
    for i in range(1,1+dimensiuneapop):
        if populatie[i][3] >= individetilist[3]:
            individetilist[0]=populatie[i][0]
            individetilist[1]=populatie[i][1]
            individetilist[2]=populatie[i][2]
            individetilist[3]=populatie[i][3]

        populatie[i][4]= populatie[i][3] / F
        f.write(f"{populatie[i]}\n")
        # print(populatie[i])
    f.write(f"Probabilitati selectie:  \n")
    intervale = []
    st = 0
    for i in populatie:
        dr = st + populatie[i][4]
        intervale.append((st, dr))
        st = dr

    f.write("\nIntervare probabilitati selectie (stanga):\n")
    for i in range(len(intervale)):
        f.write(f"{intervale[i][0]}\n")
        if i==len(intervale)-1:
            f.write(f"{intervale[i][1]}\n")
    for k in range(nrEtape):
        print(f"INDIVID MAXIM: {individetilist} \n")

        populatieNoua = {}
        populatieNoua[1]=individetilist
        for i in range(2, 1 + dimensiuneapop):
            prob = random.uniform(0, 1)
            index = binary_search(intervale, prob)
            if index != -1:
                f.write(f"u={prob} selectam cromozomul {index+1}\n")
                x=populatie.get(index+1)
                # print(x)
                # print(x,index)
                populatieNoua[i] = x

        f.write("Dupa selectie: \n")
        # print(populatieNoua)
        for i in range(1,1+dimensiuneapop):
            f.write(f"{i}: {populatieNoua[i][1:]}\n")




        f.write(f"\nProbabilitatea de incrucisare {probRecombinare} \n")
        lista_incrucisare = []
        for i in range(2, 1 + dimensiuneapop):
            probincr = random.uniform(0, 1)
            if probincr <= probRecombinare:
                f.write(f"{i}: {populatieNoua[i][1]} u={probincr}< {probRecombinare} participa\n")
                ide, binar, x, fx, val = populatieNoua[i]
                ide = i
                lista_incrucisare.append([ide, binar, x, fx, val])

                # remove this line
                # if i not in lista_incrucisare.keys():
                #     lista_incrucisare[i]=[ide,binar,x,fx,val]
            else:
                f.write(f"{i}: {populatieNoua[i][1]} u={probincr}\n")
        for i in range(0,len(lista_incrucisare)):
            f.write(f"{i}, {lista_incrucisare[i]} \n")

        # print("lg este" ,len(lista_incrucisare)-1)

        # f.write(f"Luungime este {len(lista_incrucisare)}\n")
        if (len(lista_incrucisare))%2==0:
            for i in range(0, 1+len(lista_incrucisare)-1, 2):
                # print(i)
                c1 = lista_incrucisare[i]
                c2 = lista_incrucisare[i + 1]
                # print(c1,c1[0])
                # print(c2,c2[0])
                punctrupere = random.randint(0, dimensiuneapop - 1)
                puncturupere1=random.randint(punctrupere, dimensiuneapop - 1)
                c1_new = c1[1][:punctrupere] + c2[1][punctrupere:puncturupere1]+ c1[i][puncturupere1:]
                c2_new = c2[1][:punctrupere] + c1[1][punctrupere:puncturupere1]+ c2[i][puncturupere1:]
                f.write(
                    f"Recombinare dintre cromozomul {c1[0]} si {c2[0]} cu punctul {punctrupere}\n")
                f.write(f"{c1[1]} {c2[1]}\n")
                f.write(f"Rezultat {c1_new}={conv(c1_new, ia, ib)} {c2_new}={conv(c2_new, ia, ib)}\n")
                for i in populatieNoua:
                    if populatieNoua[i][1]==individetilist[1]:
                        continue
                    if i == c1[0]:
                        binar = c1_new
                        x = conv(binar, ia, ib)
                        fx = valoareinfunctiex(a, b, c, x)
                        populatieNoua[i][1] = binar
                        populatieNoua[i][2] = x
                        populatieNoua[i][3] = fx
                    if i == c2[0]:
                        binar = c2_new
                        x = conv(binar, ia, ib)
                        fx = valoareinfunctiex(a, b, c, x)
                        populatieNoua[i][1] = binar
                        populatieNoua[i][2] = x
                        populatieNoua[i][3] = fx
        elif len(lista_incrucisare)>=3:
            for i in range(0, len(lista_incrucisare)-3, 2):
                # print(i)
                c1 = lista_incrucisare[i]
                c2 = lista_incrucisare[i + 1]
                # print(c1,c1[0])
                # print(c2,c2[0])
                punctrupere = random.randint(0, dimensiuneapop - 1)
                c1_new = c1[1][:punctrupere] + c2[1][punctrupere:]
                c2_new = c2[1][:punctrupere] + c1[1][punctrupere:]
                f.write(f"Recombinare dintre cromozomul {c1[0]} si {c2[0]} cu punctul {punctrupere}\n")
                f.write(f"{c1[1]} {c2[1]}\n")
                f.write(f"Rezultat {c1_new}={conv(c1_new, ia, ib)} {c2_new}={conv(c2_new, ia, ib)}\n")
                for i in populatieNoua:
                    if populatieNoua[i][1] == individetilist[1]:
                        continue
                    if i == c1[0]:
                        binar = c1_new
                        x = conv(binar, ia, ib)
                        fx = valoareinfunctiex(a, b, c, x)
                        populatieNoua[i][1] = binar
                        populatieNoua[i][2] = x
                        populatieNoua[i][3] = fx
                    if i == c2[0]:
                        binar = c2_new
                        x = conv(binar, ia, ib)
                        fx = valoareinfunctiex(a, b, c, x)
                        populatieNoua[i][1] = binar
                        populatieNoua[i][2] = x
                        populatieNoua[i][3] = fx
            c1 = lista_incrucisare[-3]
            c2 = lista_incrucisare[-2]
            c3= lista_incrucisare[-1]
            # print(c1,c1[0])
            # print(c2,c2[0])
            # print(c3,c3[0])

            punctrupere = random.randint(0, dimensiuneapop - 1)
            c1_new = c1[1][:punctrupere] + c2[1][punctrupere:]
            c2_new = c2[1][:punctrupere] + c3[1][punctrupere:]
            c3_new = c3[1][:punctrupere] + c1[1][punctrupere:]
            f.write(f"Recombinare dintre cromozomul {c1[0]} si {c2[0]} si {c3[0]} cu punctul {punctrupere}\n")
            f.write(f"{c1[1]} {c2[1]} {c3[1]}\n")
            f.write(f"Rezultat {c1_new}={conv(c1_new, ia, ib)} {c2_new}={conv(c2_new, ia, ib)} {c3_new}={conv(c3_new, ia, ib)}\n")
            for i in populatieNoua:
                if populatieNoua[i][1] == individetilist[1]:
                    continue
                if i == c1[0]:
                    binar = c1_new
                    x = conv(binar, ia, ib)
                    fx = valoareinfunctiex(a, b, c, x)
                    populatieNoua[i][1] = binar
                    populatieNoua[i][2] = x
                    populatieNoua[i][3] = fx
                if i == c2[0]:
                    binar = c2_new
                    x = conv(binar, ia, ib)
                    fx = valoareinfunctiex(a, b, c, x)
                    populatieNoua[i][1] = binar
                    populatieNoua[i][2] = x
                    populatieNoua[i][3] = fx
                if i == c3[0]:
                    binar = c3_new
                    x = conv(binar, ia, ib)
                    fx = valoareinfunctiex(a, b, c, x)
                    populatieNoua[i][1] = binar
                    populatieNoua[i][2] = x
                    populatieNoua[i][3] = fx

        f.write(f"\nDupa recombinare: \n")
        for i in range(1, 1 + dimensiuneapop):
            f.write(f"{i}: {populatieNoua[i]}\n")
        f.write(f"Probabilitate de mutatie pentru fiecare gena {probMutatie}\n")
        f.write("Au fost modificati cromozomii: \n")
        for i in range(2,dimensiuneapop+1):
            x =  populatieNoua.get(i)
            # print(x)
            bin=list(x[1])
            ok = False
            for j in bin:
                probbit = random.uniform(0, 1)
                if probbit <= probMutatie:
                    bin[i] = '1' if bin[i] == '0' else '0'
                    ok = True
                    poz=i
            result = ''.join(bin)
            if ok:
                for j in populatieNoua:
                    if j==i:
                        populatieNoua[j][1] = result
                        populatieNoua[j][2] = conv(result, ia, ib)
                        populatieNoua[j][3] = valoareinfunctiex(a, b, c, populatieNoua[i][2])
                f.write(f" {i} {populatieNoua[i]} \n")
        f.write("Dupa mutatie: \n")
        mx=-1
        dev=0
        for i in range(1, len(populatieNoua)):
            if populatie[i][3] >= individetilist[3]:
                individetilist[0] = populatie[i][0]
                individetilist[1] = populatie[i][1]
                individetilist[2] = populatie[i][2]
                individetilist[3] = populatie[i][3]

            dev=dev+populatieNoua[i][3]
            f.write(f"{i}: {populatieNoua[i]}\n")
        ls.append((individetilist[3],dev/dimensiuneapop))
    import matplotlib.pyplot as plt

    for i, j in ls:
        f.write(f"{i} {j}\n")

    max_values = [t[0] for t in ls]
    mean_values = [t[1] for t in ls]


    plt.plot(range(1, nrEtape + 1), max_values, label='Maximul functiei max f(Xi), Vi=1,nrEpoci')


    plt.plot(range(1, nrEtape + 1), mean_values, label='Mean funtiei 1/n ∑f(Xi), Vi=1,nrEpoci')


    plt.title('Evolutia functiei in NrEtape')
    plt.xlabel('NrEtape')
    plt.ylabel('Valorea functie(fit)')


    plt.legend()


    plt.show()
