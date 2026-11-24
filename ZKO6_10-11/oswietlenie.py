import math
import numpy as np
import matplotlib.pyplot as plt

#wagi tych cech 
waga_swiatlo = 1.5
waga_pora = 1.0
waga_ruch = 0.7


def dzwon(x, srodek, szerokosc):
    #funkcja gaussa dalje od 0 do 1 
    roznica = x - srodek
    return math.exp(-(roznica * roznica) / (2 * szerokosc * szerokosc))


def rozmyj(swiatlo, pora, ruch):
    #zmieniamy zwykle liczby na stopnie od 0 do 1 
    ciemno = min(1.0, dzwon(swiatlo, 15, 20) * waga_swiatlo)
    jasno = min(1.0, dzwon(swiatlo, 85, 20) * waga_swiatlo)
    noc = min(1.0, dzwon(pora, 22, 4) * waga_pora)
    dzien = min(1.0, dzwon(pora, 12, 4) * waga_pora)
    jest_ruch = min(1.0, dzwon(ruch, 80, 25) * waga_ruch)
    brak_ruchu = min(1.0, dzwon(ruch, 10, 25) * waga_ruch)

    return ciemno, jasno, noc, dzien, jest_ruch, brak_ruchu


def wnioskuj(ciemno, jasno, noc, dzien, jest_ruch, brak_ruchu):
    #reguly: and -> min, or -> max
    regula_duzo_1 = min(ciemno, jest_ruch)   #ciemno i jest ruch -> dużo światła
    regula_duzo_2 = min(ciemno, noc)         #ciemno I noc -> dużo światła
    duzo = max(regula_duzo_1, regula_duzo_2)

    regula_srednio_1 = min(ciemno, brak_ruchu) #ciemno i brak ruchu -> średnio
    regula_srednio_2 = min(jasno, jest_ruch)  #jasno i ruch -> średnio
    srednio = max(regula_srednio_1, regula_srednio_2)

    malo = max(jasno, brak_ruchu)             #jasno LUB brak ruchu -> mało światła

    return malo, srednio, duzo


def wyostrz(malo, srednio, duzo):
    #liczenie srodka ciezkosci dla jasnosci lampy 
    licznik = 0.0
    mianownik = 0.0

    for jasnosc in range(0, 101, 2):
        #przycinanie kazdego dzwonu wyjscia do siły
        k_malo = min(malo, dzwon(jasnosc, 15, 15))
        k_srednio = min(srednio, dzwon(jasnosc, 50, 15))
        k_duzo = min(duzo, dzwon(jasnosc, 85, 15))

        #łaczenie do wspolnego kształtu 
        wspolny_ksztalt = max(k_malo, k_srednio, k_duzo)

        licznik = licznik + (jasnosc * wspolny_ksztalt)
        mianownik = mianownik + wspolny_ksztalt

    if mianownik == 0:
        return 0.0
    return licznik / mianownik


def policz_jasnosc(swiatlo, pora, ruch):
    c, j, n, d, r, br = rozmyj(swiatlo, pora, ruch)
    m, s, dz = wnioskuj(c, j, n, d, r, br)
    wynik = wyostrz(m, s, dz)
    return wynik


#test
jasnosc_test = policz_jasnosc(swiatlo=10, pora=23, ruch=70)
print("Jasność lampy:", round(jasnosc_test, 1), "%")



#===============================================================================
# --- WYKRES 1: Światło i pora dnia (ruch stały = 70) ---
os_swiatlo = np.linspace(0, 100, 25)
os_pora = np.linspace(0, 24, 25)
S1, P1 = np.meshgrid(os_swiatlo, os_pora)
Z1 = np.zeros((25, 25))

for i in range(25):
    for j in range(25):
        Z1[i, j] = policz_jasnosc(S1[i, j], P1[i, j], ruch=70)

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection="3d")
ax1.plot_surface(S1, P1, Z1, cmap="plasma")
ax1.set_xlabel("Światło z zewnątrz [%]")
ax1.set_ylabel("Pora dnia [h]")
ax1.set_zlabel("Jasność lampy [%]")
ax1.set_title("Wykres 1: Światło vs Pora dnia (ruch = 70)")


# --- WYKRES 2: Światło i ruch (pora dnia stała = 21:00) ---
os_ruch = np.linspace(0, 100, 25)
S2, R2 = np.meshgrid(os_swiatlo, os_ruch)
Z2 = np.zeros((25, 25))

for i in range(25):
    for j in range(25):
        Z2[i, j] = policz_jasnosc(S2[i, j], pora=21, ruch=R2[i, j])

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection="3d")
ax2.plot_surface(S2, R2, Z2, cmap="viridis")
ax2.set_xlabel("Światło z zewnątrz [%]")
ax2.set_ylabel("Ruch [%]")
ax2.set_zlabel("Jasność lampy [%]")
ax2.set_title("Wykres 2: Światło vs Ruch (pora = 21:00)")

plt.show()