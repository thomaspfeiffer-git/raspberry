#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import requests
import json

def get_and_sort_awattar_data():
    """
    Ruft Strommarktdaten von der aWATTar API ab und sortiert sie nach Preis.
    """
    url = "https://api.awattar.at/v1/marketdata"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Löst einen Fehler bei schlechten HTTP-Antworten aus (4xx oder 5xx)
        data = response.json()

        # Die Daten befinden sich unter dem Schlüssel 'data' und sind eine Liste von Dictionaries.
        # Wir sortieren diese Liste basierend auf dem Wert des Schlüssels 'marketprice'.
        if 'data' in data and isinstance(data['data'], list):
            sorted_data = sorted(data['data'], key=lambda x: x['marketprice'])
            return sorted_data
        else:
            print("Unerwartete Datenstruktur von der API erhalten.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None
    except json.JSONDecodeError:
        print("Fehler beim Parsen der JSON-Antwort.")
        return None
    except KeyError:
        print("Der Schlüssel 'marketprice' wurde in den Daten nicht gefunden. Überprüfen Sie die API-Antwortstruktur.")
        return None

if __name__ == "__main__":
    print("Rufe Strommarktdaten von aWATTar ab und sortiere sie nach Preis...\n")
    sorted_market_data = get_and_sort_awattar_data()

    if sorted_market_data:
        print("Sortierte Strommarktdaten (aufsteigend nach Kosten):")
        for entry in sorted_market_data:
            start_time_hr = entry.get('start_timestamp', 0) // 1000 // 3600 % 24 # Umrechnung in Stunden des Tages
            end_time_hr = entry.get('end_timestamp', 0) // 1000 // 3600 % 24
            price_eur_mwh = entry.get('marketprice', 'N/A')
            unit = entry.get('unit', 'N/A')
            # Konvertiere Preis von EUR/MWh zu ct/kWh für bessere Lesbarkeit
            price_ct_kwh = price_eur_mwh / 10 if isinstance(price_eur_mwh, (int, float)) else 'N/A'

            # Zeitstempel lesbar formatieren (optional, aber hilfreich)
            from datetime import datetime
            start_dt = datetime.fromtimestamp(entry.get('start_timestamp', 0) // 1000).strftime('%Y-%m-%d %H:%M:%S')
            end_dt = datetime.fromtimestamp(entry.get('end_timestamp', 0) // 1000).strftime('%Y-%m-%d %H:%M:%S')


            print(f"  Zeitraum: {start_dt} - {end_dt}, Preis: {price_ct_kwh} ct/kWh (Original: {price_eur_mwh} {unit})")

