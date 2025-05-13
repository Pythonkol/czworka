import logging

logging.basicConfig(level=logging.INFO, format = '%(message)s')

Typ_obl = input("Podaj działanie, posługując się odpowiednią liczbą: 1 Dodawanie, 2 Odejmowanie, 3 Mnożenie, 4 Dzielenie: ")

x=int(input("podaj pierwszą cyfrę: "))
y=int(input("podaj drugą cyfrę: "))

if Typ_obl =="1":
    logging.info(f"Dodawanie {x} i {y} ")
    koncowy = x + y
elif Typ_obl =="2":
    logging.info(f"Odejmowanie {x} i {y} ")
    koncowy = x - y
elif Typ_obl =="3":
    logging.info(f"Mnożenie {x} i {y} ")
    koncowy = x * y
elif Typ_obl =="4":
    logging.info(f"Dzielenie {x} i {y} ")
    koncowy = x / y
else:
    print ("Nieprawidłowe działanie")
    Typ_obl = None

if Typ_obl is not None:
    print(f"Wynik to {koncowy}")