import pickle
import numpy as np
from pymatgen.core.structure import Structure
from ase.data import atomic_numbers
import logging

# This code works in pymatgen 2023.8.10 version.
# Python >= 3.8

# Setup logging
logging.basicConfig(filename='extraction.log', filemode='w', format='%(message)s', level=logging.INFO)

input_file = 'sampled_data_block_0_block_1.p'
output_file = 'sample-nequip.extxyz'

# Define allowed atomic numbers
allowed_species = [1, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 
                   23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 
                   41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 
                   58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 73, 74, 75, 
                   76, 77, 78, 79, 80, 81, 82, 83, 92, 93, 94]

# Load data from Pickle files
with open(input_file, 'rb') as f:
    data = pickle.load(f)
    #print(f'{input_file} is updated to data')
    logging.info(f"{input_file} is loaded")

# Track total counts
total_materials = len(data)
total_structures = sum(len(structures['structure']) for structures in data.values())
logging.info(f"Total materials: {total_materials}, Total structures: {total_structures}")

# Save to extxyz format
with open(output_file, 'w') as f:
    excluded_material_count = 0
    excluded_structure_count = 0
    length_mismatch_count = 0

    for material_id, structures in data.items():
        print(f"extract data: {material_id}")
        valid_material = False

        structure_count = len(structures['structure'])  # number of structures

        for i in range(structure_count):
            structure = structures['structure'][i]  # select structure
            positions = structure.cart_coords  # extract positions from pymatgen Structure
            energies = structures['energy'][i]  # energy at structure
            forces = structures['force'][i]  # force at structure
            stresses = structures['stress'][i]  # stress at structure
            atom_species = structures['structure'][i].species  # atom species in structure

            # Length confirmation: check if positions and forces have the same length
            if len(positions) != len(forces):
                print(f"Length mismatch for material ID {material_id}, structure index {i}")
                logging.info(f"Length mismatch for material ID {material_id}, structure index {i}")
                length_mismatch_count += 1
                excluded_structure_count += 1
                continue

            # Check if all species are allowed
            valid_indices = [j for j, sp in enumerate(atom_species) if atomic_numbers[sp.name] in allowed_species]
            if not valid_indices:
                print(f"No valid atoms for material ID {material_id}, structure index {i}")
                logging.info(f"No valid atoms for material ID {material_id}, structure index {i}")
                excluded_structure_count += 1
                continue

            valid_material = True

            # Lattice
            lattice = structure.lattice  # pymatgen Lattice object
            lattice_str = " ".join(map(str, lattice.matrix.flatten()))  # Lattice to string type

            # stress list to strings
            stress_flattened = [-0.1 * s for stress in stresses for s in stress]  # stress flatten and convert unit
            stress_str = " ".join(map(str, stress_flattened))  # to strings

            # Write the lattice information
            f.write(f"{len(valid_indices)}\n")
            f.write(f"Lattice=\"{lattice_str}\" Properties=species:S:1:pos:R:3:forces:R:3 stress=\"{stress_str}\" energy={energies} pbc=\"T T T\"\n")

            for j in valid_indices:
                species = atom_species[j]
                pos = positions[j]
                force = forces[j]
                f.write(f"{species:<3}\t{pos[0]:>15.8f}\t{pos[1]:>15.8f}\t{pos[2]:>15.8f}\t{force[0]:>15.8f}\t{force[1]:>15.8f}\t{force[2]:>15.8f}\n")

        if not valid_material:
            excluded_material_count += 1

    # Log summary of processed and excluded data
    logging.info(f"Excluded materials: {excluded_material_count}")
    logging.info(f"Excluded structures: {excluded_structure_count}")
    logging.info(f"Structures excluded due to length mismatch: {length_mismatch_count}")

print(f"extxyz data saved to {output_file}")
