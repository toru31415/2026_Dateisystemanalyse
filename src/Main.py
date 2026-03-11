#region Description
# --------------------------------------------------------------------
# HAUPTPROGRAMM
# Ablaufplan unseres Codes:
#1. Programm starten und Pfad eingeben.  
#2. Scan läuft und gibt einen Report aus (Übersicht + Top-Liste)  
#3. Abfrage: **Filtern/Suchen?** → Ergebnisse werden angezeigt  
#4. Abfrage: **Dateien löschen?** (Trefferliste, sonst Top-Liste)  
#   - Auswahl der Dateien
#   - Dry-Run (nur als Vorschau)
#   - wirklich löschen (doppelte Bestätigung)
# --------------------------------------------------------------------
#endregion Description


#region Import
from Scan import analyse_starten
from Filter import filter_und_suche
from Cleanup import dateien_löschen_start
#endregion Import


#region Function | hauptmenü
def hauptmenü():
    print("\n================= Dateisystemanalyse =================")
    print("┌" + "─" * 52 + "┐")
    print("│" + "Willkommen zur Dateisystemanalyse!".center(52) + "│")
    print("│" + "Scannen • Reporten • Filtern • Löschen".center(52) + "│")
    print("└" + "─" * 52 + "┘")

    treffer_liste = None
    top10 = None

    top10, scan_ergebnis = analyse_starten()
    input("\nEnter drücken, um zum Menü zurückzukehren...")
    
    while True:
        print("\n================= Dateisystemanalyse =================")
        print("\n--------------------- Hauptmenü ----------------------")
        print("1) Ordner analysieren")
        print("2) Dateien filtern / suchen")
        print("3) Dateien löschen")
        print("0) Beenden")

        try:
            eingabe = int(input("Was möchtest du machen? (0-3) "))
        except ValueError:
            print("Bitte eine Zahl eingeben!")
            continue

        match eingabe:
            case 1: 
                top10, scan_ergebnis = analyse_starten()
                input("\nEnter drücken, um zum Menü zurückzukehren...")
            case 2:
                treffer_liste = filter_und_suche(scan_ergebnis)
                input("\nEnter drücken, um zum Menü zurückzukehren...")
            case 3:
                dateien_löschen_start(top10, treffer_liste)
                input("\nEnter drücken, um zum Menü zurückzukehren...")
            case 0:
                print("================== Programm beendet ==================")
                break
#endregion Function | hauptmenü


#region Execution | hauptmenü
hauptmenü()
#endregion Execution