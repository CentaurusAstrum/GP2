import os
import numpy as np
import rawpy
import imageio
from time import time, sleep
import threading

input_directory = 'cr3_images'
output_directory = 'png_images'
stop_flag = False

def check_for_stop():
    global stop_flag
    input("Drücken Sie Enter, um den Prozess zu beenden...\n\n")
    stop_flag = True

def convert_cr3_to_png(input_dir, output_dir):
    global stop_flag
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Output directory '{output_dir}' created.")
    else:
        print(f"Output directory '{output_dir}' already exists.")

    files_processed = set()
    
    while not stop_flag:
        deltas = []
        counter = 0
        
        for root, dirs, files in os.walk(input_dir):
            cr3_files = [file for file in files if file.lower().endswith('.cr3') and file not in files_processed]
            total_files = len(cr3_files)
            
            for file in cr3_files:
                if stop_flag:
                    break
                start_time = time()
                raw_path = os.path.join(root, file)
                files_processed.add(file)  # Markiere Datei als verarbeitet
                relative_path = os.path.relpath(raw_path, input_dir)
                output_path = os.path.splitext(relative_path)[0] + '.png'
                image_path = os.path.join(output_dir, output_path)
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                
                print(f"Opening and converting '{raw_path}'...")
                with rawpy.imread(raw_path) as raw:
                    rgb = raw.postprocess()
                    imageio.imsave(image_path, rgb)

                delta = time() - start_time
                deltas.append(delta)
                counter += 1
                mean_delta = np.mean(deltas)
                files_left = total_files - counter
                estimated_time = mean_delta * files_left

                if estimated_time > 60:
                    estimated_time /= 60
                    estimated_time_unit = "minutes"
                else:
                    estimated_time_unit = "seconds"

                if delta > 60:
                    delta /= 60
                    delta_unit = "minutes"
                else:
                    delta_unit = "seconds"

                print(f'Converted files: {counter}/{total_files}\n'
                      f'Files left: {files_left}\n'
                      f'Last file conversion time: {delta:.2f} {delta_unit}\n'
                      f'Estimated time left: {estimated_time:.2f} {estimated_time_unit}')
                print('_'*50)
                print()

        if not cr3_files:
            print("Warte auf neue Dateien...")
            sleep(10)  # Wartezeit bis zur nächsten Überprüfung

    print(f'The converted images are in the folder: {output_directory}')

# Startet den Thread zur Überwachung der Beendigung
stop_thread = threading.Thread(target=check_for_stop)
stop_thread.start()

convert_cr3_to_png(input_directory, output_directory)

stop_thread.join()
