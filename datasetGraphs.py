import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
final_dataset = pd.read_csv('water_potability_augmented.csv')

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
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()