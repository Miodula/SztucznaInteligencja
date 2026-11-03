import tkinter as tk
from tkinter import filedialog
import math
import heapq
import time

#zmienne
wierzcholki = {} 
graf = {}         
start = 1
cel = 4

#pitagoras zeby obliczyc odległość miedzy punktami 
def oblicz_odleglosc(w1, w2):
    x1, y1 = wierzcholki[w1]
    x2, y2 = wierzcholki[w2]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def narysuj_wezel(numer, kolor):
    x = wierzcholki[numer][0] * 50
    y = wierzcholki[numer][1] * 50
    plotno.create_oval(x-10, y-10, x+10, y+10, fill=kolor)
    plotno.create_text(x, y, text=str(numer))

def wczytaj_i_narysuj():
    global start, cel
    sciezka = filedialog.askopenfilename(filetypes=[("Pliki txt", "*.txt")])
    if not sciezka:
        return
    
    plik = open(sciezka, 'r')
    linie = plik.readlines()
    plik.close()
    
#czyszczenie starych danych grafu 
    wierzcholki.clear()
    graf.clear()
    plotno.delete("all")
    etykieta_wynik.config(text="Koszt: ---")
    
    liczba_wierzcholkow = int(linie[0])
    cel = liczba_wierzcholkow 
    
    #wspołrzedne
    for i in range(1, liczba_wierzcholkow + 1):
        dane = linie[i].split()
        wierzcholki[i] = (int(dane[0]), int(dane[1]))
        
    #sasiedzi
    for i in range(1, liczba_wierzcholkow + 1):
        dane = linie[liczba_wierzcholkow + i].split()
        sasiedzi = [int(x) for x in dane[1:]] 
        graf[i] = sasiedzi

   #rysowanie lini grafu 
    for w1, sasiedzi in graf.items():
        x1 = wierzcholki[w1][0] * 50
        y1 = wierzcholki[w1][1] * 50
        for w2 in sasiedzi:
            x2 = wierzcholki[w2][0] * 50
            y2 = wierzcholki[w2][1] * 50
            plotno.create_line(x1, y1, x2, y2, fill="lightgray")

    #wezły
    for w in wierzcholki:
        if w == start:
            narysuj_wezel(w, "lime") #start
        elif w == cel:
            narysuj_wezel(w, "red")  #cel
        else:
            narysuj_wezel(w, "white") #reszta

#główny algorytm
def szukaj_drogi():
    wybrany_algorytm = lista_algorytmow.get()
    
    kolejka = [] #kolejka priorytetowa 
    heapq.heappush(kolejka, (0, start)) #start narazie z priorytetem 0
    
    poprzednicy = {start: None} #do narysowania sciezki
    koszty = {start: 0}       #g(n)
    
    while len(kolejka) > 0: #wziecie kolejki z najmniejszym priorytetem
        priorytet, obecny = heapq.heappop(kolejka)
        
        if obecny != start and obecny != cel:
            narysuj_wezel(obecny, "yellow")
            okno.update()       
            time.sleep(0.05)  
            
        
        if obecny == cel:
            break
            
        #sprawdzamy sąsiadów
        for sasiad in graf[obecny]:
            nowy_koszt = koszty[obecny] + oblicz_odleglosc(obecny, sasiad)
            
            # Jeśli znaleźliśmy lepszą (krótszą) drogę do sąsiada
            if sasiad not in koszty or nowy_koszt < koszty[sasiad]:
                koszty[sasiad] = nowy_koszt
                poprzednicy[sasiad] = obecny
                
                #obliczanie szacowanej odleglosci do celu
                h = oblicz_odleglosc(sasiad, cel)
                
                if wybrany_algorytm == "Dijkstra":
                    p = nowy_koszt   # f(n) = g(n)
                elif wybrany_algorytm == "Best First Search":
                    p = h          # f(n) = h(n)
                else: #algorytm A*
                    p = nowy_koszt + h   # f(n) = g(n) + h(n)
                    
                heapq.heappush(kolejka, (p, sasiad))
                
    #odtwarzanie drogi
    if cel in poprzednicy:
        krok = cel
        while krok != start:
            poprzedni_krok = poprzednicy[krok]
            
            #rysowanie czerwonej linii
            x1 = wierzcholki[krok][0] * 50
            y1 = wierzcholki[krok][1] * 50
            x2 = wierzcholki[poprzedni_krok][0] * 50
            y2 = wierzcholki[poprzedni_krok][1] * 50
            plotno.create_line(x1, y1, x2, y2, fill="red", width=3)
            
            krok = poprzedni_krok
            
        etykieta_wynik.config(text=f"Koszt: {round(koszty[cel], 2)}")
    else:
        etykieta_wynik.config(text="Brak drogi!")

#interfejs
okno = tk.Tk()
okno.title("Grafy")

naglowek = tk.Frame(okno)
naglowek.pack(pady=5)

przycisk_wczytaj = tk.Button(naglowek, text="Wczytaj Graf", command=wczytaj_i_narysuj)
przycisk_wczytaj.pack(side=tk.LEFT, padx=5)

lista_algorytmow = tk.StringVar(value="A*")
opcje = ["Best First Search", "Dijkstra", "A*"]
tk.OptionMenu(naglowek, lista_algorytmow, *opcje).pack(side=tk.LEFT, padx=5)

przycisk_szukaj = tk.Button(naglowek, text="Start!", command=szukaj_drogi, bg="lightgreen")
przycisk_szukaj.pack(side=tk.LEFT, padx=5)

etykieta_wynik = tk.Label(naglowek, text="Koszt: ---", font=("Arial", 12, "bold"))
etykieta_wynik.pack(side=tk.LEFT, padx=20)

plotno = tk.Canvas(okno, width=800, height=600, bg="white")
plotno.pack()

okno.mainloop()