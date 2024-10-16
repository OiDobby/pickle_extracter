import pickle
import random

# extract max_samples dictionary from both the block_0 and block_1
max_samples = 100
n_sample = 10

# file names as inputs
input1 = 'block_0.p'
input2 = 'block_1.p'
output_prefix = f"sampled_data_{input1.split('.')[0]}_{input2.split('.')[0]}"

# Load data from Pickle files
with open(input1, 'rb') as f:
    data = pickle.load(f)
    print(f"{input1} is loaded")
with open(input2, 'rb') as f:
    data.update(pickle.load(f))
    print(f"{input2} is updated to data")

# Collect all keys into a list
all_keys = list(data.keys())

# Repeat sampling n times
for i in range(n_sample):
    # Randomly sample max_samples from all keys
    sampled_keys = random.sample(all_keys, min(max_samples, len(all_keys)))
    
    # Create new data with the sampled entries
    sampled_data = {k: data[k] for k in sampled_keys}
    
    # Generate output file name (save with different names for each repetition)
    output_file = f"{output_prefix}_{i+1}.p"
    
    # Save the sampled data to a file
    with open(output_file, 'wb') as f:
        pickle.dump(sampled_data, f)
    
    print(f'Sampled data {i+1}/{n_sample} saved to {output_file}')
