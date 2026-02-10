#  2026 Semesterarbeit - LAP
## Dateisystemanalyse in Python
Diese Datgeisystemanalyse in Python ist ein konsolenbasiertes Python-Tool, das einen frei wählbaren Ordner    rekursiv scannt und einen übersichtlichen Report ausgibt inkl den 10 grössten Dateien. Anschliessend kann optional nach Dateinamen/Dateiendungen gefiltert und gezielt aufgeräumt werden (aufgeräumte Daten werden gelöscht). Vor dem löschen geschieht ein dry-run mit doppelter bestätigung bevor die markierten Daten gelöscht.

## Funktionen und Features

- **Pfad scannen (rekursiv)**: Unterordner und Dateien werden erfasst
- **Report in der Konsole**:
  - Anzahl Dateien / Ordner
  - Gesamtgrösse des Scanbereichs
- **Top-10 grösste Dateien**
- **Filter/Suche**:
  - Dateiname enthält...
  - Dateiendungen (z. B. `.jpg,.png,.pdf`)
- **Bereinigung (Löschen)**:
  - Auswahl aus Trefferliste (falls vorhanden), sonst aus Top-Liste
  - **Dry-Run** (zeigt nur, was gelöscht würde)
  - Optionales endgültiges Löschen mit **doppelter Bestätigung** (`Ja/Nein` + `DELETE`)
- Optional: **Report-Export** als `.txt` oder `.json` in `./reports`

---

## Ablauf

1. Programm starten und Pfad eingeben.  
2. Scan läuft und gibt einen Report aus (Übersicht + Top-Liste)  
3. Abfrage: **Filtern/Suchen?** → Ergebnisse werden angezeigt  
4. Abfrage: **Dateien löschen?** (Trefferliste, sonst Top-Liste)  
   - Auswahl der Dateien
   - Dry-Run (nur als Vorschau)
   - wirklich löschen (doppelte Bestätigung)