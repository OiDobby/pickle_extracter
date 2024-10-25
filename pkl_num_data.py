import pickle

# data load from Pickle files
with open('block_0.p', 'rb') as f:
    data = pickle.load(f)
    print("block_0 is loaded")
with open('block_1.p', 'rb') as f:
    data.update(pickle.load(f))
    print("block_1 is updated to data")

#sample test
#input_file = 'sampled_data.p'
#with open(input_file, 'rb') as f:
#    data = pickle.load(f)

# count structure number
def count_structures(data):
    total_structures = 0
    for material_id, snapshots in data.items():
        structure_count = len(snapshots.get('structure', []))  # 각 material의 structure 갯수
        total_structures += structure_count
    return total_structures

# calculate number all of the structures
total_structure_count = count_structures(data)
print(f"Total number of structures in block_0 and block_1: {total_structure_count}")

