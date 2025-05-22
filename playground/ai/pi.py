#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-



import decimal
import time
import math

def calculate_pi_gauss_legendre(num_digits):
    """
    Berechnet Pi auf eine angegebene Anzahl von Stellen mit dem Gauss-Legendre-Algorithmus.
    Verwendet das Python 'decimal'-Modul.

    Args:
        num_digits (int): Die Gesamtzahl der signifikanten Stellen von Pi, die berechnet werden sollen (inklusive '3').

    Returns:
        str: Pi als String mit 'num_digits' signifikanten Stellen.
    """
    if num_digits <= 0:
        return ""
    if num_digits == 1:
        return "3"

    # Präzision für decimal-Berechnungen setzen.
    # Benötigt etwas mehr als num_digits für Guard-Digits zur Sicherstellung der Genauigkeit.
    # Ca. log10(num_digits) oder eine feste kleine Zahl (z.B. 10-15) als Guard-Digits.
    guard_digits = 15  # Sicherheitsmarge für die Präzision
    precision = num_digits + guard_digits
    decimal.getcontext().prec = precision

    # Startwerte für Gauss-Legendre
    a_n = decimal.Decimal(1)
    b_n = decimal.Decimal(1) / decimal.Decimal(2).sqrt()
    t_n = decimal.Decimal(1) / decimal.Decimal(4)
    p_n = decimal.Decimal(1)

    # Anzahl der Iterationen bestimmen.
    # Jede Iteration verdoppelt ungefähr die Anzahl der korrekten Stellen.
    # Daher werden ceil(log2(num_digits)) Iterationen benötigt.
    # Eine zusätzliche Iteration für erhöhte Sicherheit.
    # Für 10.000.000 Stellen: math.log2(10**7) ca. 23.25. Also 24 Iterationen.
    # Wir verwenden ceil(log2(num_digits)) + 1. Für 10^7 ist das 24 + 1 = 25 Iterationen.
    iterations = math.ceil(math.log2(num_digits)) + 1

    print(f"Starte {iterations} Iterationen des Gauss-Legendre-Algorithmus...")

    # Iterationsschleife
    for i in range(iterations):
        a_prev = a_n
        a_n = (a_prev + b_n) / 2
        b_n = (a_prev * b_n).sqrt()
        t_n = t_n - p_n * (a_prev - a_n)**2
        p_n = 2 * p_n
        if (i + 1) % 5 == 0 or i == iterations -1 : # Fortschrittsanzeige alle 5 Iterationen
             print(f"Iteration {i + 1}/{iterations} abgeschlossen. ({(time.time() - start_time_global)/3600:.2f} Stunden bisher)")


    # Pi berechnen
    pi_val = (a_n + b_n)**2 / (4 * t_n)

    # In String konvertieren und auf die gewünschte Anzahl Stellen kürzen.
    # str(pi_val) erzeugt einen String mit 'precision' Stellen.
    # Wir kürzen diesen auf 'num_digits'.
    pi_string = str(pi_val)

    return pi_string[:num_digits]


if __name__ == "__main__":
    N_DIGITS = 10_000_000  # Zielanzahl der Pi-Stellen

    print(f"Beginne mit der Berechnung von {N_DIGITS:,} Stellen von Pi.")
    print("ACHTUNG: Dies wird auf einem Raspberry Pi 4 mit dem Python 'decimal'-Modul")
    print("SEHR LANGE dauern (potenziell viele Stunden oder sogar Tage!).")
    print("Die Verwendung einer Bibliothek wie 'gmpy2' wäre DEUTLICH schneller.")
    print(f"Die Präzision des Decimal-Moduls wird auf {N_DIGITS + 15} Stellen gesetzt.")

    start_time_global = time.time() # Globale Startzeit für Fortschrittsanzeige in Iterationen

    calculated_pi = None
    try:
        calculated_pi = calculate_pi_gauss_legendre(N_DIGITS)
    except Exception as e:
        print(f"Ein Fehler ist während der Berechnung aufgetreten: {e}")
        import traceback
        traceback.print_exc()

    end_time_global = time.time()
    duration_seconds = end_time_global - start_time_global
    duration_hours = duration_seconds / 3600

    if calculated_pi:
        output_filename = f"pi_{N_DIGITS}_stellen.txt"
        try:
            with open(output_filename, "w") as f:
                f.write(calculated_pi)
            print(f"\nBerechnung von {N_DIGITS:,} Pi-Stellen erfolgreich abgeschlossen.")
            print(f"Die ersten 100 Stellen: {calculated_pi[:100]}")
            if N_DIGITS > 100:
                print(f"Die letzten 100 Stellen: {calculated_pi[-100:]}")
            print(f"Das Ergebnis wurde in der Datei '{output_filename}' gespeichert.")
        except IOError as e:
            print(f"Fehler beim Schreiben der Pi-Stellen in die Datei {output_filename}: {e}")
            print("Berechnete Pi-Stellen (erste 100):")
            print(calculated_pi[:100])

    print(f"Gesamte Berechnungszeit: {duration_seconds:.2f} Sekunden ({duration_seconds/60:.2f} Minuten oder {duration_hours:.2f} Stunden).")



