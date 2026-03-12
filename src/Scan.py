#region Description
# --------------------------------------------------------------------
# Rekursiver Scan durch den gewählten Pfad / Ordner.
# --------------------------------------------------------------------
#endregion Description


#region Import
from Utils import pfad_aus_input
from Top10 import top_10_dateien
from Report import report_erstellen,report_speichern
from pathlib import Path
#endregion Import


#region Function | analyse_starten
def analyse_starten():
    print("\n============= Dateisystemanalyse starten =============")
    while True:                                                                                 # Solange kein gültiger Pfad eingegeben wird, wird die Frage wiederholt.
        eingabe = input("\nBitte einen Ordnerpfad eingeben (z.B. C:\\Users\\...): ")            # Fragt nach der Eingabe eines Pfades.
        start_pfad = pfad_aus_input(eingabe)                                                    # Übergibt die "eingabe" der Funktion: "pfad_aus_input" und speichert den Rückgabewert in der "start_pfad" Variable.

        if start_pfad is None:                                                                  # Pfüft ob ein Pfad eingegeben wurde.
            print("Bitte einen Pfad eingeben!")                                                 # Falls die Eingabe Leer ist, wird eine Meldung ausgegeben.
            continue

        if not start_pfad.exists():                                                             # Prüft ob der pfad nicht existiert.Wenn "True", dann...(Muss ein Ordner oder eine Datei sein)
            print("Dieser Pfad existiert nicht!")                                               # Wenn der Pfad nicht exisitiert, wird eine Meldung ausgegeben.
            continue

        if not start_pfad.is_dir():                                                             # Prüft ob der pfad keine Datei ist...Wenn "True", dann...(Muss ein Ordner sein und keine Datei)
            print("Der Pfad muss ein Ordner sein!")                                             # Wenn der Pfad eine Datei und kein Ordner ist, wird eine Meldung ausgegeben.
            continue
        break

    print("\nDer Scan läuft... bitte warten.")                                                  # Die Meldung "Scan läuft" wird angezeigt, damit man weiss, dass etwas passiert.
    scan_ergebnis = scan_ordner(start_pfad)                                                     # Scannt die Dateien: Die Variable "start_pfad" wird der Funktion "scan_ordner" aus dem Modul Scan übergeben und das Ergebnis des Scans in der neuen Variabel gespeichert

    top10 = top_10_dateien(scan_ergebnis["dateien"])                                            # Nimmt aus dem Scan den Key "dateien" (aus dem dictionary) und ermittelt damit die Top 10 grössten Dateien.

    report_konsole = report_erstellen(scan_ergebnis, top10, komplett=False)                     # Der ganze Report für die Konsole(nur top10) wird in "report_konsole" gespeichert und danach ausgegeben.
    print("\n" + report_konsole + "\n")

    report_datei = report_erstellen(scan_ergebnis, top10, komplett=True)                        # Der ganze Report wird in "report_datei" gespeichert und danach weiterverarbeitet.
    gespeichert = report_speichern(report_datei)
    bezugspfad = Path(__file__).parent.parent.parent                                            # Speichert den obersten Ordner des Tools in einer Variabel.
    relspeicherpfad = str(gespeichert.relative_to(bezugspfad))                                  # Damit nicht eine ellenlanger Pfad ausgegeben wird, wird nur der Relative Pfad zum obersten Projektordner in einer Variabel übernommen.
    print("----------------- Report Speicherort -----------------")                             # Der Report wird gespeichert und der Speicherpfad in die Variabel "gespeichert" übergeben und danach Ausgegeben.
    print(f"Der Report wird unter: {relspeicherpfad} gespeichert.\n")
    return top10,scan_ergebnis
#endregion Function | analyse_starten

#region Function | scan_ordner
def scan_ordner(start_pfad):
    resultat = {                                                                                # In der Variabel "resultat" wird ein dicionary erstellt.
        "start_pfad": str(start_pfad),                                                          # Der Startpfad als Text / string für die Ausgabe
        "anzahl_dateien": 0,                                                                    # Einfache Zahl der gefundene Dateien
        "anzahl_ordner": 0,                                                                     # Eiofache Zahl der gefundenen Unterordner
        "gesamt_bytes": 0,                                                                      # Gesamtgrösse in bytes (zusammengezählt)
        "fehler": [],                                                                           # Liste von Fehlermeldungen (wird erst später ausgegeben)
        "dateien": []                                                                           # Liste aller Dateien
    }
    rekursiver_scan(start_pfad, start_pfad, resultat)                                           # startet die Funktion mit dem rekursiven Scan.

    return resultat                                                                             # Gibt das Dict an die Variable scan-result im Main file zurück.
