import win32com.client
import pandas as pd

sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)

directory = r'C:\Users\Joel Neumann\OneDrive\Dokumente\Kamera\3\Images'
ns = sh.NameSpace(directory)

columns = []
colnum = 0
item_count = 0

while True:
    colname = ns.GetDetailsOf(None, colnum)
    if not colname:
        break
    columns.append(colname)
    colnum += 1

file_path = 'data.txt'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(','.join(columns) + '\n')

    for item in ns.Items():
        item_details = [item.Path]
        for colnum in range(len(columns)):
            colval = ns.GetDetailsOf(item, colnum)
            item_details.append(colval)
        file.write(','.join(item_details) + '\n')
    
        item_count += 1
        print(f"Verarbeitet: {item_count} Elemente")

print("Fertig! Alle Daten wurden verarbeitet.")

"""
file_path = 'data.txt'
data = pd.read_csv(file_path, usecols=[1, 5], delimiter=',', encoding='utf-8', header=None)

data.columns = ['ImageName', 'Date and time']

# Laden der Daten mit Pandas
data = pd.read_csv(file_path, delimiter=',', encoding='utf-8', header=None)
data.columns = columns  # Verwenden der zuvor gesammelten Spaltennamen

# Angenommen, die Image-Namen sind in der ersten Spalte (Index 0) nach Ihrem Code
filtered_data = data[data[columns[0]].str.contains('IMG')]

# Ausgeben der gefilterten Daten
print(filtered_data)

value_file = 'value.txt'
# Speichern der gefilterten Daten in 'value.txt', ohne Index, mit UTF-8 Kodierung
filtered_data.to_csv(value_file, index=False, encoding='utf-8')
"""