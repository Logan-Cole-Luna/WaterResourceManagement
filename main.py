import json
from statistics import LinearRegression
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

def open_prediction_window(User_Input):
    # Function to open a new window with the prediction image

    data_window = Toplevel(root_tk)
    data_window.title("Data Input Window")
    data_window.geometry("300x200")
    prediction_window.title("Prediction Results")
    prediction_window = Toplevel(data_window)

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
        global username
        username = username_entry.get()
        password = password_entry.get()
        print("Username:", username)
        print("Password:", password)
        login_window.destroy()
        login_button_map.pack_forget()  # Remove the login button
        logout_button.pack(side="right")
        report_button.pack(side="left")
        data_button_pack.pack(side="left")
        prediction_button.pack(side="left")
        user_reports_button.pack(side="left")
        global_reports_button.pack(side="left")
        data_button_pack.pack(side="left")
        return username


    # Function to open a new window with the prediction images
    def log_out():
        # Hide the buttons related to the logged-in state
        report_button.pack_forget()
        logout_button.pack_forget()
        user_reports_button.pack_forget()
        global_reports_button.pack_forget()
        prediction_button.pack_forget()
        data_button_pack.pack_forget()
        map_widget.delete_all_marker()

        # Display the login button
        login_button_map.pack()

    report_button = tkinter.Button(blank_space, text="Report", command=open_report_window)
    data_button_pack = tkinter.Button(blank_space, text="Predictive Model", command=open_data_window)
    prediction_button = Button(blank_space, text="Show Predictive Analysis", command=open_prediction_window)
    logout_button = tkinter.Button(blank_space, text="Log Out", command=log_out)
    user_reports_button = tkinter.Button(blank_space_top, text="Your Reports", command=your_reports)
    global_reports_button = tkinter.Button(blank_space_top, text="Global Reports", command=global_reports)


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
    global report_window
    report_window = tkinter.Toplevel(root_tk)
    report_window.title("Water Report")
    report_window.geometry("275x750")

    # Create labels and entries for each parameter
    parameters = [
        ("Temperature:", "temp"),
        ("pH:", "ph"),
        ("Dissolved Oxygen:", "do"),
        ("Rainfall:", "rainfall"),
        ("TDS:", "tds"),
        ("Chlorine Added:", "chlorine"),
        ("Turbidity:", "turbidity"),
        ("Algae Concentration:", "algae"),
        ("Nitrate:", "nitrate"),
        ("Phosphorus:", "phosphorus"),
        ("Microbial Counts:", "microbial"),
        ("BOD:", "bod"),
        ("Heavy Metals Index:", "heavy"),
        ("Hardness:", "hardness"),
        ("Solids:", "solids"),
        ("Chloramines:", "chloramines"),
        ("Sulfate:", "sulfate"),
        ("Conductivity:", "conductivity"),
        ("Organic Carbon:", "organic"),
        ("Trihalomethanes:", "trihalomethanes"),
        ("Potability:", "potability"),
        ("Algae Increase:", "algae_increase")
    ]

    for i, (label_text, entry_name) in enumerate(parameters):
        label = tkinter.Label(report_window, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)

        entry = tkinter.Entry(report_window)
        entry.grid(row=i, column=1, padx=5, pady=5)

    # Create a submit button that saves the data to a file
    submit_button = tkinter.Button(report_window, text="Submit", command=lambda: save_data(username))
    submit_button.grid(row=len(parameters), column=0, columnspan=2, padx=5, pady=5)

def save_data(username):
    # Get the values from the entries
    data = [entry.get() for entry in report_window.winfo_children() if isinstance(entry, tkinter.Entry)]

    # Open a file with the username as the name
    with open(f"USER_{username}.txt", "a") as file:
        # Write the data to the file, separated by commas
        file.write(",".join(data) + "\n" + str(current_location) + "\n")
    with open(f"global_reports.txt", "a") as file:
        # Write the data to the file, separated by commas
        file.write(",".join(data) + "\n" + str(current_location) + "\n")
    report_window.destroy()


def open_data_window():
    data_window = tkinter.Toplevel(root_tk)
    data_window.title("Data Input Window")
    data_window.geometry("300x200")

    # Add username label and entry
    answer_label = tkinter.Label(data_window, text="Would you like to give a Dataset\n for Predictive Analysis (Yes/No):")
    answer_label.pack()

    # Create a frame for buttons
    button_frame = tkinter.Frame(data_window)
    button_frame.pack()

    # Add a "Login" button at the bottom
    yes_button = tkinter.Button(button_frame, text="Yes")#, command=open_prediction_window(1))
    yes_button.pack()

    no_button = tkinter.Button(button_frame, text="No")#, command=open_prediction_window(2))
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
    # Construct the file name based on the given username
    file_name = f"USER_{username}.txt"
    map_widget.delete_all_marker()
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

            # Process the remaining lines (e.g., read and pin coordinates on the map)
            for index in range(1, len(lines), 2):
                coordinates_str = lines[index].strip()
                try:
                    # Parse the coordinates from the string
                    coordinates = eval(coordinates_str)

                    # Pin the coordinates on the map
                    map_widget.set_address(f"{coordinates[0]}, {coordinates[1]}", marker=True, text="Your Report")

                except (ValueError, IndexError) as e:
                    print(f"Error parsing coordinates in line {index + 1}: {e}")

    except FileNotFoundError:
        map_widget.delete_all_marker()
        print(f"File {file_name} not found.")

def global_reports():
    # Construct the file name based on the given username
    file_name = f"global_reports.txt"
    map_widget.delete_all_marker()
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

            # Process the remaining lines (e.g., read and pin coordinates on the map)
            for index in range(1, len(lines), 2):
                coordinates_str = lines[index].strip()
                try:
                    # Parse the coordinates from the string
                    coordinates = eval(coordinates_str)

                    # Pin the coordinates on the map
                    map_widget.set_address(f"{coordinates[0]}, {coordinates[1]}", marker=True, text="")

                except (ValueError, IndexError) as e:
                    print(f"Error parsing coordinates in line {index + 1}: {e}")

    except FileNotFoundError:
        map_widget.delete_all_marker()
        print(f"File {file_name} not found.")
    
    
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
