# https://www.kaggle.com/code/mrtoddy/kagglepredic
# Time Series Forecasting
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates


def train(dataset):
    # Sort dataset by Date
    dataset = dataset.sort_values(by='Date')

    # Split dataset chronologically
    train_size = int(len(dataset) * 0.6)
    train_dataset = dataset[:train_size]
    test_dataset = dataset[train_size:]

    # Drop non-numeric columns and irrelevant columns for this modeling process
    X_train = train_dataset.drop(['Algae Concentration', 'Date'], axis=1)
    y_train = train_dataset['Algae Concentration']

    X_test = test_dataset.drop(['Algae Concentration', 'Date'], axis=1)
    y_test = test_dataset['Algae Concentration']

    # Train a Linear Regression model
    regression = LinearRegression()
    regression.fit(X_train, y_train)

    # Evaluate the model
    score = regression.score(X_test, y_test)
    print(f"R^2 Score: {score}")

    # Predict on the test dataset
    predictions = regression.predict(X_test)

    # Plot Actual vs. Predicted - ensuring that the dates match the predictions
    plt.figure(figsize=(14, 6))
    # plt.plot(test_dataset['Date'], y_test, label='Actual Values', color='blue')
    plt.plot(test_dataset['Date'], predictions, label='Predicted Values', color='red', linestyle='dashed')
    plt.title('Predicted Algae Concentration')
    plt.xlabel('Date')
    plt.ylabel('Algae Concentration')

    # Format the date on x-axis to display every 5 years
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.legend()
    plt.savefig('predicted_algae_concentration.png')
    plt.show()
    plt.close()

    # Return the path of the saved images
    return 'predicted_algae_concentration.png'


#dataset = pd.read_csv('water_potability_augmented_v2.csv')

#train(dataset)
