import json

def main():
    plik = open('bezrobocie.json', 'r', encoding='utf-8')
    baza = json.load(plik)
    plik.close()

    odpowiedzi_uzytkownika = {}
    print("SEKCJA PYTAŃ")
    
    for id_pytania, dane_pytania in baza["questions"].items():
        print("\n" + dane_pytania["text"])
        opcje = dane_pytania["answers"]
        
        for i, opcja in enumerate(opcje):
            print(f"{i + 1}. {opcja}")
            
        while True:
            wybor = input("Twój wybór (podaj cyfrę): ")

            if wybor.isdigit() and 1 <= int(wybor) <= len(opcje):
                wybrana_odpowiedz = opcje[int(wybor) - 1]
                odpowiedzi_uzytkownika[id_pytania] = wybrana_odpowiedz
                break 
            else:
                print("Błąd! Podaj poprawną cyfrę z listy.")

    print("\n WYNIK")
    znaleziono_regule = False
    
    for regula in baza["rules"]:
        warunki = regula["if"]
        czy_pasuje = True 
        
        for id_pytania, wymagana_odpowiedz in warunki.items():
            if odpowiedzi_uzytkownika.get(id_pytania) != wymagana_odpowiedz:
                czy_pasuje = False
                break 

        if czy_pasuje:
            znaleziono_regule = True
            print(f"Diagnoza: {regula['then']['diagnosis']}")
            print(f"Porada:   {regula['then']['action']}\n")
            
    if not znaleziono_regule:
        print("Brak pasujących reguł dla Twoich odpowiedzi.")

if __name__ == "__main__":
    main()