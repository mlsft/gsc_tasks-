# DarkMatter-Lensing
Using PyAutoLens to simulate dark matters and learn their representation.

## Requirements

- numpy
- jupyterlab
- matplotlib
- shutil
- torch
- torchvision
- autolens>=0.40.0

*Upgrade wheels to the latest version is recommended!*

## Usage

Following the following steps before starting your notebooks. 

1. PiPy installation: `pip install -r requirements.txt`  (*conda avaliable too*).
2. `export PYTHONPATH=/path/to/autolens_workspace/` *(absolute path here, use `pwd` to view your current path).*
3. `export WORKSPACE=/path/to/autolens_workspace/` *(absolute path here, use `pwd` to view your current path).*
4. Download lensing dataset from https://drive.google.com/file/d/1IhgY91XCXz1QF5GoZow8Hu-YvzWbPZP6/view?usp=sharing .
5. Unzip the `tar.gz` formatted dataset and move `user/Downloads/lenses` folder to the `DarkMatter-Lensing/data` folder.
6. Delete the contents in `lenses_train` and `lenses_valid` if you want to re-shuffle the whole dataset.
7. Restart and clear outputs of `*.ipynb`.
8. Optional: Remove the contents in `data` folder if you do not expect to push the dataset to GitHub (*I push it for convenience*).

## Contents

- Linearly dense dark matter simulation with [PyAutoLens](https://github.com/Jammy2211/PyAutoLens).
- Dark matter representation by convolutional neural network.