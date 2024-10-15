import pickle
import numpy as np
from pymatgen.core.structure import Structure
from ase.data import atomic_numbers

# This code works in pymatgen 2023.8.10 version.
# Python >= 3.8

# file names
input_file1 = 'block_0.p'
input_file2 = 'block_1.p'
output_file = 'output_file.extxyz'

# Define allowed atomic numbers
allowed_species = [1, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 
                   23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 
                   41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 
                   58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 73, 74, 75, 
                   76, 77, 78, 79, 80, 81, 82, 83, 92, 93, 94]

# Load data from Pickle files
with open(input_file1, 'rb') as f:
    data = pickle.load(f)
    print(f"{input_file1} is loaded")
with open(input_file2, 'rb') as f:
    data.update(pickle.load(f))
    print(f"{input_file2} is updated to data")

# Save to extxyz format
with open(output_file, 'w') as f:
    for material_id, structures in data.items():
        print(f"extract data: {material_id}")
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
                continue

            # Filter out species not in allowed_species
            filtered_positions = []
            filtered_forces = []
            filtered_species = []

            for j, species in enumerate(atom_species):
                atomic_num = atomic_numbers.get(species.symbol)
                if atomic_num in allowed_species:
                    filtered_positions.append(positions[j])
                    filtered_forces.append(forces[j])
                    filtered_species.append(species.symbol)

            # Skip if no valid atoms remain
            if not filtered_positions:
                print(f"No valid atoms for material ID {material_id}, structure index {i}")
                continue

            # Lattice
            lattice = structure.lattice  # pymatgen Lattice object
            lattice_str = " ".join(map(str, lattice.matrix.flatten()))  # Lattice to string type

            # Write the lattice information
            # stress list to strings
            stress_flattened = [-0.1 * s for stress in stresses for s in stress]  # stress flatten and convert unit
            stress_str = " ".join(map(str, stress_flattened))  # to strings
            f.write(f"{len(filtered_positions)}\n")
            f.write(f"Lattice=\"{lattice_str}\" Properties=species:S:1:pos:R:3:forces:R:3 stress=\"{stress_str}\" energy={energies} pbc=\"T T T\"\n")

            # Write filtered positions and forces
            for j in range(len(filtered_positions)):
                species = filtered_species[j]  # atomic species
                pos = filtered_positions[j]  # position
                force = filtered_forces[j]  # force

                # write in extxyz format
                f.write(f"{species:<3}\t{pos[0]:>15.8f}\t{pos[1]:>15.8f}\t{pos[2]:>15.8f}\t{force[0]:>15.8f}\t{force[1]:>15.8f}\t{force[2]:>15.8f}\n")

print(f"extxyz data saved to {output_file}")
