#region Description
# --------------------------------------------------------------------
# Das Testing wird mit dem AAA-Prinzip durchgeführt
# --------------------------------------------------------------------
#endregion Description


#region Import
import builtins
from pathlib import Path
import Cleanup
#endregion Import

#region Testing | test_cleanup_dateien_loeschen
def test_cleanup_dateien_loeschen(tmp_path):
    # Arrange - Daten vorbereiten
    f1 = tmp_path / "a.txt"                                                                                                     # Variable f1 im tmp_path definieren, mit a.txt als Datei
    f2 = tmp_path / "b.txt"                                                                                                     # Variable f1 im tmp_path definieren, mit b.txt als Datei
    f1.write_text("bingo")                                                                                                      # Datei a.txt erstellen, mit dem Inhalt "bingo"
    f2.write_text("bongo")                                                                                                      # Datei b.txt erstellen, mit dem Inhalt "bongo"

    auswahl = [                                                                                                                 # Auswahl Liste für zum Löschen erstellen
        {"abspfad": str(f1), "relpfad": "a.txt"},
        {"abspfad": str(f2), "relpfad": "b.txt"},
    ]

    # Act - Funktion ausführen
    status = Cleanup.dateien_löschen(auswahl)                                                                                   # Funktion Dateien_löschen mit der vorbereiteten Auswahl starten und dies ins status schreiben

    # Assert - Ergebnis prüfen
    assert status["gelöscht"] == 2                                                                                              # Kontrolle, ob beide Dateien gelöscht werden konnten
    assert status["fehlgeschlagen"] == 0                                                                                        # Kontrolle, ob keine Fehler beim Löschen auftreten
    assert f1.exists() is False                                                                                                 # Kontrolle, ob die Datei a.txt noch vorhanden ist
    assert f2.exists() is False                                                                                                 # Kontrolle, ob die Datei b.txt noch vorhanden ist
#endregion Testing | test_cleanup_dateien_loeschen

#region Testing | test_cleanup_dateien_loeschen_mit_fehlern
def test_cleanup_dateien_loeschen_mit_fehlern(tmp_path):
    # Arrange - Daten vorbereiten
    f1 = tmp_path / "ist_vorhanden.txt"                                                                                         # Variable f1 im tmp_path definieren, mit ist_vorhanden.txt als Datei
    f1.write_text("wichtige daten")                                                                                             # Datei ist_vorhanden.txt erstellen, mit dem Inhalt "wichtige daten"
    vermisst = tmp_path / "nicht_vorhanden.txt"                                                                                 # Variable vermisst im tmp_path definieren, mit nicht_vorhanden.txt als Datei

    auswahl = [                                                                                                                 # Auswahl Liste für zum Löschen erstellen
        {"abspfad": str(f1), "relpfad": "ist_vorhanden.txt"},
        {"abspfad": str(vermisst), "relpfad": "nicht_vorhanden.txt"},
    ]

    # Act - Funktion ausführen
    status = Cleanup.dateien_löschen(auswahl)                                                                                   # Funktion Dateien_löschen mit der vorbereiteten Auswahl starten und dies ins status schreiben

    # Assert - Ergebnis prüfen
    assert status["gelöscht"] == 1                                                                                              # Kontrolle, ob eine Datei gelöscht wurde
    assert status["fehlgeschlagen"] == 1                                                                                        # Kontrolle, ob eine Datei auf einen Fehler gelaufen ist
    assert any("nicht_vorhanden.txt" in m for m in status["meldungen"])                                                         # Kontrolle, ob die nicht_vorhanden.txt unter den Meldungen zu finden ist
#endregion Testing | test_cleanup_dateien_loeschen_mit_fehlern

#region Testing | test_cleanup_testlauf_anzeigen_ohne_eingabe
def test_cleanup_testlauf_anzeigen_ohne_eingabe(capsys):
    # Arrange - Daten vorbereiten
    # Keine Daten zum vorbereiten, da man keinen Input übergibt

    # Act - Funktion ausführen
    Cleanup.testlauf_anzeigen([])                                                                                               # Funktion testlauf_anzeigen starten, ohne parameter

    # Assert - Ergebnis prüfen
    rueckmeldung = capsys.readouterr().out                                                                                      # Fehlermeldung in die Variable rueckmeldung schreiben
    assert "TESTLAUF" in rueckmeldung                                                                                           # Kontrolle, dass man im Testlauf ist
    assert "(Keine Dateien ausgewählt)" in rueckmeldung                                                                         # Kontrolle, dass man in den Fehler Keine Dateien ausgewählt läuft
#endregion Testing | test_cleanup_testlauf_anzeigen_ohne_eingabe

