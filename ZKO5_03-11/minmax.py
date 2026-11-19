import math

n = int(input("Rozmiar planszy (np. 3): "))
depth = int(input("Maksymalna głębokość (np. 4): "))
komp_first = input("Czy komputer zaczyna? (t/n): ") == 't'

board = [[' ']*n for _ in range(n)]
KOMP, HUMAN = ('X', 'O') if komp_first else ('O', 'X')

def wygrana(b, p):
    r = len(b)
    return any(all(b[i][j] == p for j in range(r)) for i in range(r)) or \
           any(all(b[j][i] == p for j in range(r)) for i in range(r)) or \
           all(b[i][i] == p for i in range(r)) or \
           all(b[i][r-1-i] == p for i in range(r))

def minimax(b, d, is_max):
    if wygrana(b, KOMP): return 10 - d
    if wygrana(b, HUMAN): return d - 10
    if ' ' not in [c for row in b for c in row] or d == 0: return 0
    
    r = len(b)
    best = -math.inf if is_max else math.inf
    for i in range(r):
        for j in range(r):
            if b[i][j] == ' ':
                b[i][j] = KOMP if is_max else HUMAN
                val = minimax(b, d - 1, not is_max)
                b[i][j] = ' '
                best = max(best, val) if is_max else min(best, val)
    return best

#główna pętla gry
tura_komp = komp_first
while True:
    for row in board: print(row)
    if wygrana(board,KOMP): print("Komputer wygrał!"); break
    if wygrana(board, HUMAN): print("Wygrałeś!"); break
    if ' ' not in [c for row in board for c in row]: print("Remis!"); break

    if tura_komp:
        print("Komputer myśli...")
        best_val, best_move = -math.inf, None
        for i in range(n):
            for j in range(n):
                if board[i][j] == ' ':
                    board[i][j] = KOMP
                    val = minimax(board, depth - 1, False)
                    board[i][j] = ' '
                    if val > best_val: best_val, best_move = val, (i, j)
        board[best_move[0]][best_move[1]] = KOMP
        tura_komp = False
    else:
        try:
            r, c = map(int, input(f"Twój ruch (wiersz kolumna od 0 do {n-1}): ").split())
            #sprawdzamy czy współrzędne mieszczą się na planszy
            if 0 <= r < n and 0 <= c < n:
                if board[r][c] == ' ':
                    board[r][c] = HUMAN
                    tura_komp = True
                else:
                    print("Pole jest już zajęte! Wybierz inne.")
            else:
                print(f"Błąd! Wpisz liczby z zakresu od 0 do {n-1}.")
        except ValueError:
            print("Wpisz dwie liczby oddzielone spacją, np. 1 2")