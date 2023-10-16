import pandas as pd
import numpy as np

# Load the provided Kaggle dataset
kaggle_dataset = pd.read_csv('/mnt/data/water_potability.csv')

# Augment the Kaggle dataset with additional features

# 1. Date: Generate a series of dates for the Kaggle dataset
kaggle_dataset['Date'] = pd.date_range(start="2023-01-01", periods=len(kaggle_dataset), freq="D")

# 2. Rainfall: Simulate rainfall data with more rain in certain months (like May)
rainfall_avg = 5
kaggle_rainfall = np.random.normal(rainfall_avg, 2, len(kaggle_dataset))
kaggle_rainfall = [max(0, r) for r in kaggle_rainfall]
for i, date in enumerate(kaggle_dataset['Date']):
    if date.month == 5:
        kaggle_rainfall[i] += np.random.uniform(5, 10)
kaggle_dataset['Rainfall'] = kaggle_rainfall

# 3. Algae Increase: Create a target variable that indicates if the algae concentration will increase the next day
kaggle_dataset['Algae Increase'] = (kaggle_dataset['Solids'].diff(periods=-1) < 0).astype(int)

# 4. Microbial Counts: Simulate Microbial Counts
kaggle_microbial_counts = np.random.poisson(30, len(kaggle_dataset))
kaggle_dataset['Microbial Counts'] = [max(0, m) for m in kaggle_microbial_counts]

# 5. BOD (Biochemical Oxygen Demand): Simulate BOD
kaggle_BOD = np.random.normal(7.5, 5, len(kaggle_dataset))
kaggle_dataset['BOD'] = [max(0, b) for b in kaggle_BOD]

# 6. Heavy Metals Index: Simulate Heavy Metals (combined index for simplicity)
kaggle_dataset['Heavy Metals Index'] = np.random.uniform(0, 1, len(kaggle_dataset))

# Display the augmented Kaggle dataset
kaggle_dataset.head()
