#region Description
# --------------------------------------------------------------------
# Das Testing wird mit dem AAA-Prinzip durchgeführt
# --------------------------------------------------------------------
#endregion Description


#region Import
import pytest
from pathlib import Path
from Scan import scan_ordner
#endregion Import


#region Function | erstelle_testdatei -> Test Datei erstellen
def erstelle_testdatei(path: Path, size: int):                                                                              # Erlaubt das erstellen von Testdateien. Dies mit dem Input vom Namen der zu erstellenden Datei und der Zielgrösse
    path.write_bytes(b'a' * size)                                                                                           # Datei schreiben, bis die definierte grösse erreicht wurde
#endregion Function | erstelle_testdatei


#region Testing | test_scan_resultat -> Test mit zwei Dateien und einem Unterordner, ob der Scan richtig ausgeführt wird
def test_scan_resultat(tmp_path):                                                                                           # https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html
    # Arrange - Daten vorbereiten
    sub = tmp_path / "subdir"                                                                                               # Ordner subdir im tmp_path definieren
    sub.mkdir()                                                                                                             # Ordner subdir im tmp_path erstellen
    f1 = sub / "file1.txt"                                                                                                  # Datei "file1.txt" im Unterordner sub definieren
    f2 = tmp_path / "file2.bin"                                                                                             # Datei "file2.bin" im rootordner definieren

    erstelle_testdatei(f1, 100)                                                                                             # Datei "file1.txt" erstellen
    erstelle_testdatei(f2, 200)                                                                                             # Datei "file2.bin" erstellen

    # Act - Funktion ausführen
    resultat = scan_ordner(tmp_path)                                                                                        # Scan starten, mit den Testdateien

    # Assert - Ergebnis prüfen
    # -> Assert | Resultat Zusammenfassung mit erwarteten werten kontrollieren
    assert resultat["anzahl_dateien"] == 2                                                                                  # Kontrolle, ob es zwei Dateien gescannt hat
    assert resultat["anzahl_ordner"] == 1                                                                                   # Kontrolle, ob es einen Ordner gescannt hat
    assert resultat["gesamt_bytes"] == 300                                                                                  # Kontrolle, ob die gesammt grösse 300 ist. 100 + 200 = 300

    # -> Assert | relativen Pfad kontrollieren
    relpfad = [dateipfad["relpfad"] for dateipfad in resultat["dateien"]]                                                   # Relative Pfade aus dem Resultat in eine eigene Variable schreiben
    assert str(f1.relative_to(tmp_path)) in relpfad                                                                         # Kontrolle, ob die erstellt file1.txt Datei in der Rückgabe am gleichen Ort ist, wie bei der Erstelltung
    assert str(f2.relative_to(tmp_path)) in relpfad                                                                         # Kontrolle, ob die erstellt file2.bin Datei in der Rückgabe am gleichen Ort ist, wie bei der Erstelltung

    # -> Assert | Resultat der Einzelnen Dateien prüfen
    bytes_for_f1 = next(dateipfad["bytes"] for dateipfad in resultat["dateien"] if dateipfad["dateiname"] == "file1.txt")   # Informationen zur file1.txt Datei in eine Variable schreiben
    bytes_for_f2 = next(dateipfad["bytes"] for dateipfad in resultat["dateien"] if dateipfad["dateiname"] == "file2.bin")   # Informationen zur file2.bin Datei in eine Variable schreiben
    assert bytes_for_f1 == 100                                                                                              # Kontrolle, ob die file1.txt Datei 100 bytes gross ist
    assert bytes_for_f2 == 200                                                                                              # Kontrolle, ob die file2.bin Datei 200 bytes gross ist
#endregion Testing | test_scan_resultat

#region Testing | test_scan_ordnerstruktur -> Test mit zwei Dateien, ob diese im Resultat vorhanden sind
def test_scan_ordnerstruktur(tmp_path):
    # Arrange - Daten vorbereiten
    (tmp_path / "a").mkdir()                                                                                                # Ordner a im tmp_path erstellen
    verschachtelt = tmp_path / "a" / "verschachtelt.txt"                                                                    # Datei verschachtelt.txt für im Unterordner a definieren
    rootfile = tmp_path / "root.txt"                                                                                        # Datei root.txt für den root Pfad definieren
    verschachtelt.write_text("hello")                                                                                       # Datei verschachtelt.txt mit dem Inhalt "hello" befüllen und somit erstellen
    rootfile.write_text("world!")                                                                                           # Datei root.txt mit dem Inhalt "world!" befüllen und somit erstellen

    # Act - Funktion ausführen
    resultat = scan_ordner(tmp_path)                                                                                        # Scan starten, mit den Testdateien

    # Assert - Ergebnis prüfen
    assert any(entry["dateiname"] == "verschachtelt.txt" for entry in resultat["dateien"])                                  # Kontrolle, ob die verschachtelt.txt im Resultat ausgegeben wird
    assert any(entry["relpfad"].startswith("a") for entry in resultat["dateien"])                                           # Kontrolle, ob eine datei im a/ ordner zu finden ist
#endregion Testing | test_scan_ordnerstruktur
