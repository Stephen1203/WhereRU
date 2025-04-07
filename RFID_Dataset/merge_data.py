import numpy as np
import os

base_dir = "processed_RFID_data"  # Replace with your data path
output_dir = os.path.join(base_dir, "merged_RFID_data")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get all .npy files in the directory
all_files = os.listdir(base_dir)
npy_files = [f for f in all_files if f.endswith('.npy')]

# Create a dictionary to store files for each category
class_files = {}

# Categorize files based on the first number in the filename
for file_name in npy_files:
    # Get the first number in the filename as the category
    class_num = int(file_name.split('.')[0])
    if class_num not in class_files:
        class_files[class_num] = []
    class_files[class_num].append(file_name)

# Process files for each category
for class_idx in sorted(class_files.keys()):
    data_list = []
    print(f"\nProcessing Class {class_idx}:")

    # Process all files in this category
    for file_name in class_files[class_idx]:
        file_path = os.path.join(base_dir, file_name)
        data = np.load(file_path)
        print(f"  File {file_name}: n = {data.shape[0]}")
        data_list.append(data)

    if data_list:  # Ensure there is data to merge
        merged_data = np.concatenate(data_list, axis=0)

        # Save to the new folder
        output_path = os.path.join(output_dir, f"{class_idx}_merged.npy")
        np.save(output_path, merged_data)

        print(f"  --> Merged file {class_idx}_merged.npy: n = {merged_data.shape[0]}, full shape = {merged_data.shape}")
    else:
        print(f"  Warning: No data files found for class {class_idx}")

print("\nProcessing complete!")