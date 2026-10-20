import time
import os
import sys

KOLOR_CZERWONY = '\033[1;31m'    # Start
KOLOR_ZIELONY = '\033[1;32m'     # Odwiedzone
KOLOR_ZOLTY = '\033[1;33m'       # Czeka w kolejce
KOLOR_NIEBIESKI = '\033[1;34m'   # Koniec
KOLOR_FIOLETOWY = '\033[1;35m'   # Ostateczna znaleziona droga
KOLOR_DOMYSLNY = '\033[0m'       # Zwykłe pole

# kierunki 
GORA = (-1, 0)
DOL = (1, 0)
PRAWO = (0, 1)
LEWO = (0, -1)

AKCJE = {
    '┼': [GORA, DOL, PRAWO, LEWO],
    '┤': [GORA, DOL, LEWO],
    '│': [GORA, DOL],
    '┴': [GORA, PRAWO, LEWO],
    '─': [PRAWO, LEWO],
    '├': [GORA, DOL, PRAWO],
    '┌': [DOL, PRAWO],
    '┬': [DOL, PRAWO, LEWO],
    '┐': [DOL, LEWO],
    '╵': [GORA],
    '┘': [GORA, LEWO],
    '╷': [DOL],
    '└': [GORA, PRAWO],
    '╴': [LEWO],
    '╶': [PRAWO],
    ' ': [] 
}

ODWROTNY_KIERUNEK = {
    GORA: DOL,
    DOL: GORA,
    PRAWO: LEWO,
    LEWO: PRAWO
}

def wczytaj_mape(sciezka):
    plik = open(sciezka, 'r', encoding='utf-8')
    linie = plik.read().splitlines()
    plik.close()
    
    maks_dlugosc = 0
    for linia in linie:
        if len(linia) > maks_dlugosc:
            maks_dlugosc = len(linia)
            
    mapa = []
    for linia in linie:
        mapa.append(linia.ljust(maks_dlugosc, ' '))
        
    return mapa


def rysuj_mape(mapa, start, koniec, odwiedzone, oczekujace, znaleziona_droga=None):
    if znaleziona_droga is None:
        znaleziona_droga = []
        
    os.system('cls' if os.name == 'nt' else 'clear')
    
    for y in range(len(mapa)):
        for x in range(len(mapa[0])):
            pozycja = (y, x)
            znak = mapa[y][x]
            
        
            if pozycja == start:
                print(KOLOR_CZERWONY + znak + KOLOR_DOMYSLNY, end="")
            elif pozycja == koniec:
                print(KOLOR_NIEBIESKI + znak + KOLOR_DOMYSLNY, end="")
            elif pozycja in znaleziona_droga:
                print(KOLOR_FIOLETOWY + znak + KOLOR_DOMYSLNY, end="")
            elif pozycja in oczekujace:
                print(KOLOR_ZOLTY + znak + KOLOR_DOMYSLNY, end="")
            elif pozycja in odwiedzone:
                print(KOLOR_ZIELONY + znak + KOLOR_DOMYSLNY, end="")
            else:
                print(KOLOR_DOMYSLNY + znak + KOLOR_DOMYSLNY, end="")
        print() 

# sprawdzenie gdzie mozna isc 
def pobierz_sasiadow(mapa, y, x):
    sasiedzi = []
    znak = mapa[y][x]
    
    if znak not in AKCJE:
        return sasiedzi
        
    for ruch_y, ruch_x in AKCJE[znak]:
        nowe_y = y + ruch_y
        nowe_x = x + ruch_x
        
        if 0 <= nowe_y < len(mapa) and 0 <= nowe_x < len(mapa[0]):
            znak_sasiada = mapa[nowe_y][nowe_x]
            if znak_sasiada in AKCJE:
                wymagany_kierunek = ODWROTNY_KIERUNEK[(ruch_y, ruch_x)]
                if wymagany_kierunek in AKCJE[znak_sasiada]:
                    sasiedzi.append((nowe_y, nowe_x))
                    
    return sasiedzi


def szukaj_sciezki(mapa, start, koniec, algorytm):
    lista_pol = [(start, None)] 
    
    odwiedzone = []
    skad_przyszlismy = {} 
    kroki = 0
    
    while len(lista_pol) > 0:
        if algorytm == "BFS":
            obecne, poprzednie = lista_pol.pop(0) 
        elif algorytm == "DFS":
            obecne, poprzednie = lista_pol.pop()  
            
        if obecne in odwiedzone:
            continue
            
        odwiedzone.append(obecne)
        

        if poprzednie is not None:
            skad_przyszlismy[obecne] = poprzednie
            
        kroki += 1
        
        tylko_pozycje_oczekujace = []
        for pole, skad in lista_pol:
            tylko_pozycje_oczekujace.append(pole)
            
        rysuj_mape(mapa, start, koniec, odwiedzone, tylko_pozycje_oczekujace)
        time.sleep(0.05) # zmieniłem sobie sam zeby było szybciej 
        
        if obecne == koniec:
            droga_do_celu = []
            krok = koniec
            
            while krok in skad_przyszlismy:
                droga_do_celu.append(krok)
                krok = skad_przyszlismy[krok] 
                
            rysuj_mape(mapa, start, koniec, odwiedzone, tylko_pozycje_oczekujace, droga_do_celu)
            return True, kroki
            
        # dodawanie sąsiadów
        sasiedzi = pobierz_sasiadow(mapa, obecne[0], obecne[1])
        for sasiad in sasiedzi:
            if sasiad not in odwiedzone:
                lista_pol.append((sasiad, obecne))
                
    return False, kroki

def main():
    sciezka = sys.argv[1] 
    mapa = wczytaj_mape(sciezka)
    
    wysokosc = len(mapa)
    szerokosc = len(mapa[0])
    
    for linia in mapa:
        print(linia)
        
    print(f"Rozmiar: {szerokosc} x {wysokosc}")
    
    start_x, start_y = input("Podaj START (x y): ").split()
    koniec_x, koniec_y = input("Podaj KONIEC (x y): ").split()
    algorytm = input("Wybierz algorytm (BFS lub DFS): ").upper()
    
    start = (int(start_y), int(start_x))
    koniec = (int(koniec_y), int(koniec_x))
    
    znaleziono, kroki = szukaj_sciezki(mapa, start, koniec, algorytm)
    
    if znaleziono:
        print(f"\nSUKCES! Znaleziono droge (pokolorowana na fioletowo - kod {KOLOR_FIOLETOWY}FIOLETOWY{KOLOR_DOMYSLNY}).")
    else:
        print("\nPORAZKA. Brak drogi.")
    print(f"Liczba wykonanych krokow: {kroki}")

if __name__ == "__main__":
    main()