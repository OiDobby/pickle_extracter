import pickle
import random

# extract max_samples dictionary from both the block_0 and block_1
max_samples = 100
sampled_data = {}

# file names as inputs
input1 = 'block_0.p'
input2 = 'block_1.p'
output = f"sampled_data_{input1.split('.')[0]}_{input2.split('.')[0]}.p"

# sampling from block_0
with open(input1, 'rb') as f:
    block_0_data = pickle.load(f)
    print(f"File {input1} loaded successfully.")
    block_0_keys = random.sample(list(block_0_data.keys()), min(max_samples, len(block_0_data)))
    sampled_data.update({k: block_0_data[k] for k in block_0_keys})
    #sampled_data.update({k: block_0_data[k] for k in list(block_0_data.keys())[:max_samples]})

# sampling from block_1
with open(input2, 'rb') as f:
    block_1_data = pickle.load(f)
    print(f"File {input2} loaded successfully.")
    block_1_keys = random.sample(list(block_1_data.keys()), min(max_samples, len(block_1_data)))
    sampled_data.update({k: block_1_data[k] for k in block_1_keys})
    #sampled_data.update({k: block_1_data[k] for k in list(block_1_data.keys())[:max_samples]})

# save in new Pickle file
with open(output, 'wb') as f:
    pickle.dump(sampled_data, f)

print(f'Randomly sampled data saved to {output}')

