import random

import numpy as np

pary = [(-5, -150), (-4, -77), (-3, -30), (-2, 0), (-1, 10), (1 / 2, 131 / 8), (1, 18), (2, 25), (3, 32), (4, 75), (5, 130)]

def funkcja(x, wspolczynniki):
    a,b,c,d = wspolczynniki
    return a * x ** 3 + b * x ** 2 + c * x + d

def funkcja_celu(wspolczynniki):
    wynik = 0
    for x, y in pary:
        wynik += (funkcja(x,wspolczynniki) - y)**2
    return wynik

def zakoduj_chromosom(wspolczynniki):
    chromosom = ''
    for x in wspolczynniki:
        if x > 0:
            chromosom += '1' + bin(x & 0b1111)[2:].zfill(4)
        elif x < 0:
            chromosom += '0' + bin(x*-1 & 0b1111)[2:].zfill(4)
        else:
            chromosom += '00000'
    return chromosom

def odkoduj_chromosom(chromosom):
    wspolczynniki = []
    for i in range(0, len(chromosom), 5):
        znak = int(chromosom[i])
        wartość = int(chromosom[i+1:i+5], 2)
        if znak == 0:
            wartość *= -1
        wspolczynniki.append(wartość)
    return wspolczynniki

def generuj_wspolczynniki():
    a = random.randint(-15, 15)
    b = random.randint(-15, 15)
    c = random.randint(-15, 15)
    d = random.randint(-15, 15)
    return (a,b,c,d)

def krzyzowanie(chromosom1, chromosom2):
    punkt = random.randint(0,20)
    return chromosom1[:punkt] + chromosom2[punkt:], chromosom2[:punkt] + chromosom1[punkt:]

def mutacja(chromosom):
    punkt = random.randint(0,19)
    if chromosom[punkt] == '1':
        if punkt == 20:
            chromosom = chromosom[:punkt] + "0"
        else:
            chromosom = chromosom[:punkt] + "0" + chromosom[punkt + 1:]
    else:
        if punkt == 20:
            chromosom = chromosom[:punkt] + "1"
        else:
            chromosom = chromosom[:punkt] + "1" + chromosom[punkt + 1:]
    return chromosom

def ruletka(populacja):
    wartosci = [funkcja_celu(odkoduj_chromosom(chromosom)) for chromosom in populacja]
    nowe_wartosci = [max(wartosci) - wynik + 1 for wynik in wartosci]
    wynik_suma = sum(nowe_wartosci)
    szansa = [wynik / wynik_suma for wynik in nowe_wartosci]
    return np.random.choice(populacja, size=len(populacja), p=szansa)


populacja = []
for i in range(300):
    populacja.append(zakoduj_chromosom(generuj_wspolczynniki()))
for i in range(300):
    for j in range(300):
        szansa = random.uniform(0,1)
        if szansa >= 0.25:
            indeks = random.choice([i for k in range(0, 299) if k != j])
            populacja[j], populacja[indeks] = krzyzowanie(populacja[j], populacja[indeks])
    for j in range(300):
        szansa = random.uniform(0,1)
        if szansa >= 0.10:
            populacja[j] = mutacja(populacja[j])
    populacja = ruletka(populacja)
    if i%10 == 0:
        print(f"{i} krok: Najlepsze rozwiazanie: {funkcja_celu(odkoduj_chromosom(populacja[i]))}\n dla wartosci {odkoduj_chromosom(populacja[i])}")
wartosci = [funkcja_celu(odkoduj_chromosom(chromosom)) for chromosom in populacja]
indeks = wartosci.index(min(wartosci))
print(f"Najlepsze rozwiazanie: {wartosci[indeks]}\n dla wartosci {odkoduj_chromosom(populacja[indeks])}")