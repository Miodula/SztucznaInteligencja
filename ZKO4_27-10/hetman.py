import random

N = 8

def ocena(osobnik):
    bledy = 0
    for i in range(N):
        for j in range(i + 1, N):
            if osobnik[i] == osobnik[j] or abs(i - j) == abs(osobnik[i] - osobnik[j]):
                bledy += 1
    return bledy

def rysuj_szachownice(osobnik):
    print("\nSzachownica ([H] - Hetman, [ ] - puste pole):")
    for wiersz in range(N):
        linia = ""
        for kolumna in range(N):
            if osobnik[wiersz] == kolumna:
                linia += "[H]" #hetman
            else:
                linia += "[ ]" #puste pole
        print(linia)
    print("\nReprezentacja w liście:", osobnik)

populacja = []
for _ in range(100):
    osobnik = []
    for _ in range(N):
        osobnik.append(random.randint(0, N - 1))
    populacja.append(osobnik)

for pokolenie in range(10000):
    
    populacja.sort(key=ocena)
    najlepszy = populacja[0]
    
    if ocena(najlepszy) == 0:
        print(f"\nZnaleziono rozwiązanie w {pokolenie} pokoleniu.")
        rysuj_szachownice(najlepszy)
        break
        
    nowe_pokolenie = populacja[:10] #top 10 najlepszych

    while len(nowe_pokolenie) < 100:
        ojciec = random.choice(populacja[:50])
        matka = random.choice(populacja[:50])
        
        dziecko = ojciec[:4] + matka[4:]
        
        if random.randint(1, 100) <= 20:
            losowy_wiersz = random.randint(0, N - 1)
            nowa_kolumna = random.randint(0, N - 1)
            dziecko[losowy_wiersz] = nowa_kolumna
            
        nowe_pokolenie.append(dziecko)
        
    #podmianka starej populcji na nowa 
    populacja = nowe_pokolenie