#endregion Function | scan_ordner

#region Function | rekursiver_scan
def rekursiver_scan(aktueller_ordner, start_pfad, resultat):                                    # Diese Funktion durchsucht den aktuellen Ordner und ruft sich bei einem Unterordner erneut auf. Falls es keinen Unterordner mehr gibt, wird die Funktion beendet.
    try:    
        for objekt in aktueller_ordner.iterdir():                                               # Mit .iterdir werden alle Order und Dateien im angegebenen Pfad durch iteriert und als Eintrag in der Variable "Objekt" als Pfad gespeichert"
            try: 
                if objekt.is_dir():                                                             # Wenn das aktuelle "Objekt" ein Ordner ist, 
                    resultat["anzahl_ordner"] += 1                                              # ...wird der Zähler um eins erhöht
                    rekursiver_scan(objekt, start_pfad, resultat)                               # ...und für den neuen Ordner wird die Funktion erneut rekursiv aufgerufen.

                elif objekt.is_file():                                                          # Wenn das aktuelle "Objekt" ein File ist,
                    resultat["anzahl_dateien"] += 1                                             # ...wird der Zähler um eins erhöht.

                    grösse_in_bytes = objekt.stat().st_size                                     # .stat ist teil des pathlib moduls und holt die Dateiinformationen vom Betriebssystem. in diesem Fall wird mit .st_size die Dateigrösse in Bytes genommen
                    resultat["gesamt_bytes"] += grösse_in_bytes                                 # grösse in bytes zum resultat dazuzählen (für die Gesammtgrösse)

                    rel_pfad = str(objekt.relative_to(start_pfad))                              # Mit .relative_to wird aus dem Pfad des aktuellen Dateipfads in der Variable "objekt", ein relativer Pfad, bezogen auf den Startpfad, erstellt und in die neue Variabel gespeichert.

                    dateiendung = objekt.suffix.lower() if objekt.suffix else "(keine)"         # Speichert die Dateiendung (.pdf oder .jpg) in die "dateiendung" Variable. Falls es keine Endung gibt...was bei pathlib sein kann, wird mit "(keine)" ergänzt, um beim Filter damit arbeiten zu können.

                    resultat["dateien"].append({                                                # Die gesammelten Dateiinfos werden unter dem Dict Key "dateien" als Liste gespeichert.
                        "abspfad": str(objekt),                                                 # Absoluter Pfad um den genauen Ort der Datei zu kennen
                        "relpfad": rel_pfad,                                                    # Relativer Pfad um die ausgabe übersichtlicher zu machen
                        "dateiname": objekt.name,                                               # Dateiname mit Endung für weitere Verarbeitung
                        "dateiendung": dateiendung,                                             # Dateiendung für weitere Verarbeitung
                        "bytes": grösse_in_bytes                                                # Dateigrösse in bytes für weitere Verarbeitung
                    })
            except PermissionError:                                                             # Keine Berechtigung auf dieses File.
                resultat["fehler"].append(f"Kein Zugriff: {objekt}")
            except FileNotFoundError:                                                           # File konnte nicht gefunden werden.
                resultat["fehler"].append(f"Nicht gefunden: {objekt}")
            except OSError:                                                                     # Allgemeine Fehler
                resultat["fehler"].append(f"Fehler beim Lesen: {objekt}")
    except PermissionError:                                                                     # Keine Berechtigung auf diesen Ordner.
        resultat["fehler"].append(f"Kein Zugriff: {aktueller_ordner}")
    except FileNotFoundError:                                                                   # Ordner konnte nicht gefunden werden.
        resultat["fehler"].append(f"Nicht gefunden: {aktueller_ordner}")
    except OSError:                                                                             # Allgemeine Fehler
        resultat["fehler"].append(f"Fehler beim Lesen: {aktueller_ordner}")
#endregion Function | rekursiver_scan