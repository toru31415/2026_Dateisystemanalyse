#region Description
#  --------------------------------------------------------------------
# Löschen mit Sicherheit:
# 1) Testlauf (zeigt nur an, was gelöscht würde)
# 2) Bestätigung
# 3) zweite Bestätigung
# 4) echtes Löschen
# --------------------------------------------------------------------
#endregion Description


#region Import
from pathlib import Path
from Utils import frage,tabelle_formatieren
#endregion Import


#region Function | dateien_löschen_start
def dateien_löschen_start(top10,treffer_liste):
    print("\n================ Dateien löschen =====================")
    if frage("\nMöchtest du Dateien löschen? (j/n): "):                                                 # Der Input vom User wird der Funktion "frage" übergeben, um die Eingabe zu prüfen.
        datenwahl(top10,treffer_liste)                                                                  # Wenn die Eingabe Ja ist, wird dir Hauptfunktion der Datenwahl aktiviert.
#endregion Function | dateien_löschen_start

#region Function | datenwahl -> Diese Funktion ist dazu da um die zu löschenden Daten auszuwählen.
def datenwahl(top10, treffer_liste):                                                                    # Diese Funktion ist dazu da um die zu löschenden Daten auszuwählen.
    auswahl = {"1", "2"}                                                                                # Definiert welche Zahl welche Liste ist

    print("Welche Liste willst du als Grundlage nehmen?")
    print("1 = Top 10 Liste")
    print("2 = Trefferliste")
    wahl = input("Auswahl (1/2): ").strip()                                                             # Fragt welche Liste genommen werden soll.

    while wahl not in auswahl:                                                                          # Solange die Eingabe nicht 1 oder 2 ist...
        wahl = input("Auswahl (1/2): ").strip()                                                         # ...wird nochmals gefragt.

    if wahl == "1":                                                                                     # Falls die wahl 1 ist...
        quelle = top10                                                                                  # Wird der inhalt von "top10" in die Variabel "quelle" übernommen.
    elif wahl == "2":                                                                                   # Falls die wahl 2 ist...
        quelle = treffer_liste                                                                          # Wird der inhalt von "top10" in die Variabel "quelle" übernommen

    if not quelle:                                                                                      # Überprüft die Variable "quelle" auf Inhalt.
        wahl2 = frage("Die ausgewählte Liste ist leer. Möchtest du eine andere Liste wählen? (j/n):")   # Falls leer, wird gefrtagt, ob eine andere Liste genommen werden soll.
        if wahl2 is True:                                                                               # Falls ja, dann wird die Funktion "datenwahl" erneut gestartet.
            datenwahl(top10, treffer_liste)
        else:                                                                                           # Fall keine neue Liste gewählt wird, geht es zurück ins Hauptmenü.
            return
    else:
        löschvorgang_starten(quelle)
#endregion Function | datenwahl

