#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-


import requests
import datetime

def fetch_and_sort_prices():
    url = "https://api.awattar.at/v1/marketdata"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Daten: {response.status_code}")
        return

    data = response.json()["data"]

    # Umwandeln der Timestamps und Preise in lesbare Form
    preis_liste = []
    for eintrag in data:
        startzeit = datetime.datetime.fromtimestamp(eintrag["start_timestamp"] / 1000)
        endzeit = datetime.datetime.fromtimestamp(eintrag["end_timestamp"] / 1000)
        preis = eintrag["marketprice"] / 1000  # Umrechnung von €/MWh in €/kWh
        preis_liste.append({
            "start": startzeit,
            "ende": endzeit,
            "preis_ct_kwh": preis * 100  # in Cent/kWh
        })

    # Sortieren nach Preis
    preis_liste.sort(key=lambda x: x["preis_ct_kwh"])

    # Ausgabe
    print("⏰ Zeitfenster - 💶 Preis (Cent/kWh)")
    for eintrag in preis_liste:
        print(f"{eintrag['start']} - {eintrag['ende']}: {eintrag['preis_ct_kwh']:.2f} ct/kWh")

if __name__ == "__main__":
    fetch_and_sort_prices()

