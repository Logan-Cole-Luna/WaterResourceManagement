import tkinter
from tkintermapview import TkinterMapView
import geocoder
from tkinter import Toplevel, Label, Button
from PIL import Image, ImageTk
import pandas as pd
from PredictionModel import train


# Assume that the train function returns a list of image file paths
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

    UserDataset = pd.read_csv('water_potability_augmented_example.csv')
    UserData = UserDataset.drop(['Algae Concentration', 'Date'], axis=1)
    predict = regression.predict(UserData)

    # Plot Actual vs. Predicted
    plt.figure(figsize=(14, 6))
    plt.plot(UserDataset['Date'], predict, label='Predicted Values', color='red', linestyle='dashed')
    plt.title('Predicted Algae Concentration')
    plt.xlabel('Date')
    plt.ylabel('Algae Concentration')
    plt.show()
    # Save the Predicted Algae Concentration plot
    plt.savefig('predicted_algae_concentration.png')
    plt.close()

    # Return the path of the saved images
    return 'predicted_algae_concentration.png'

def open_login_window():
    # Function to open a new window with the prediction image
    def open_prediction_window():
        data_window = Toplevel(root_tk)
        data_window.title("Data Input Window")
        data_window.geometry("300x200")
        prediction_window = Toplevel(data_window)
        prediction_window.title("Prediction Results")

    if User_Input == 1:
        dataset = 1
    elif User_Input == 2:
        dataset = pd.read_csv('water_potability_augmented_v2.csv')

    # Load and display the prediction image
    image_path = train(dataset)
    img = Image.open(image_path)
    img = img.resize((400, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(prediction_window, image=img)
    panel.image = img
    panel.pack()

    # Button to open the prediction window


def open_login_window():
    # Function to open a new window with the prediction image
    def print_credentials():
        username = username_entry.get()
        password = password_entry.get()
        print("Username:", username)
        print("Password:", password)
        login_window.destroy()
        login_button_map.pack_forget()  # Remove the login button
        data_button_pack.pack(side="left")
        prediction_button.pack(side="left")
        global_reports_button.pack(side="left")
        prediction_button = Button(blank_space, text="Show Predictive Analysis", command=open_prediction_window)
        prediction_button.pack()
        data_button_pack = tkinter.Button(blank_space, text="Predictive Model", command=open_data_window)
        data_button_pack.pack(side="right")

    # Function to open a new window with the prediction images
    def log_out():
        # Hide the buttons related to the logged-in state
        report_button.pack_forget()
        logout_button.pack_forget()
        user_reports_button.pack_forget()
        global_reports_button.pack_forget()
        prediction_button.pack_forget()
        data_button_pack.pack_forget()

        # Display the login button
        login_button_map.pack()



    report_button = tkinter.Button(blank_space, text="Report", command=open_report_window)
    
    logout_button = tkinter.Button(blank_space, text="Log Out", command=log_out)
    
    user_reports_button = tkinter.Button(blank_space_top, text="Your Reports", command=your_reports)
    
    global_reports_button = tkinter.Button(blank_space_top, text="Global Reports", command=open_report_window)
    
    prediction_button = Button(blank_space, text="Show Predictive Analysis", command=open_prediction_window)
    data_button_pack = tkinter.Button(blank_space, text="Predictive Model", command=open_data_window)

    login_window = tkinter.Toplevel(root_tk)
    login_window.title("Login Window")
    login_window.geometry("300x200")

    # Add username label and entry
    username_label = tkinter.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tkinter.Entry(login_window)
    username_entry.pack()

    # Add password label and entry
    password_label = tkinter.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tkinter.Entry(login_window, show="*")
    password_entry.pack()

    # Create a frame for buttons
    button_frame = tkinter.Frame(login_window)
    button_frame.pack()

    # Add a "Login" button at the bottom
    login_button = tkinter.Button(button_frame, text="Login", command=print_credentials)
    login_button.pack()

def open_report_window():
    report_window = tkinter.Toplevel(root_tk)
    report_window.title("Water Report")
    report_window.geometry("500x500")

def open_data_window():
    data_window = tkinter.Toplevel(root_tk)
    data_window.title("Data Input Window")
    data_window.geometry("300x200")

    # Add username label and entry
    answer_label = tkinter.Label(data_window, text="Would you like to give a Dataset\n for Predictive Analysis (Yes/No):")
    answer_label.pack()

    # Add password label and entry
    # data_label = tkinter.Label(data_window, text="Password:")
    # data_label.pack()
    # data_label = tkinter.Entry(data_window, show="*")
    # data_label.pack()

    # Create a frame for buttons
    button_frame = tkinter.Frame(data_window)
    button_frame.pack()

    # Add a "Login" button at the bottom
    yes_button = tkinter.Button(button_frame, text="Yes", command=open_prediction_window(1))
    yes_button.pack()

    no_button = tkinter.Button(button_frame, text="No", command=open_prediction_window(2))
    no_button.pack()

    info_label = tkinter.Label(data_window, text="If no, an example dataset will be used,\n if yes, \na dataset my be formatted similar \nto the dataset linked below:")
    info_label.pack()
    button_frame_low = tkinter.Frame(data_window)
    button_frame_low.pack()
    link_button = tkinter.Button(button_frame_low, text="Example Dataset") #, command=print_credentials))
    link_button.pack()


root_tk = tkinter.Tk()
root_tk.geometry(f"{600}x420")
root_tk.title("Water Quality Management")

# create map widget
map_widget = TkinterMapView(root_tk, width=600, height=370, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# google normal tile server
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

# Get current location
g = geocoder.ip('me')
current_location = g.latlng

# Set the map to the current location
def your_reports():
    if current_location:
        map_widget.set_address(f"{current_location[0]}, {current_location[1]}", marker=True)

# Create a blank space at the bottom
blank_space = tkinter.Frame(root_tk, height=20, bg="white")
blank_space.pack(fill="both", expand=True, side="bottom")

# Create a blank space at the top
blank_space_top = tkinter.Frame(root_tk, height=20, bg="white")
blank_space_top.pack(fill="both", expand=True, side="top")

# Add a "Login" button to the blank space
login_button_map = tkinter.Button(blank_space, text="Login", command=open_login_window)
login_button_map.pack()



# Sample code to display an image, will take images from PredictionModel & display
'''
from PIL import ImageTk, Image
image1 = Image.open("<path/image_name>")
import tkinter
from tkinter import *
from PIL import Image, ImageTk
root = Tk()

# Create a photo image object of the image in the path
image1 = Image.open("<path/image_name>")
test = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=test)
label1.image = test

# Position image
label1.place(x=<x_coordinate>, y=<y_coordinate>)
root.mainloop()
'''

root_tk.mainloop()
