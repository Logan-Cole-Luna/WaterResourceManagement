import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
final_dataset = pd.read_csv('water_potability_augmented_v2.csv')

# 1. Temperature over time
plt.figure(figsize=(14, 6))
plt.plot(final_dataset['Date'], final_dataset['Temperature'], color='blue', label='Temperature')
plt.title('Temperature over Time')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.tight_layout()
plt.show()

# 2. Rainfall over time
plt.figure(figsize=(14, 6))
plt.plot(final_dataset['Date'], final_dataset['Rainfall'], color='cyan', label='Rainfall')
plt.title('Rainfall over Time')
plt.xlabel('Date')
plt.ylabel('Rainfall (mm)')
plt.legend()
plt.tight_layout()
plt.show()

# 3. Algae Concentration over time
plt.figure(figsize=(14, 6))
plt.plot(final_dataset['Date'], final_dataset['Algae Concentration'], color='green', label='Algae Concentration')
plt.title('Algae Concentration over Time')
plt.xlabel('Date')
plt.ylabel('Algae Concentration')
plt.legend()
plt.tight_layout()
plt.show()

# 4. Correlation Heatmap
plt.figure(figsize=(14, 10))
correlation_matrix = final_dataset.drop(columns=['Date']).corr()
# seaborn import, used to make heat map
# How does it predict how they affect one another?
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()


import seaborn as sns
import matplotlib.pyplot as plt

# Make sure your Date column is in datetime format
final_dataset['Date'] = pd.to_datetime(final_dataset['Date'])

# Time Series Plot for Algae Concentration
plt.figure(figsize=(14, 6))
sns.lineplot(x='Date', y='Algae Concentration', data=final_dataset)
plt.title('Algae Concentration Over Time')
plt.xlabel('Date')
plt.ylabel('Algae Concentration')
plt.show()


# Scatter Plot for Algae Concentration vs Temperature
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Temperature', y='Algae Concentration', data=final_dataset)
plt.title('Algae Concentration vs Temperature')
plt.xlabel('Temperature')
plt.ylabel('Algae Concentration')
plt.show()

# Distribution Plot for BOD
plt.figure(figsize=(10, 6))
sns.histplot(final_dataset['BOD'], kde=True)
plt.title('Distribution of Biochemical Oxygen Demand (BOD)')
plt.xlabel('BOD')
plt.show()

# Box Plot for Algae Increase vs Algae Concentration
plt.figure(figsize=(10, 6))
sns.boxplot(x='Algae Increase', y='Algae Concentration', data=final_dataset)
plt.title('Algae Concentration by Algae Increase Category')
plt.xlabel('Algae Increase')
plt.ylabel('Algae Concentration')
plt.show()

# Heatmap of Correlations
plt.figure(figsize=(12, 10))
correlation_matrix = final_dataset.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# Pair Plot for a subset of variables
sns.pairplot(final_dataset[['Algae Concentration', 'Temperature', 'Rainfall', 'BOD']])
plt.show()

# Violin Plot for Temperature across Algae Increase categories
plt.figure(figsize=(10, 6))
sns.violinplot(x='Algae Increase', y='Temperature', data=final_dataset)
plt.title('Temperature Distribution by Algae Increase Category')
plt.xlabel('Algae Increase')
plt.ylabel('Temperature')
plt.show()
