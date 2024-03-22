import os
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter
from scipy.optimize import curve_fit

program_start = perf_counter()

input_folder_image = "originalbilder"
input_file = "kugelmitte.txt"
output_file = "hohe_px.txt"
output_folder1 = "height_px"
output_folder2 = "height_brightness_plot"

tol = 0.3  # Bestimmt den threshhold für "dunkelheit" am unteren Bildrand

image_files = os.listdir(input_folder_image)

cx = np.loadtxt(input_file, skiprows=1, usecols=1)
cy = np.loadtxt(input_file, skiprows=1, usecols=2)
rad = np.loadtxt(input_file, skiprows=1, usecols=3)

if not os.path.exists(output_folder1):
    os.mkdir(output_folder1)

if not os.path.exists(output_folder2):
    os.mkdir(output_folder2)

iteration = 0
with open(output_file, "w") as f:
    f.write("Name:        h:   edge:     d_edge:\n")

for i, file_name in enumerate(image_files):
    iteration += 1
    time_iteration = perf_counter()
    print(f'Processing {file_name}, {iteration}/{len(image_files)}...')
    image = np.mean(plt.imread(f"{input_folder_image}/{file_name}"), -1)
    x = int(cx[i])
    y = int(cy[i])
    r = int(rad[i])

    bottom_index = image.shape[0] - 1

    edge = bottom_index  # Laufindex
    while image[edge, x] < tol:  # falls Pixel "dunkel", Kante eins weiter oben
        edge -= 1

    h = edge - y - r

    #Speichert Bild der Kante
    plt.imshow(image[edge-100:bottom_index,x-300:x+300], cmap="Greys_r")
    plt.title(f'{file_name}, {h}')
    plt.axhline(y=100)
    plt.savefig(f'{output_folder1}/{file_name}')  # [bottomIndex:edge+100,x-100:x+100]
    # plt.show()
    plt.close()
    # try:
    #Berechnet Fehler
    width = -1
    
    image = image[edge-200:bottom_index,x-r:x+r]

    mean = np.mean(image, 1)

    lower_mean = np.mean(mean[200:])
    upper_mean = np.mean(mean[:200])

    #Linear Fit
    upper_side = mean[:200-20]
    lower_side = mean[200+20:]

    def linear(x,a,b):
        y = a*x + b
        return y

    t_complete = np.linspace(0,len(mean), len(mean))
    #Left fit
    t_upper = t_complete[:200-20]
    popt, pcov = curve_fit(linear, xdata=t_upper, ydata=upper_side)

    upper_fit = linear(t_complete, popt[0], popt[1])

    #Right fit
    t_lower = t_complete[200+20:]
    popt, pcov = curve_fit(linear, xdata=t_lower, ydata=lower_side)

    lower_fit = linear(t_complete, popt[0], popt[1])


    upper_bound = np.argwhere(np.abs(upper_fit - mean) <= 0.01)[-1]
    lower_bound = np.argwhere(np.abs(lower_fit - mean) <= 0.01)[0]

    width = (lower_bound-upper_bound)[0]

    #Speichert Helligkeitsplot
    plt.plot(t_complete, mean)
    plt.plot(t_complete, upper_fit)
    plt.plot(t_complete, lower_fit)
    plt.title(f"{file_name}, d_edge={width}")
    plt.xlabel("y px")
    plt.ylabel("Mittlere Helligkeit")
    # plt.axvline(x=upper_bound)
    # plt.axvline(x=lower_bound)
    plt.savefig(f'{output_folder2}/{file_name}')  # [bottomIndex:edge+100,x-100:x+100]
    # plt.show()
    plt.close()

# except: 
#     print(f"Error with Fehlerberechnung of {file_name}, put down d_edge as -1")

    with open(output_file, "a") as f:
        f.write(f'{file_name} {h} {edge} {width} \n')

    print(f'Processing of {file_name} finished after {perf_counter() - time_iteration} seconds.')

