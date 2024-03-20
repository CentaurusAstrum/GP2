# Image Analysis with Hough Transformation

This repository contains tools and data for analyzing images with a focus on detecting spherical structures using the Hough Transformation. The repository is structured into two main directories: `data` and `src`.

## Directory Structure

### `data`

This directory hosts two types of files:

- **data.txt:** These are the original informations of the images that serve as the input for the analysis. They contain various objects, among which spherical structures are to be detected.
- **Ergebnisv1.txt:** After processing the raw images with the tools found in the `src` directory, the results are stored here. This includes metadata about detected spheres, such as their coordinates, sizes, and other relevant attributes.

### `src`

Contains the source code for image analysis. The scripts are designed to apply the Hough Transformation to the provided images in order to detect and analyze spherical structures. These scripts are capable of processing the raw data found in the `data` directory and outputting their findings in a structured format for further analysis or visualization.

## Getting Started

To use the tools provided in this repository, please ensure you have a Python environment set up with the necessary libraries installed. The primary dependencies include:

- OpenCV
- NumPy
- Matplotlib (for visualization purposes)
- scikit-image

You can install these dependencies by running:

```bash
pip install opencv-python numpy matplotlib scikit-image

