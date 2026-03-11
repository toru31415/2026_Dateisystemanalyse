#region Description
# --------------------------------------------------------------------
# In dieser Datei sind Hilfsfunktionen, die mehrere andere Dateien nutzen.
# -> Pfade sauber einlesen
# -> Bytes in GB umrechnen
# -> Zeitstempel erstellen
# -> Ja/Nein-Fragen in der Konsole
# -> Reports-Ordner sicherstellen
# --------------------------------------------------------------------
#endregion Description


#region import
from pathlib import Path                                                                # Vereinfacht die Pfadangabe im Code. Beispiel: pfad = "C:\\Users\\Jemand" vs pfad = Path(r"C:\Users\Jemand")
from datetime import datetime                                                           # datetime braucht man für Datum/Uhrzeit im Report-Namen
#endregion Description

#region Function | pfad_aus_input
def pfad_aus_input(text):                                                               # Diese Funktion nimmt die Benutzereingabe (String) und macht daraus einen Path.
    text = text.strip()                                                                 # entfernt Leerzeichen vorne/hinten
    text = text.strip('"')                                                              # entfernt doppelte Anführungszeichen
    text = text.strip("'")                                                              # entfernt einfache Anführungszeichen
    return Path(text)                                                                   # gibt einen Path zurück
#endregion Function | pfad_aus_input

#region Function | umrechnung_gb
def umrechnung_gb(bytes_wert):
    gb = bytes_wert / (1024 ** 3)                                                       # Wandelt Bytes in Gigabyte um (1 GB sind 1024^3 Bytes).
    return f"{gb:.2f} GB"                                                               # Formatiert die Gigabyte Zahl mit 2 Nachkommastellen und erweitert die Ausgabe mit der Einheit.
#endregion Function | umrechnung_gb

#region Function | zeitstempel
def zeitstempel():                                                                      # Gibt einen Zeitstempel im Format Jahr-Monat-Tag_Stunde-Minute-Sekunde zurück
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")                                 # Nimmt die aktuelle Zeit. strtime wandelt die Ermittelte Zeit in einen String um.
#endregion Function | zeitstempel

#endregion Function | frage
def frage(frage):                                                                       # Die Funktion prüft die eingabe auf j/n oder Ja/nein.
    while True:                                                                         # Schleife, solange eine Falsche eingabe erfolgt.
        antwort = input(frage).strip().lower()                                          # Fragt nach einer Eingabe und entfernt die leerschläge vorne und hinten und macht die Zeichen klein.
        if antwort in ["j", "ja"]:
            return True                                                                 # Falls j oder ja eingegeben wird, wird die schleife verlassen und True zurückgegeben.
        if antwort in ["n", "nein"]:
            return False                                                                # Falls n oder nein eingegeben wird, wird die schleife verlassen und False zurückgegeben.
        print("Bitte nur 'j' oder 'n' eingeben.")
#endregion Function | frage

#region Function | tabelle_formatieren
def tabelle_formatieren (daten):                                                        # Diese Funktion wird verwendet um die Tabellen schön zu formatieren und danach wieder zurückzugeben.
    spalten = []

    umrechnung_gb_daten = [umrechnung_gb(d["bytes"]) for d in daten]                                                     # alle gespeiocherten werte unter dem Key "bytes" im dict "daten" werden in Gigabyte umgewandelt.
    position_weite = max(len("Position"), len(str(len(daten))))                                                          # Speichert den grösseren Wert von max(a, b) in der Variabel.
    grösse_gb_weite = max(len("Dateigrösse"), max(len(i) for i in umrechnung_gb_daten))                                  # Speichert den grösseren Wert von max(a, b) in der Variabel und nimmt beim zweiten max() die länge des längsten Objekts in "umrechnung_gb_daten".
    dateinamen_weite = max(len("Dateiname"), max(len(d["dateiname"]) for d in daten))                                    # Speichert den grösseren Wert von max(a, b) in der Variabel und nimmt beim zweiten max() die länge des längsten Objekts im Key "dateiname".
    relativerpfad_weite = max(len("Relativer Pfad"), max(len(str(Path(d["relpfad"]).parent)) for d in daten))            # Speichert den grösseren Wert von max(a, b) in der Variabel und nimmt beim zweiten max() die länge des längsten Objekts im Key "relpfad" ohne den Dateinamen.

    spalten.append(f"{"Position":<{position_weite}} | {"Dateigrösse":<{grösse_gb_weite}} | {"Dateiname":<{dateinamen_weite}} | {"Relativer Pfad zum Startpfad":<{relativerpfad_weite}}")        # linksbündige Kopfzeile mit den definierten Weiten (mit leerzeichen gefüllt).
    spalten.append(f"{"-"*position_weite}-+-{"-"*grösse_gb_weite}-+-{"-"*dateinamen_weite}-+-{"-"*relativerpfad_weite}")                                                                        # Erzeugt die dazu passende Trennlinie.

    for i, d in enumerate(daten, start=1):                                                                                                                                                      # daten wird iteriert (i = positionsnummer, d = aktueller Eintrag)
        relativerordner = str(Path(d["relpfad"]).parent)                                                                                                                                        # Trennt Pfad und Dateiname und nimmt nur den Pfad.
        spalten.append(f"{i:>{position_weite}} | {umrechnung_gb(d["bytes"]):>{grösse_gb_weite}} | {d["dateiname"]:<{dateinamen_weite}} | {relativerordner}")                                    # Inhalt von "daten" wird links- oder rechtsbündig in die Liste ergänzt.

    return spalten
#endregion Function | tabelle_formatieren