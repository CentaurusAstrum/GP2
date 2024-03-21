import win32com.client
import pandas as pd

# Erstelle eine Set, um die Pfade der bereits verarbeiteten Elemente zu speichern
verarbeitete_pfade = set()

file_path = 'data/raw_data.txt'

# Versuche, die vorhandene Datei zu lesen und speichere die Pfade der verarbeiteten Elemente
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            verarbeitete_pfade.add(line.split(',')[0])  # Nehme an, dass der Pfad die erste Spalte ist
except FileNotFoundError:
    print("Ausgabedatei existiert noch nicht. Eine neue wird erstellt.")

sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
directory = 'C:\\Users\\Joel Neumann\\OneDrive\\Dokumente\\Kamera\\Auswertung neue Bilder\\cr3_images'
ns = sh.NameSpace(directory)

columns = []
colnum = 0
item_count = 0

# Spaltennamen erfassen
while True:
    colname = ns.GetDetailsOf(None, colnum)
    if not colname:
        break
    columns.append(colname)
    colnum += 1

# Elemente verarbeiten
with open(file_path, 'a', encoding='utf-8') as file:
    if not verarbeitete_pfade: 
        file.write(','.join(columns) + '\n')
    
    for item in ns.Items():
        if item.Path not in verarbeitete_pfade:  # Überprüfe, ob das Element schon verarbeitet wurde
            item_details = [item.Path]
            for colnum in range(len(columns)):
                colval = ns.GetDetailsOf(item, colnum)
                item_details.append(colval)
            file.write(','.join(item_details) + '\n')
    
            item_count += 1
            print(f"Verarbeitet: {item_count} Elemente")
        else:
            print(f"Übersprungen (bereits verarbeitet): {item.Path}")

print(f"Fertig! Alle neuen Daten wurden verarbeitet.")