#region Testing | test_cleanup_testlauf_anzeigen_tabelle_formatieren -> Testen, dass das tabellen_formatieren in der Testlauf_anzeigen korrekt abläuft
def test_cleanup_testlauf_anzeigen_tabelle_formatieren(monkeypatch, capsys):
    # Arrange - Daten vorbereiten
    monkeypatch.setattr(Cleanup, "tabelle_formatieren", lambda lst: ["Wert1", "Wert2"])                                         # Mit Hilfe von monkeypatch die tabelle_formatieren funktion verändern, damit man den Wert1 und Wert2 übergeben kann

    # Act - Funktion ausführen
    Cleanup.testlauf_anzeigen([{"relpfad": "x"}])                                                                               # Funktion testlauf_anzeigen starten

    # Assert - Ergebnis prüfen
    rueckmeldung = capsys.readouterr().out                                                                                      # Rückmeldung aus der Auführung in die Variable rueckmeldung schreiben
    assert "Wert1" in rueckmeldung                                                                                              # Kontrolle, ob Wert1 in der rueckmeldung erwähnt wurde
    assert "Wert2" in rueckmeldung                                                                                              # Kontrolle, ob Wert2 in der rueckmeldung erwähnt wurde
#endregion Testing | test_cleanup_testlauf_anzeigen_tabelle_formatieren

#region Testing | test_cleanup_loeschvorgang_starten_ohne_eingabe
def test_cleanup_loeschvorgang_starten_ohne_eingabe(monkeypatch, capsys):
    # Arrange - Daten vorbereiten
    monkeypatch.setattr(Cleanup, "tabelle_formatieren", lambda lst: ["1 - a", "2 - b"])                                         # Mit Hilfe von monkeypatch die tabellen_formatieren eingabe verändern
    monkeypatch.setattr(builtins, "input", lambda prompt="": "")                                                                # Mit Hilfe von monkeypatch den Input auf Enter also abbrechen ändern

    quelle = [{"relpfad": "a", "abspfad": "/tmp/a"}]                                                                            # Variable quelle vorbereiten, diese wird später als input in die Funktion übergeben

    # Act - Funktion ausführen
    Cleanup.löschvorgang_starten(quelle)                                                                                        # Funktion löschvorgang_starten mit den parametern aus quelle starten

    # Assert - Ergebnis prüfen
    rueckmeldung = capsys.readouterr().out                                                                                      # Rückmeldung aus der Ausführung in die Variable rueckmeldung schreiben
    assert "abgebrochen" in rueckmeldung                                                                                        # Kontrolle, ob die Rückmeldung "abgebrochen" enthält
#endregion Testing | test_cleanup_loeschvorgang_starten_ohne_eingabe

#region Testing | test_cleanup_loeschvorgang_starten_fake_dateien_loeschen
def test_cleanup_loeschvorgang_starten_fake_dateien_loeschen(monkeypatch, capsys):
    # Arrange - Daten vorbereiten
    monkeypatch.setattr(Cleanup, "tabelle_formatieren", lambda lst: ["1: a"])                                                   # Mit Hilfe von monkeypatch die tabellen_formatieren eingabe verändern.
    monkeypatch.setattr(builtins, "input", lambda prompt="": "1")                                                               # Mit Hilfe von monkeypatch die input eingabe verändern, damit bestätigt wird
    monkeypatch.setattr(Cleanup, "frage", lambda prompt: True)                                                                  # Mit Hilfe von monkeypatch die frage eingabe verändern, damit bestätigt wird

    called = {}                                                                                                                 
    def fake_dateien_löschen(auswahl):                                                                                          # Funktion um die Dateien vermeintlich also fake zu löschen
        called['args'] = auswahl
        return {"gelöscht": 1, "fehlgeschlagen": 0, "meldungen": []}

    monkeypatch.setattr(Cleanup, "dateien_löschen", fake_dateien_löschen)                                                       # Mit Hilfe von monkeypatch die den Aufruf von dateien_löschen mit fake_dateien_löschen zu ersetzen

    quelle = [{"relpfad": "a.txt", "abspfad": str(Path.cwd() / "a.txt")}]                                                       # Variable definieren mit den Parametern, was gelöscht werden soll

    # Act - Funktion ausführen
    Cleanup.löschvorgang_starten(quelle)                                                                                        # Funktion löschvorgang_starten mit den parametern aus quelle starten

    # Assert - Ergebnis prüfen
    rueckmeldung = capsys.readouterr().out                                                                                      # Rückmeldung aus der Ausführung in die Variable rueckmeldung schreiben
    assert "Gelöscht:" in rueckmeldung                                                                                          # Kontrolle, ob Gelöscht in der Rückmeldung erwähnt wird
    assert called.get('args') is not None                                                                                       # Kontrolle, dass called nicht mehr leer also none ist
    assert isinstance(called['args'], list)                                                                                     # Kontrolle, ob die args im dict "called" eine liste sind
#endregion Testing | test_cleanup_loeschvorgang_starten_fake_dateien_loeschen