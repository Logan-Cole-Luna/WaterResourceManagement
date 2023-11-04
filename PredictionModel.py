# https://www.kaggle.com/code/mrtoddy/kagglepredic
# Time Series Forecasting

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load the dataset
dataset = pd.read_csv('water_potability_augmented_v2.csv')

# Sort dataset by Date
dataset = dataset.sort_values(by='Date')

# Time Series Data Exploration
# Plot Algae Concentration over time
plt.figure(figsize=(12, 6))
dataset.set_index('Date')['Algae Concentration'].plot()
plt.title('Algae Concentration Over Time')
plt.ylabel('Algae Concentration')
plt.xlabel('Date')
plt.show()

# Split dataset chronologically
train_size = int(len(dataset) * 0.6)
train_dataset = dataset[:train_size]
test_dataset = dataset[train_size:]

# Drop non-numeric columns and irrelevant columns for this modeling process
X_train = train_dataset.drop(['Algae Concentration', 'Date'], axis=1)
y_train = train_dataset['Algae Concentration']

X_test = test_dataset.drop(['Algae Concentration', 'Date'], axis=1)
y_test = test_dataset['Algae Concentration']
print(y_test)

# Train a Linear Regression model
regression = LinearRegression()
regression.fit(X_train, y_train)

# Evaluate the model
score = regression.score(X_test, y_test)
print(f"R^2 Score: {score}")

# Predict on the test dataset (if you want to submit or save predictions)
predict = regression.predict(X_test)

# Plot Actual vs. Predicted
plt.figure(figsize=(14, 6))
plt.plot(test_dataset['Date'], y_test, label='Actual Values', color='blue')
plt.plot(test_dataset['Date'], predict, label='Predicted Values', color='red', linestyle='dashed')
plt.title('Actual vs. Predicted Algae Concentration')
plt.xlabel('Date')
plt.ylabel('Algae Concentration')
plt.legend()
plt.show()

# Calculate and display the MAE and RMSE
mae = mean_absolute_error(y_test, predict)
rmse = np.sqrt(mean_squared_error(y_test, predict))

print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Square Error (RMSE): {rmse:.2f}")


# The dataset for the classification task
classification_data_path = 'water_potability_augmented_v2.csv'
data = pd.read_csv(classification_data_path)

# Prepare the data for classification
data.dropna(inplace=True)  # Drop rows with missing values for simplicity
X = data.drop(['Potability', 'Date'], axis=1)  # Exclude 'Date' for model training
Y = data['Potability']

# Normalize and standardize the features
normalizer = MinMaxScaler()
standardizer = StandardScaler()
X = normalizer.fit_transform(X)
X = standardizer.fit_transform(X)

# Split the data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Dictionary to hold model names and their scores
model_scores = {}

# create instances of all models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Naive Bayes': GaussianNB(),
    'Support Vector Machine': SVC(),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'Bagging': BaggingClassifier(),
    'AdaBoost': AdaBoostClassifier(),
    'Gradient Boosting': GradientBoostingClassifier(),
    'Extra Trees': ExtraTreeClassifier(),
}

# Train and evaluate each model
for name, model in models.items():
    model.fit(X_train, Y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(Y_test, y_pred)
    model_scores[name] = accuracy

# Convert model_scores to a DataFrame for seaborn plotting
model_scores_df = pd.DataFrame(list(model_scores.items()), columns=['Model', 'Accuracy'])

# Plot the accuracies using seaborn
plt.figure(figsize=(14, 8))
accuracy_plot = sns.barplot(x='Accuracy', y='Model', data=model_scores_df.sort_values('Accuracy', ascending=False), palette="Blues_d")
plt.title('Classification Model Accuracies')
plt.xlabel('Accuracy')
plt.ylabel('Model')
plt.tight_layout()

# Display the plot
plt.show()

# Return the scores for each model
model_scores_df.sort_values('Accuracy', ascending=False)

