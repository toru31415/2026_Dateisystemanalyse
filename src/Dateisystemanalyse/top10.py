#region Description
# --------------------------------------------------------------------------
# Sortiert die Dateien absteigend nach der grösse und nimmt die 10 grössten.
# --------------------------------------------------------------------------
#endregion Description


#region Function | top_10_dateien
def top_10_dateien(datenliste):
    sortiert = sorted(datenliste, key=lambda d: d["bytes"], reverse=True)                   # Nimmt die Datenliste und sortiert die ganze Liste nach Bytes absteigend.
    return sortiert[:10]                                                                    # Gibt die 10 ersten Einträge aus der Variable "sortiert" zurück.
#endregion Function | top_10_dateien
