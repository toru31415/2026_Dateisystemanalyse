#region Description
# --------------------------------------------------------------------
# Das Testing wird mit dem AAA-Prinzip durchgeführt
# --------------------------------------------------------------------
#endregion Description


#region Import
import builtins
import pytest
import Filter
#endregion Import


#region Function | testdatensatz_erstellen -> Test Liste erstellen
def testdatensatz_erstellen():                                                                                                      # Funktion um einen Testdatensatz zu erstellen
    return [
        {"dateiname": "Readme.TXT", "dateiendung": ".txt"},
        {"dateiname": "image.jpg", "dateiendung": ".jpg"},
        {"dateiname": "report.PDF", "dateiendung": ".pdf"},
        {"dateiname": "another.JPG", "dateiendung": ".jpg"},
    ]
#endregion Function | testdatensatz_erstellen


#region Testing | test_dateifilter_ohne_filterung -> Test vom Filtern, aber es wird nach nichts gefilter. Der Testdatensatz ist somit vorher und nachher der Selbe
def test_dateifilter_ohne_filterung():
    # Arrange - Daten vorbereiten
    daten = testdatensatz_erstellen()                                                                                               # Daten Variable mit den Testdaten aus Testdatensatz_erstellen befüllen
    
    # Act - Funktion ausführen
    resultat = Filter.dateifilter(daten, name_text="", endung_text="")                                                              # Filter Funktion ausführen und nach nichts filtern
    
    # Assert - Ergebnis prüfen
    assert resultat == daten                                                                                                        # Kontrolle, ob die Eingabe nach dem Filtern noch gleich ist und somit nicht verloren geht
#endregion Testing | test_dateifilter_ohne_filterung

#region Testing | test_dateifilter_nur_dateiname -> Test vom Filtern, wo nur nach einem bestimmten Dateinamen gesucht wird
def test_dateifilter_name_nur_dateiname():
    # Arrange - Daten vorbereiten
    daten = testdatensatz_erstellen()                                                                                               # Daten Variable mit den Testdaten aus Testdatensatz_erstellen befüllen

    # Act - Funktion ausführen
    resultat = Filter.dateifilter(daten, name_text="readme", endung_text="")                                                        # Filter Funktion ausführen und nur nach Dateien mit dem namen "readme" filtern

    # Assert - Ergebnis prüfen
    assert len(resultat) == 1                                                                                                       # Kontrolle, ob nur ein Resultat besteht
    assert resultat[0]["dateiname"] == "Readme.TXT"                                                                                 # Kontrolle, ob an erster Stelle [0] der Eintrag Readme.TXT steht
#endregion Testing | test_dateifilter_nur_dateiname

#region Testing | test_dateifilter_eingabe_bereinigung -> Test vom Filtern, ob dieser Punkt oder Leerschlag Symbole berinigt
def test_dateifilter_extension_filter_eingabe_bereinigung():
    # Arrange - Daten vorbereiten
    daten = testdatensatz_erstellen()                                                                                               # Daten Variable mit den Testdaten aus Testdatensatz_erstellen befüllen
    
    # Act - Funktion ausführen
    resultat = Filter.dateifilter(daten, name_text="", endung_text="jpg, PDF , .txt")                                               # Filter Funktion ausführen und nach endungen filtern, die Eingabe enthält aber noch leerschläge und punkte
    
    # Assert - Ergebnis prüfen
    assert len(resultat) == 4                                                                                                       # Kontrolle, ob vier Resultate nach dem Filtern bestehen bleiben
    assert any(e["dateiendung"].lower() == ".pdf" for e in resultat)                                                                # Kontrolle, ob .pdf in der Liste gefunden wurde
#endregion Testing | test_dateifilter_eingabe_bereinigung

#region Testing | test_dateifilter_dateiname_und_endung -> Test vom Filtern, wo nach Name und Endung der Datei gefilter wird
def test_dateifilter_dateiname_und_endung():
    # Arrange - Daten vorbereiten
    daten = testdatensatz_erstellen()                                                                                               # Daten Variable mit den Testdaten aus Testdatensatz_erstellen befüllen
    
    # Act - Funktion ausführen
    resultat = Filter.dateifilter(daten, name_text="image", endung_text=".jpg")                                                     # Filter Funktion ausführen und nach Datei Image und Endung jpg filtern

    # Assert - Ergebnis prüfen
    assert len(resultat) == 1                                                                                                       # Kontrolle, ob nur ein Resultat besteht
    assert resultat[0]["dateiname"] == "image.jpg"                                                                                  # Kontrolle, ob der Dateiname image.jpg ist
