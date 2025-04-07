# RFID Indoor Localization Dataset

## Overview

This dataset supports research on privacy-sensitive indoor localization using RFID technology, specifically for the "WhereRU" system. It contains RSSI (Received Signal Strength Indicator) values collected from a grid of passive RFID tags when a person stands at different locations with different orientations.

## Data Collection Setup

### Hardware
- **RFID Reader**: Impinj R420 with a 4-antenna array
- **RFID Tags**: Impinj H47 passive tags
- **Tag Arrangement**: 8×8 grid (64 tags) with 20cm spacing between tags (approximating half-wavelength of UHF RFID signals at 915 MHz)
- **Experimental Area**: 2m × 2m square divided into 16 equal grids (0.5m × 0.5m each)

### Collection Methodology
- Volunteers stood in the center of each grid cell facing four different orientations (front, back, left, right)
- Background movement was introduced to create realistic interference
- Ultrasonic sensors were installed during data collection to maintain environmental consistency
- For each position-orientation combination, RSSI values were collected from all 64 tags via the 4-antenna array
- Each sample consists of a 4-channel 8×8 matrix (4 antennas × 64 tags)

### Dataset Size
- Approximately 1,600 samples per grid cell
- **Total samples**: 25,600
- **Features per sample**: 4×8×8 = 256 RSSI values

## Data Format

The dataset is provided in NumPy format:
- `.npy` files containing processed RSSI matrices
- Each sample contains RSSI readings from all 4 antennas for the 8×8 grid of tags
- The dataset leverages the human occlusion effect, where a person's presence alters RSSI values

## Preprocessing

The data processing pipeline includes:
1. Reading raw CSV files from the RFID reader
2. Extracting tag_id, antenna_id, and RSSI values
3. Organizing data into rounds of measurements
4. Skipping the first two rounds to ensure stability
5. Creating 4×8×8 feature matrices (4 antennas, 8×8 tag grid)
6. Handling missing values through interpolation based on neighboring tag readings

## Directory Structure

```
RFID_Dataset/
├── processed_data/        # Processed .npy files
├── merged_data/           # Merged datasets by position
├── scripts/               # Processing scripts
│   ├── process_raw.py     # Script for processing raw CSV data
│   └── merge_data.py      # Script for merging processed files
└── README.md              # This documentation file
```

## Usage Examples

```python
import numpy as np
import matplotlib.pyplot as plt

# Load a processed dataset file
data = np.load('merged_data/1_merged.npy')

# Display information about the dataset
print(f"Dataset shape: {data.shape}")
print(f"Number of samples: {data.shape[0]}")
print(f"Feature dimensions: {data.shape[1:]} (antennas × rows × columns)")

# Visualize RSSI values from the first antenna for a sample
plt.figure(figsize=(8, 6))
plt.imshow(data[0, 0], cmap='viridis')
plt.colorbar(label='RSSI (dBm)')
plt.title('RSSI Values from First Antenna')
plt.xlabel('Tag Column')
plt.ylabel('Tag Row')
plt.show()
```

## Data Processing Code

The repository includes the following processing scripts:

### `process_raw.py` (Data Processing Script)
This script transforms raw CSV data from the RFID reader into structured NumPy arrays:
- Extracts tag_id, antenna_id, and RSSI values
- Organizes readings into measurement rounds
- Creates 4-dimensional feature matrices (samples × antennas × grid_rows × grid_cols)
- Handles missing RSSI readings through neighborhood interpolation

### `merge_data.py` (Data Merging Script)
This script combines processed files from multiple collection sessions:
- Groups files by location category
- Concatenates data from the same location
- Creates consolidated datasets for each position

## Temporary Citation

This dataset is currently unpublished. If you use this dataset before publication, please contact the authors for appropriate citation information.

```
# After publication, please use the following citation format:
@article{WhereRU2025,
  title={WhereRU: Privacy-Sensitive Indoor Localization using RFID Technology},
  author={[Authors]},
  journal={[Journal/Conference]},
  year={2025}
}
```

## License

This dataset is made available under the [Choose your license - e.g., CC BY-NC 4.0] license.

## Contact

For questions about the dataset, please contact:
[Your email/contact information]

---

**Note**: This dataset accompanies a paper currently under review. The full citation information and additional documentation will be updated upon publication.
