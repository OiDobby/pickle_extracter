import pickle
import numpy as np
from pymatgen.core.structure import Structure

# This code work in pymatgen 2023.8.10 version.
# Python >= 3.8

#input_file = 'sampled_data.p'
output_file = 'output_file.extxyz'

# data load from Pickle file
with open('block_0.p', 'rb') as f:
    data = pickle.load(f)
    print("block_0 is loaded")
with open('block_1.p', 'rb') as f:
    data.update(pickle.load(f))
    print("block_1 is updated to data")


# save extxyz format
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

            # length confirmation
            if len(positions) != len(forces):
                print(f"Length mismatch for material ID {material_id}, structure index {i}")
                continue

            # Lattice
            lattice = structure.lattice  # pymatgen Lattice object
            lattice_str = " ".join(map(str, lattice.matrix.flatten()))  # Lattice to string type

            # Write the lattice information
            # stress list to strings
            stress_flattened = [-0.1 * s for stress in stresses for s in stress]  # stress flatten and convert unit (KBa to GPa)
            stress_str = " ".join(map(str, stress_flattened))  # to strings
            f.write(f"{len(positions)}\n")
            f.write(f"Lattice=\"{lattice_str}\" Properties=species:S:1:pos:R:3:forces:R:3 stress=\"{stress_str}\" energy={energies} pbc=\"T T T\"\n")


            # Write positions and forces
            for j in range(len(positions)):
                species = atom_species[j]  # atomic species
                pos = positions[j]  # position
                force = forces[j] # force

                # write in extxyz format
                f.write(f"{species:<3}\t{pos[0]:>15.8f}\t{pos[1]:>15.8f}\t{pos[2]:>15.8f}\t{force[0]:>15.8f}\t{force[1]:>15.8f}\t{force[2]:>15.8f}\n")

print(f"extxyz data saved to {output_file}")
