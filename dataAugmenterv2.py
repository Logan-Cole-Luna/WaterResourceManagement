import pandas as pd
import numpy as np

# Load the original Kaggle dataset
kaggle_dataset = pd.read_csv('water_potability_augmented.csv')

# Generate a series of dates for the Kaggle dataset starting from January 1, 2023.
kaggle_dataset['Date'] = pd.date_range(start="2023-01-01", periods=len(kaggle_dataset), freq="D")

# Simulate rainfall data with an average, added variance, and seasonality.
# More rain in spring and fall, less in summer and winter.
rainfall_avg = 5
rainfall_seasonality = 3 * np.sin(2 * np.pi * kaggle_dataset['Date'].dt.dayofyear / 365)
kaggle_rainfall = np.random.normal(rainfall_avg + rainfall_seasonality, 2, len(kaggle_dataset))
kaggle_rainfall = [max(0, r) for r in kaggle_rainfall]

kaggle_dataset['Rainfall'] = kaggle_rainfall


# A derived feature indicating if the algae concentration (inferred from solids) will increase the next day.
kaggle_dataset['Algae Increase'] = (kaggle_dataset['Solids'].diff(periods=-1) < 0).astype(int)

# Simulate Microbial Counts using a Poisson distribution.
kaggle_dataset['Microbial Counts'] = np.random.poisson(30, len(kaggle_dataset))

# Simulate BOD (Biochemical Oxygen Demand) using a normal distribution.
kaggle_dataset['BOD'] = np.random.normal(7.5, 5, len(kaggle_dataset))

# Simulate a combined index for Heavy Metals using a uniform distribution.
kaggle_dataset['Heavy Metals Index'] = np.random.uniform(0, 1, len(kaggle_dataset))

# Simulate seasonal temperature using a sine wave with added random noise.
kaggle_dataset['Temperature'] = 20 + 10 * np.sin(2 * np.pi * kaggle_dataset['Date'].dt.dayofyear / 365) + np.random.normal(0, 3, len(kaggle_dataset))

# Simulate Algae Concentration influenced by temperature and rainfall with added random noise.
algae_base = 50
algae_concentration = algae_base + 0.5 * np.array(kaggle_dataset['Temperature']) + 0.3 * np.array(kaggle_dataset['Rainfall'])
algae_concentration = [a + np.random.uniform(-10, 10) for a in algae_concentration]
kaggle_dataset['Algae Concentration'] = algae_concentration


# Save the augmented dataset
kaggle_dataset.to_csv('water_potability_augmented_example.csv', index=False)
