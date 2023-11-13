# https://www.kaggle.com/code/mrtoddy/kagglepredic
# Time Series Forecasting
import pandas as pd
from sklearn.linear_model import LinearRegression

def train():
    import matplotlib.pyplot as plt
    # Load the dataset based off of user input
    # if input == 1
    # dataset = input
    # if input == 2
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
    #plt.show()

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
    #plt.show()


    UserDataset = pd.read_csv('water_potability_augmented_example.csv')
    UserData = UserDataset.drop(['Algae Concentration', 'Date'], axis=1)
    predict = regression.predict(UserData)

    # Plot Actual vs. Predicted
    plt.figure(figsize=(14, 6))
    plt.plot(UserDataset['Date'], predict, label='Predicted Values', color='red', linestyle='dashed')
    plt.title('Predicted Algae Concentration')
    plt.xlabel('Date')
    plt.ylabel('Algae Concentration')
    # Save the Predicted Algae Concentration plot
    plt.savefig('predicted_algae_concentration.png')
    plt.close()

    # Return the path of the saved images
    return ['predicted_algae_concentration.png']


# Capture the output images from the training function
output_images = train()

train()
