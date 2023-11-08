import pandas as pd
import numpy as np

# ---- Load the Kaggle Dataset ----

# The dataset is loaded from a specified path and stored in a DataFrame.
kaggle_dataset = pd.read_csv('water_potability_augmented.csv')

# ---- Augment the Kaggle Dataset ----

# Generate a series of dates for the Kaggle dataset starting from January 1, 2023.
kaggle_dataset['Date'] = pd.date_range(start="2023-01-01", periods=len(kaggle_dataset), freq="D")

# Simulate rainfall data with an average and added variance.
# There's more rain (additional random values) added for the month of May.
rainfall_avg = 5
kaggle_rainfall = np.random.normal(rainfall_avg, 2, len(kaggle_dataset))
kaggle_rainfall = [max(0, r) for r in kaggle_rainfall]
for i, date in enumerate(kaggle_dataset['Date']):
    if date.month == 5:
        kaggle_rainfall[i] += np.random.uniform(5, 10)
kaggle_dataset['Rainfall'] = kaggle_rainfall

# A derived feature indicating if the algae concentration (inferred from solids) will increase the next day.
kaggle_dataset['Algae Increase'] = (kaggle_dataset['Solids'].diff(periods=-1) < 0).astype(int)

# Simulate Microbial Counts using a Poisson distribution.
# https://www.scribbr.com/statistics/poisson-distribution/#:~:text=A%20Poisson%20distribution%20is%20a,the%20mean%20number%20of%20events.
# Reasoning: The Poisson distribution is often used to model the number of
#   times an event occurs within a fixed period. It's commonly used for counting data,
#   like the number of bacteria or microbes in a certain volume of water.
# Reference: Consul, P. C., & Jain, G. C. (1973). A generalization of the Poisson distribution. Technometrics, 15(4), 791-799.kaggle_microbial_counts = np.random.poisson(30, len(kaggle_dataset))
kaggle_microbial_counts = np.random.poisson(30, len(kaggle_dataset))
kaggle_dataset['Microbial Counts'] = [max(0, m) for m in kaggle_microbial_counts]

# Simulate BOD (Biochemical Oxygen Demand) using a normal distribution.
# Reasoning: Many natural phenomena, due to the Central Limit Theorem,
#   tend to have outcomes that are normally distributed, especially when they are the result of many random processes.
# Reference: DeCarlo, L. T. (1997). On the meaning and use of kurtosis. Psychological methods, 2(3), 292.
kaggle_BOD = np.random.normal(7.5, 5, len(kaggle_dataset))
kaggle_dataset['BOD'] = [max(0, b) for b in kaggle_BOD]

# Simulate a combined index for Heavy Metals using a uniform distribution.
# Reasoning: The uniform distribution provides a constant probability for all outcomes in a specified range.
#   It's used when there's no particular preference or weighting for values within a given range.
# Reference: Johnson, N. L., Kotz, S., & Balakrishnan, N. (1994). Continuous univariate distributions, Vol. 1. (Wiley Series in Probability and Mathematical Statistics).
kaggle_dataset['Heavy Metals Index'] = np.random.uniform(0, 1, len(kaggle_dataset))

# ---- Regenerate the Synthetic Dataset ----

# Generate dates spanning three years.
num_days = 3 * 365
dates = pd.date_range(start="2020-01-01", periods=num_days, freq="D")

# Simulate seasonal temperature using a sine wave with added random noise.
temperature = 20 + 10 * np.sin(2 * np.pi * dates.dayofyear / 365) + np.random.normal(0, 3, num_days)

# Similar rainfall simulation as before, but for the synthetic dataset.
rainfall_avg = 5
rainfall = np.random.normal(rainfall_avg, 2, num_days)
rainfall = [max(0, r) for r in rainfall]
for i, date in enumerate(dates):
    if date.month == 5:
        rainfall[i] += np.random.uniform(5, 10)

# Simulate Algae Concentration influenced by temperature and rainfall with added random noise.
algae_base = 50
algae_concentration = algae_base + 0.5 * np.array(temperature) + 0.3 * np.array(rainfall)
algae_concentration = [a + np.random.uniform(-10, 10) for a in algae_concentration]

# Simulate other water quality features using various statistical distributions.
pH = np.random.normal(7.5, 0.5, num_days)
DO = np.random.normal(9, 2, num_days)
turbidity = np.random.normal(7, 5, num_days)
nitrate = np.random.normal(3.5, 2, num_days)
phosphorus = np.random.normal(0.3, 0.2, num_days)
TDS = np.random.normal(350, 150, num_days)
microbial_counts = np.random.poisson(30, num_days)
BOD = np.random.normal(7.5, 5, num_days)
heavy_metals_index = np.random.uniform(0, 1, num_days)
chlorine_added = [5 if a > 70 else 3 if a > 60 else 1 for a in algae_concentration]

# Construct the synthetic dataset.
enhanced_dataset = pd.DataFrame({
    "Date": dates,
    "Temperature": temperature,
    "pH": pH,
    "Dissolved Oxygen": DO,
    "Rainfall": rainfall,
    "TDS": TDS,
    "Chlorine Added": chlorine_added,
    "Turbidity": turbidity,
    "Algae Concentration": algae_concentration,
    "Nitrate": nitrate,
    "Phosphorus": phosphorus,
    "Microbial Counts": microbial_counts,
    "BOD": BOD,
    "Heavy Metals Index": heavy_metals_index
})

# ---- Merge the Datasets ----

# Combine the synthetic dataset with the augmented Kaggle dataset.
final_dataset = pd.concat([enhanced_dataset, kaggle_dataset], axis=0, ignore_index=True)

# Fill missing values in the dataset using the median of respective columns.
final_dataset = final_dataset.fillna(final_dataset.median(numeric_only=True))

# Display the first few rows of the merged dataset.
print("Augmented Dataset:\n", final_dataset.head())
final_dataset.to_csv('water_potability_augmented_train.csv', index=False)
