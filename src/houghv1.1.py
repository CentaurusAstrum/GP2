import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as im
from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks
from time import perf_counter, time


# PARAMETER vorher festzulegen
# Das Programm sollte zusammen mit dem ORDNER mit den Bildern
# (path unter image_folder_path abspeichern) in einem Ordner liegen
# low und high sollten für jede Messreihe neu gewählt werden (in exktra Programm),
# Kantenbild anzeigen lassen und so kalibrieren
# potential_radii ist ein array mit potentiellen Radien für die Kugel in Pixeln
# Die Datei Kugel.txt sollte im selben Ordner wie das Programm liegen
input_folder = "originalbilder"
output_file_name = "kugelmitte.txt"
low = 0.5
high = 0.6
r_min = 240
r_max = 260
potential_radii = np.linspace(r_min, r_max, 11)

image_files = sorted(os.listdir(input_folder))  # Ensure the files are sorted
#start_index = image_files.index('IMG_5201.png')  # Find the index of the starting file
#image_files = image_files[start_index:]  # Adjust the list to start from the found index
delta_times = []
counter = 0

with open(output_file_name, "w") as f:
    f.write('Name: x: y: r: rmin: rmax: \n')

for file_name in image_files:
    start_time = time()
    print(f'Reading file {file_name}...')
    image = plt.imread(f'{input_folder}/{file_name}')
    print('Done.')
    
    # Your existing code for processing each file goes here.

    # Greyscale
    grey = np.mean(image, -1)

    # Kantenbild
    print(f'Calculating Edges...')
    edges = canny(grey, low_threshold=low, high_threshold=high)

    # Hough
    print('Performing Hough Transform...')
    hough = hough_circle(edges, potential_radii)
    # Speichert Eigenschaften des besten Kreis fits
    accums, cx, cy, r = hough_circle_peaks(hough, potential_radii, total_num_peaks=1)
    # Finde index des besten Kreises (r etc. ist ein Array)

    index = np.argwhere(potential_radii == r[0])
    end_time = time()
    delta = end_time - start_time
    delta_times.append(delta)
    counter += 1
    time_left = np.mean(delta_times) * (len(image_files) - counter)
    if time_left > 60:
        if delta > 60:
            print(f'Done: {counter}, after: {delta / 60:.2f} minutes \nleft: {len(image_files) - counter} \nestimated time left: {time_left / 60:.2f} minutes.')
        else:
            print(f'Done: {counter}, after: {delta:.2f} seconds \nleft: {len(image_files) - counter} \nestimated time left: {time_left / 60:.2f} minutes.')
    else:
        print(f'Done: {counter} \nleft: {len(image_files) - counter} \nestimated time left: {time_left:.2f} seconds.')

        
    print('Saving Results...')
    im.imsave(f'hough/{file_name}', arr=hough[index][0, 0])

    with open(output_file_name, "a") as f:
        f.write(f'{file_name} {cx[0]} {cy[0]} {r[0]} {r_min} {r_max} \n')


