# pickle_loader
Thiese are to handle [M3GNet](https://figshare.com/articles/dataset/MPF_2021_2_8/19470599) dataset files.

The "pkl_to_extxyz.py" file extracts data from the pickle file and saves it in extxyz file format, with the following keys;
- structure
- energy
- force
- stress

The "sample_debug.py" file extracts 100 materials (100 dictionary) from each pickle file to confirm debugging code (pkl_to_extxyz_test.py).
The sample number and output file name are optional.

## dependency
