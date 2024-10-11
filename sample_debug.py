import pickle

# extract max_samples dictionary from both the block_0 and block_1
max_samples = 100
sampled_data = {}

# sampling from block_0
with open('block_0.p', 'rb') as f:
    block_0_data = pickle.load(f)
    sampled_data.update({k: block_0_data[k] for k in list(block_0_data.keys())[:max_samples]})

# sampling from block_1
with open('block_1.p', 'rb') as f:
    block_1_data = pickle.load(f)
    sampled_data.update({k: block_1_data[k] for k in list(block_1_data.keys())[:max_samples]})

# save in new Pickle file
with open('sampled_data.p', 'wb') as f:
    pickle.dump(sampled_data, f)

print("Sampled data saved to 'sampled_data.p'")

