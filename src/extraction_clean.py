import pandas as pd

file_path = 'data/raw_data.txt'
data = pd.read_csv(file_path, usecols=[1, 5], delimiter=',', encoding='utf-8', header=None)

data.columns = ['ImageName', 'Date and time']

filtered_data = data[data['ImageName'].str.contains('IMG')]

valuefile = 'data/main_data.txt'
filtered_data.to_csv(valuefile, index=False, header=True)
print(f'done! The file {valuefile} was created.')