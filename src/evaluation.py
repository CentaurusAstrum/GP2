import win32com.client
import pandas as pd

sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)

directory = './path/to/directory'
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

print(f"Fertig! Alle Daten wurden verarbeitet.")


import pandas as pd

file_path = 'data.txt'
data = pd.read_csv(file_path, usecols=[1, 5], delimiter=',', encoding='utf-8', header=None)

data.columns = ['ImageName', 'Date and time']

filtered_data = data[data['ImageName'].str.contains('IMG')]

valuefile = 'value.txt'
filtered_data.to_csv(valuefile, index=False, header=True)
print(len(filtered_data))