#region Function | löschvorgang_starten
def löschvorgang_starten(quelle):
    print("\n-------------------- Dateiauswahl --------------------")
    print("\n".join(tabelle_formatieren(quelle)))                                                       # Die gewählte Liste wird vollständig ausgegeben, um auch jedes element auswählen zu können.

    while True:
        nummern = input("\nWelche Nummern löschen? (z.B. 1,3,5) oder leer = abbrechen: ").strip()       # Frage zur Auswahl der zu löschenden Daten.
        if not nummern:                                                                                 # Falls keine Nummern ausgewählt werden, gehts zurück zum hauptmenü.
            print("Der Vorgang wird abgebrochen und es werden keine Daten gelöscht.")
            return

        auswahl = []                                                                                    # Es wird eine Leere Liste erstellt.
        for i in nummern.split(","):                                                                    # Die eingabe wird durch iteriert und am komma getrennt und einzeln verarbeitet.
            i = i.strip()                                                                               # Entfernt leerschläge zwischen den Kommas / vorne und hinter der Zahl.
            if i.isdigit():                                                                             # Prüft ob die Eingabe eine Zahl ist.
                nummer = int(i)                                                                         # Wandelt die Nummer in einen Integer um.
                if 1 <= nummer <= len(quelle):                                                          # Die Nummer muss mindestens 1 sein und kleiner als 
                    auswahl.append(quelle[nummer - 1])                                                  # Erst dann wird der entsprechende Eintrag der auswahl hinzugefügt. -1 weil das erste Element in der Liste bei 0 ist.

        if not auswahl:                                                                                 # Falls die auswahl leer ist, wird die Frage wiederholt.
            print("Keine gültige Auswahl getroffen.")
            continue
        break                                                                                           # Falls alles stimmt wird die Schleife abgebrochen.
    
    testlauf_anzeigen(auswahl)                                                                          # Startet den Testlauf um die Daten zu löschen

    if not frage("\nSoll wirklich gelöscht werden? (j/n): "):                                           # Erste Bestätigung, dass die Daten gelöscht werden sollen
        print("Der Vorgang wird abgebrochen und es werden keine Daten gelöscht.")
        return

    if not frage("Bist du dir WIRKLICH sicher? (j/n): "):                                               # Zweite Bestätigung, dass die Daten gelöscht werden sollen
        print("Der Vorgang wird abgebrochen und es werden keine Daten gelöscht.")
        return

    stats = dateien_löschen(auswahl)                                                                    # Die gewählten Daten werden gelöscht und die Fehler in "stats" gespeichert (dictionary).

    print("\n----------------------- Ergebnis ---------------------")                                   # Start der Ergebniszeile
    print("Gelöscht:", stats["gelöscht"])                                                               # Listet die Anzahl der gelöschten Elemente auf.
    print("Fehlgeschlagen:", stats["fehlgeschlagen"])                                                   # Listet die Anzahl der fehlgeschlagenen Elemente auf.
    for i in stats["meldungen"]:                                                                        # Iteriert durch die Meldungen um sie eine nach dem anderen auszugeben.
        print("-", i)
#endregion Function | löschvorgang_starten

#region Function | testlauf_anzeigen
def testlauf_anzeigen(auswahl):
    print("\n------ TESTLAUF: Diese Dateien werden gelöscht ------")

    if not auswahl:
        print("(Keine Dateien ausgewählt)")                                                             # Zeigt an, dass keine Daten zum löschen ausgewält wurden.
        return                                                                                          # Unterbricht nur die Funktion. So kann ein kleines Testszenario geschaffen werden.

    print("\n".join(tabelle_formatieren(auswahl)))                                                      # Die auswahl wird formatiert zurückgegeben.
#endregion Function | testlauf_anzeigen

#region Function | dateien_löschen
def dateien_löschen(auswahl):                                                                           # Funktion um die Daten wirklich zu löschen.
    stats = {                                                                                           # Erstellt ein Dictionary um Infos abzufangen und speichern.
        "gelöscht": 0,
        "fehlgeschlagen": 0,
        "meldungen": []
    }

    for d in auswahl:                                                                               
        try:
            Path(d["abspfad"]).unlink()                                                                 # Für jedes element in der Variabel (dict) "auswahl" wird Absolute Pfad ausgelesen und die Datei gelöscht.
            stats["gelöscht"] += 1                                                                      # Falls erfolgreich, wird der Zähler erhöht.
        except OSError:                                                                                 # Falls etwas fehlschlägt, wird das festghehalten.
            stats["fehlgeschlagen"] += 1                                                                # Fehlerzähler geht eins nach oben.
            stats["meldungen"].append(f"Nicht gelöscht: {d['relpfad']}")                                # Das nicht gelöschte Element wird dem Key "meldungen" angehängt.

    return stats                                                                                        # Nun wird das ganze DICT wieder zurückgegeben.
#endregion Function | dateien_löschen