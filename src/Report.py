#region Description
# --------------------------------------------------------------------------------------------------------
# Reportfunktion:
# Wenn komplett = False dann wird nur Top 10 ausgegeben.
# Wenn komplett = True  dann werden alle Daten ausgegeben. Wird für den alles_ausgebenen REport gebraucht.
# --------------------------------------------------------------------------------------------------------
#endregion Description


#region Import
from pathlib import Path
from Utils import umrechnung_gb, zeitstempel, tabelle_formatieren
#endregion Import


#region Function | report_erstellen
def report_erstellen(scan_ergebnis,top10,komplett):                                                                 # Nimmt die Werte aus "scan_ergebnis", "top10" und komplett
    spalten = []                                                                                                    # Erstellt als erstes ein Leeres Array und füllt danach alles was für die Ausgabe gewünscht ist, ab.

    spalten.append("======================= Report =======================\n")                                      # Start der "Report" auflistung.
    spalten.append(f"Startpfad:      {scan_ergebnis["start_pfad"]}")                                                # Hängt den Inhalt aus "start_pfad" der Liste an.
    spalten.append(f"Anzahl Ordner:  {scan_ergebnis["anzahl_ordner"]}")                                             # Hängt den Inhalt aus "anzahl_ordner" der Liste an.
    spalten.append(f"Anzahl Dateien: {scan_ergebnis["anzahl_dateien"]}")                                            # Hängt den Inhalt aus "anzahl_dateien" der Liste an.
    spalten.append(f"Gesamtgrösse:   {umrechnung_gb(scan_ergebnis["gesamt_bytes"])}")                               # Hängt den umgerechneten Inhalt aus "gesamt_bytes" der Liste an.
    spalten.append("")                                                                                              # Hängt eine "leere Zeile" an.

    spalten.append("--------------- Top 10 Grösste Dateien ---------------")                                        # Start der "Top 10" ausgabe mit dem Schriftzug.

    if not top10:                                                                                                   # Falls die Variable "top10" leer ist, wird eine Meldung generiert. 
        spalten.append("(Keine Dateien gefunden)")
        
    else:
        top10_formatiert = tabelle_formatieren(top10)                                                               # Die Top10 Liste wird schön Formatiert und der variabel spalten sauber übergeben.
        spalten.extend(top10_formatiert)                                                                            # ...und der Liste "spalten" angehängt.

    spalten.append("")

    if komplett:                                                                                                    # True or False um diese Ausgabe nur in die Datei zu schreiben ohne Konsolenausgabe.
        spalten.append("-------------------- Alle Dateien --------------------")                                    # Start der "dateien" ausgabe mit dem Schriftzug.

        dateien = scan_ergebnis["dateien"]                                                                          # Die auszugebenden Daten werden in "dateien" geschrieben.
        if not dateien:                                                                                             # Falls die Variable "dateien" leer ist, wird eine Meldung generiert. 
            spalten.append("(Keine Dateien gefunden)")
        else:
            dateien_formatiert = tabelle_formatieren(dateien)                                                       # Die Dateien Liste wird schön Formatiert und der variabel spalten sauber übergeben.
            spalten.extend(dateien_formatiert)                                                                      # ...un der Liste "spalten" angehängt.

    spalten.append("")

    spalten.append("----------------- Fehler und Hinweise ----------------")
    if not scan_ergebnis["fehler"]:                                                                                 # Falls der Key: Fehler leer ist, wird eine entsprechende Meldung ausgegeben
        spalten.append("Keine Probleme festgestellt.")
    else:
        for i in scan_ergebnis["fehler"]:                                                                           # Jedes Objekt im Key: Fehler wird in die Liste geschrieben
            spalten.append("- " + i)

    return "\n".join(spalten)                                                                                       # Die gesammte Liste wird nun mit spaltenumbrüchen pro Eintrag in die Variabel "report_konsole" übergeben.
#endregion Function | report_erstellen

#region Function | report_speichern
def report_speichern(report_datei):                                                                                 # Diese Funktiopn speichert den Report in die korrekte Datei.
    ordner = Path(__file__).parent.parent                                                                           # Schreibt den Pfad (absolut) des darüberliegenden Ordners ohne Dateinamen von report.py in die Variabel "ordner"

    reports = ordner / "Reports"                                                                                    # Reports wird als unterordner definiert.
    reports.mkdir(exist_ok=True)                                                                                    # Erstellt den "Reports" ordner wenn er noch nicht da ist.

    dateiname = (f"Report_{zeitstempel()}.txt")                                                                     # Mit der Funktion "Zeitstempel", wird die aktuelle Zeit und  Datum für den Dateinamen ermittelt.  
    pfad = reports / dateiname                                                                                      # TXT-Datei wird mit dem aktuellen Zeitstempel definiert und mit dem zielordner zusammengesetzt.

    pfad.write_text(report_datei, encoding="utf-8")                                                                 # Die TXT-Datei wird erstellt und mit dem Inhalt befüllt. Mit "encoding= utf-8" werden die Umlaute korrekt geschrieben.
    return pfad                                                                                                     # Der Absolute Pfad des Speicherorts wird an "gespeichert" zurückgegeben.
#endregion Function | report_speichern