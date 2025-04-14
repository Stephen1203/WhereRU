import pandas as pd
import numpy as np
import os
from glob import glob


def ensure_directory(directory):
    """Ensure output directory exists, create it if not"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created output directory: {directory}")


def fill_missing_with_neighbors(feature_matrix):
    antennas, rows, cols = feature_matrix.shape

    for ant in range(antennas):
        matrix = feature_matrix[ant]
        for i in range(rows):
            for j in range(cols):
                if matrix[i, j] == -100.0:
                    neighbors = []
                    if i > 0:
                        if matrix[i - 1, j] != -100.0:
                            neighbors.append(matrix[i - 1, j])
                    if i < rows - 1:
                        if matrix[i + 1, j] != -100.0:
                            neighbors.append(matrix[i + 1, j])
                    if j > 0:
                        if matrix[i, j - 1] != -100.0:
                            neighbors.append(matrix[i, j - 1])
                    if j < cols - 1:
                        if matrix[i, j + 1] != -100.0:
                            neighbors.append(matrix[i, j + 1])

                    if neighbors:
                        matrix[i, j] = np.mean(neighbors)

    return feature_matrix


def create_dataset(csv_path, output_dir):
    print(f"\nProcessing file: {os.path.basename(csv_path)}")

    # Read CSV file, skip first 3 lines, no default column names
    df = pd.read_csv(csv_path, skiprows=3, header=None)

    # Extract needed columns (column B is tag_id, D is antenna_id, E is rssi)
    data = pd.DataFrame({
        'tag_id': df[1],  # Column B
        'antenna_id': df[3],  # Column D
        'rssi': df[4]  # Column E
    })

    # Remove all rows with NaN values
    data = data.dropna()

    # Ensure correct data types
    data['antenna_id'] = data['antenna_id'].astype(int)
    data['tag_id'] = data['tag_id'].astype(int)

    # Divide into rounds
    rounds = []
    current_round = 0
    prev_antenna = None

    for antenna_id in data['antenna_id']:
        if antenna_id == 1 and prev_antenna != 1:
            if prev_antenna is not None:
                current_round += 1
        rounds.append(current_round)
        prev_antenna = antenna_id

    data['round'] = rounds

    # Calculate total rounds and skip first two rounds
    total_rounds = data['round'].max() + 1
    data = data[data['round'] >= 2]  # Skip only first two rounds
    data['round'] = data['round'] - 2  # Renumber rounds, start from 0
    total_rounds -= 2  # Update total rounds (subtract only first two rounds)

    print(f"Total rounds (after skipping first two): {total_rounds}")

    X = []

    for round_idx in range(total_rounds):
        # Set feature matrix dimensions to (4, 8, 8)
        feature_matrix = np.full((4, 8, 8), -100.0)
        round_data = data[data['round'] == round_idx]
        grouped_data = round_data.groupby(['antenna_id', 'tag_id'])['rssi'].mean()

        for (antenna_id, tag_id), rssi in grouped_data.items():
            # Check tag ID range for 1-64
            if 1 <= antenna_id <= 4 and 1 <= tag_id <= 64:
                adjusted_tag_id = tag_id - 1
                # Calculate row/column indices for 8x8 matrix
                row_idx = adjusted_tag_id // 8
                col_idx = adjusted_tag_id % 8
                feature_matrix[antenna_id - 1, row_idx, col_idx] = rssi

        #feature_matrix = fill_missing_with_neighbors(feature_matrix)

        # Print detailed feature matrix info (print first two new rounds)
        if round_idx < 2:
            print(f"\nRound {round_idx + 1} feature matrix (original data round {round_idx + 3}):")
            for antenna_id in range(4):
                print(f"\nAntenna {antenna_id + 1} RSSI matrix:")
                print(feature_matrix[antenna_id])

        X.append(feature_matrix)

    X = np.array(X)

    # Use original CSV filename (without extension) as npy filename
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    output_filename = os.path.join(output_dir, f'{base_name}.npy')
    np.save(output_filename, X)
    print(f"\nData saved as {output_filename}")
    print(f"Data shape: {X.shape}")

    # Print basic information to verify data
    print("\nBasic data information:")
    print(f"Total rows: {len(data)}")
    print(f"Unique antenna IDs: {sorted(data['antenna_id'].unique())}")
    print(f"Unique tag IDs: {sorted(data['tag_id'].unique())}")

    return X


def process_all_files(input_dir="data", output_dir="processed_data"):
    # Ensure input and output directories exist
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist")
        return

    ensure_directory(output_dir)

    # Get all CSV files in the data directory
    csv_files = sorted(glob(os.path.join(input_dir, "*.csv")))

    if not csv_files:
        print(f"No CSV files found in directory: {input_dir}")
        return

    print(f"Found {len(csv_files)} CSV files in {input_dir} directory:")
    for i, file in enumerate(csv_files):
        print(f"{i + 1}. {os.path.basename(file)}")

    # Process each file
    for csv_file in csv_files:
        try:
            print(f"\n{'=' * 50}")
            print(f"Processing file: {os.path.basename(csv_file)}")
            print(f"{'=' * 50}")
            X = create_dataset(csv_file, output_dir)
        except Exception as e:
            print(f"Error processing file {csv_file}: {str(e)}")


if __name__ == "__main__":
    try:
        # Set input and output directories
        input_directory = "RFID_data"
        output_directory = "processed_RFID_data"

        # Process all CSV files in the data directory and store results in processed_data directory
        process_all_files(input_directory, output_directory)

        print(f"\nAll processed files have been saved in the {output_directory} directory")
    except Exception as e:
        print(f"Error: {str(e)}")