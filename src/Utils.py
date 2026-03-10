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