#endregion Testing | test_dateifilter_dateiname_und_endung

#region Testing | test_dateifilter_tabelle_formatieren
def test_dateifilter_tabelle_formatieren(monkeypatch):                                                                      # https://docs.pytest.org/en/stable/how-to/monkeypatch.html
    # Arrange - Daten vorbereiten
    beispiel = [{"dateiname": "a"}]                                                                                                 # Variable Beispiel mit der Datei a als Name erstellen
    monkeypatch.setattr(Filter, "tabelle_formatieren", lambda lst: ["wert1", "wert2"])                                              # Mit Hilfe von monkeypatch die tabelle_formatieren verändern
    
    # Act - Funktion ausführen
    rueckmeldung = Filter.filter_report(beispiel)                                                                                   # filter_report mit beispiel Daten starten und diese in die Variable rueckmeldung schreiben

    # Assert - Ergebnis prüfen
    assert rueckmeldung == "wert1\nwert2"                                                                                           # rueckmeldung prüfen, ob wert1 und wert2 darin zu finden sind
#endregion Testing | test_dateifilter_tabelle_formatieren

#region Testing | test_filter_und_suche_ohne_filter
def test_filter_und_suche_ohne_filter(monkeypatch, capsys):
    # Arrange - Daten vorbereiten
    monkeypatch.setattr(Filter, "frage", lambda prompt: False)                                                                      # Mit Hilfe von monkeypatch die frage mit False beantworten

    # Act - Funktion ausführen
    resultat = Filter.filter_und_suche({"dateien": testdatensatz_erstellen()})                                                      # filter_und_suchen starten ohen eingabe

    # Assert - Ergebnis prüfen
    assert resultat == []                                                                                                           # Kontrolle, ob die resultat leer ist
    rueckmeldung = capsys.readouterr()                                                                                              # Rückmeldung ins rueckmeldung schreiben
    assert "Filter und Suche" in rueckmeldung.out                                                                                   # Kontrolle, ob in rueckmeldung der Titel "Filter und Suche" zu finden ist
#endregion Testing | test_filter_und_suche_ohne_filter

#region Testing | test_filter_und_suche_mit_resultat
def test_filter_und_suche_mit_resultat(monkeypatch, capsys):
    inputs = iter(["image", ".jpg"])                                                                                                # input vorbereiten, dass nach image und jpgs gesucht werden soll
    monkeypatch.setattr(Filter, "frage", lambda prompt: True)                                                                       # Mit Hilfe von monkeypatch frage zum Filtern bestätigen
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))                                                          # Mit Hilfe von monkeypatch die Angaben aus Input zum Filtern übergeben
    monkeypatch.setattr(Filter, "tabelle_formatieren", lambda lst: [f"FOUND: {e['dateiname']}" for e in lst])                       # Mit Hilfe von monkeypatch das tabellen_formatieren beeinflussen
    scan_ergebnis = {"dateien": testdatensatz_erstellen()}                                                                          # Scan Ergebnis vorbereiten, welches an die Funktion übergeben wird

    # Act - Funktion ausführen
    resultat = Filter.filter_und_suche(scan_ergebnis)                                                                               # Funktion filtern_und_suche starten, mit den defineirten Scan Ergebnissen

    # Assert - Ergebnis prüfen
    assert any(e["dateiname"] == "image.jpg" for e in resultat)                                                                     # Kontrolle, ob image.jpg in den Resultaten zu finden ist
    rueckmeldung = capsys.readouterr()                                                                                              # Rückmeldung aus Skript in rueckmeldung schreiben
    assert "Trefferliste" in rueckmeldung.out                                                                                       # Kontrolle, ob in der rueckmeldung "Trefferliste" zu finden ist. Damit man sicher die richtige funktion testet
    assert "FOUND: image.jpg" in rueckmeldung.out                                                                                   # Kontrolle, ob in der rueckmeldung "FOUND: image.jpg" zu finden ist. Damit man sicher die richtige funktion testet
#endregion Testing | test_filter_und_suche_mit_resultat