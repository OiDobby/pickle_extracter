import pickle
import numpy as np
import logging
from pymatgen.core.structure import Structure
import ase.neighborlist
import ase.io

# Configure logging
logging.basicConfig(filename='neighbor_list_log.txt', level=logging.INFO, format='%(message)s')

def calculate_neighbor_list_and_save(file_list, r_max, output_with_edges, output_no_edges, strict_self_interaction=True, self_interaction=False):
    """
    Reads atomic structures from multiple pickle files, calculates neighbor lists, and saves structures with edges remaining to 'output_with_edges'
    and structures with no edges remaining to 'output_no_edges', logging the process to a log file.
    
    Args:
        file_list (list): List of paths to multiple pickle files
        r_max (float): Radius for determining neighbors
        output_with_edges (str): Path to extxyz file for saving structures with edges remaining
        output_no_edges (str): Path to extxyz file for saving structures with no edges remaining
        strict_self_interaction (bool): Whether to recognize interactions with self in periodic images
        self_interaction (bool): Whether to include self-interactions within the same cell
    """
    structures = {}

    # Load data from each file in the file list and merge into structures
    for file in file_list:
        with open(file, 'rb') as f:
            structures.update(pickle.load(f))  # Update structures (assumed to be a dictionary)
            print(f"{file} is loaded and updated to data")

    print("Processing started...")

    no_edge_count = 0  # Count of cases with no remaining edges

    # Split and save data into two files
    with open(output_with_edges, 'w') as f_with_edges, open(output_no_edges, 'w') as f_no_edges:
        for i, (material_id, material_data) in enumerate(structures.items()):
            # Print progress every 1000 material_ids
            if i % 1000 == 0 and i > 0:
                print(f"Processed {i} material_ids...")

            # Process multiple snapshots for each material_id
            snapshots = material_data['structure']  # List of pymatgen Structure objects

            for idx, snapshot in enumerate(snapshots):
                positions = np.array(snapshot.cart_coords)  # Atomic coordinates
                lattice = np.array(snapshot.lattice.matrix)  # Cell information
                pbc = (True, True, True)  # Periodic boundary conditions

                # Calculate neighbor relations using ASE's neighborlist function
                first_index, second_index, shifts = ase.neighborlist.primitive_neighbor_list(
                    "ijS",
                    pbc,  # Periodic boundary conditions
                    lattice,  # Cell information
                    positions,  # Atomic coordinates
                    cutoff=float(r_max),  # Radius for neighbors
                    self_interaction=strict_self_interaction,  # Whether to allow self-interaction
                    use_scaled_positions=False,  # Whether to use scaled coordinates
                )

                # Logic to eliminate self-interactions
                if not self_interaction:
                    bad_edge = first_index == second_index  # Find edges connected to themselves
                    bad_edge &= np.all(shifts == 0, axis=1)  # Keep only self-interactions within the same cell
                    keep_edge = ~bad_edge  # Keep interactions with other atoms and self-interactions across cell boundaries
                    if not np.any(keep_edge):
                        no_edge_count += 1  # Increment count for cases with no edges remaining
                        logging.info(f"Material ID {material_id}, structure {idx}: No edges remain after eliminating self-interactions.")
                        # Save structures with no edges remaining to f_no_edges file
                        f_output = f_no_edges
                    else:
                        # Retain only remaining edges
                        first_index = first_index[keep_edge]
                        second_index = second_index[keep_edge]
                        shifts = shifts[keep_edge]
                        f_output = f_with_edges  # Save structures with edges remaining to f_with_edges
                else:
                    f_output = f_with_edges  # Save structures with edges remaining to f_with_edges

                # Additional code to save in extxyz format
                energies = material_data['energy'][idx]  # Energy information
                forces = material_data['force'][idx]  # Force information
                stresses = material_data['stress'][idx]  # Stress information
                atom_species = snapshot.species  # Atom species

                # Save lattice information
                lattice_str = " ".join(map(str, lattice.flatten()))  # Convert lattice to string

                # Convert stress list to string
                stress_flattened = [-0.1 * s for stress in stresses for s in stress]  # Flatten stress and adjust units
                stress_str = " ".join(map(str, stress_flattened))  # Convert to string
                f_output.write(f"{len(positions)}\n")
                f_output.write(f"Lattice=\"{lattice_str}\" Properties=species:S:1:pos:R:3:forces:R:3 stress=\"{stress_str}\" energy={energies} pbc=\"T T T\"\n")

                # Save position and force information for each atom
                for j in range(len(positions)):
                    species = atom_species[j]  # Atom species
                    pos = positions[j]  # Atomic position
                    force = forces[j]  # Force
                    f_output.write(f"{species:<3}\t{pos[0]:>15.8f}\t{pos[1]:>15.8f}\t{pos[2]:>15.8f}\t{force[0]:>15.8f}\t{force[1]:>15.8f}\t{force[2]:>15.8f}\n")

    # Output the total number of cases with no remaining edges and log it
    print(f"Processing complete. Number of materials with no remaining edges: {no_edge_count}")
    logging.info(f"Total number of materials with no remaining edges: {no_edge_count}")

# Usage
file_list = ["../block_0.p", "../block_1.p"]  # List of paths to pickle files
r_max = 5.0  # It is the same as nequip tag
output_with_edges = 'output_with_edges.extxyz'  # File to save structures with edges remaining
output_no_edges = 'output_no_edges.extxyz'  # File to save structures with no edges remaining

calculate_neighbor_list_and_save(file_list, r_max, output_with_edges, output_no_edges, self_interaction=False)
