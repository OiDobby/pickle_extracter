# pickle_extracter  
These are to handle [M3GNet](https://figshare.com/articles/dataset/MPF_2021_2_8/19470599) dataset files.

The "pkl_to_extxyz.py" file extracts data from the pickle file and saves it in extxyz file format, with the following keys;
- structure
- energy
- force
- stress

The M3GNet data uses the units eV, eV/A, and kBa to represent energy, force, and stress.  
The `stress` in the M3GNet data is the raw output from VASP, indicating that there is negative stress according to the convention outlined in M3GNet's paper.  
In our output file (extxyz format), the unit of `stress` is converted to GPa by multiplying by -0.1 (kBa to GPa and changing sign).  

The "sample_debug.py" file extracts 100 materials (100 dictionary) from each pickle file to confirm debugging code (debug.py).  
The sample number and output file name are optional.

The "pkl_num_data.py" is not essential. This code is just utility file and it confirms the total number of atomic structure (snap shot) in data.  

The code in "for_nequip" directory extracts data for nequip 0.3.3 version.  
Some data are inappropriate for nequip, such as an excessively long distance between two atoms that exceeds r_max.  
Skiped that structures are recorded in "neighbor_list_log.txt" file.  
The code generates two files. The first (output_with_edges.extxyz) is compatible with nequip, whereas the second (output_no_edges.extxyz) is not.

## Usage
1. Install [pymatgen]([https://pytorch.org/get-started/locally/](https://pymatgen.org/installation.html)). This package is depended on
    - Python>=3.8
    - pymatgen==2023.8.10 (=!2024.8.9)
```shell
pip install pymatgen==2023.8.10
```
2. Strongly recommanded pymatgen version 2023.8.10, the "pkl_to_extxyz.py" file doesn't work at 2024.8.9 version of pymatgen.
3. Need to install [ASE](https://wiki.fysik.dtu.dk/ase/index.html), when you use the codes in "for_nequip" directory. The ASE requires to
    - Python 3.9 or newer
    - NumPy (base N-dimensional array package)
    - SciPy (library for scientific computing)
    - Matplotlib (plotting)
```shell
pip install --upgrade ase
```
