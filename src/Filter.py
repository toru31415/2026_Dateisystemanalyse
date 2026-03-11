#region Description
#  --------------------------------------------------------------------
# Filtert Dateien nach:
# - Dateiname enthält Text
# - Dateiendung ist in einer Liste (z.B. .jpg, .pdf)
# --------------------------------------------------------------------
#endregion Description


#region Import
from Utils import frage,tabelle_formatieren
#endregion Import


#region Function | filter_und_suche
def filter_und_suche(scan_ergebnis):
    print("\n================ Filter und Suche ====================")
    treffer_liste = []                                                                                          # Start der Suche, des Filters mit einer Leeren Liste.

    if frage("\nMöchtest du nach Dateinamen und/oder Endungen filtern? (j/n): "):                               # Ruft die Funktion auf um die Frage nach der eingabe zu prüfen (j/n).
        name_text = input("Der Dateiname enthält... (leer = kein Filter): ").strip()                            # Es kann nur nach einem Dateinamen gesucht werden / nach einer Eingabe alles mit dem gleichen namensinhalt aufgelistet werden.
        endung_text = input("Nach folgenden Endungen filtern... (z.B. .jpg,.pdf) oder leer: ").strip()          # Es können mehrere Dateiendungen ausgesucht werden.

        treffer_liste = dateifilter(scan_ergebnis["dateien"], name_text, endung_text)                           # Ruft die Funktion "dateifilter" auf und speichert die Rückgabe in der neuen Variabel.

        print("\n-------------------- Trefferliste --------------------")
        if not treffer_liste:                                                                                   # Falls es keine Treffer gibt, wird eine entsprechende meldung ausgegeben.
            print("(Keine Treffer)")
        else:
            print(filter_report(treffer_liste))                                                                 # Gibt die Formatierten Zeilen aus...
    return treffer_liste
#endregion Function | filter_und_suche

#region Function | dateifilter
def dateifilter(datenliste,name_text,endung_text):                                                              # Funktion um die Dateien zu filtern

    name_text = name_text or None                                                                               # Falls nichts eingegeben wurde wird die Variabel auf "None" gesetzt. Funktioniert nur, da vorher .strip() gemacht wird.
    if name_text:                                                                                               # Prüft die Variabel auf Inhalt
        name_text = name_text.lower()                                                                           # Macht die Zeichen in der Variabel alle klein.

    endungen = None                                                                                             # Standard inhalt der Variabel ist "None"
    if endung_text:                                                                                             # Falls etwas eingegeben wurde...
        endungen = []
        for i in endung_text.split(","):                                                                        # ...wird der Inhalt sauber beim komma getrennt.
            i = i.strip().lower()                                                                               # Bei jedem Eintrag einzeln: Leerzeichen vorne und hinten entfernen und die Zeichen klein machen.
            if not i:                                                                                           # Falls nun durch die Trennung leere Strings entstehen werden sie übersprungen.
                continue
            if i != "(keine)" and not i.startswith("."):                                                        # Falls bei einer Dateiendung welche nicht "(keine)" ist der Punkt vergessen wurde, wird dieser noch ergänzt.
                i = "." + i
            endungen.append(i)                                                                                  # Schliesslich wird der korrekt formatierte Eintrag der Liste ergänzt

    treffer = []                                                                                                # Ist die Liste für die gefilterten Treffer.

    for d in datenliste:                                                                                        # Iteriert durch die gesammte Datenliste
        prüfung = True                                                                                          # Wir gehen zum Start davon aus, dass alle Inhalte aus der Datenliste zum Filter passen.

        if name_text:                                                                                           # Wenn die Variabel "name_text" Inhalt hat...
            if name_text not in d["dateiname"].lower():                                                         # Es wird nun geprüft, ob der Filtertext nicht im Dateinamen enhalten ist. Falls True, wird das aktuelle Element auf False geändert.
                prüfung = False

        if prüfung and endungen:                                                                                # Falls in den Variablen etwas gepsiechert oder True ist....
            if d["dateiendung"] not in endungen:                                                                # Es wird nun geprüft, ob die Dateiendung nicht in "endungen" enhalten ist. Falls True, wird das aktuelle Element auf False geändert.
                prüfung = False

        if prüfung:                                                                                             # Falls "prüfung" = True, dann wird das aktuelle Element aus der Datenlist ein die Liste von der Variabel "treffer" angehängt.
            treffer.append(d)

    return treffer                                                                                              # Die sortierte Liste wird nun zurückgegeben.
#endregion Function | dateifilter

#region Function | filter_report
def filter_report(treffer_liste):
    formatiert = tabelle_formatieren(treffer_liste)                                                             # Formatiert die Liste mit der Vorlage in Utils.
    return "\n".join(formatiert)                                                                                # Die Formatierte Liste wird zurückgegeben.
#endregion Function | filter_report
