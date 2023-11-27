import json
#from statistics import LinearRegression
#from PredictionModel import train
#from PredictionInputs import upload_and_display_csv, open_prediction_window, display_csv, open_data_window
import tkinter
from tkintermapview import TkinterMapView
import geocoder
from tkinter import Toplevel, Label, Button
from PIL import Image, ImageTk
from PredictionModel import train
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import shutil
import os
from sklearn.linear_model import LinearRegression


# Assume that the train function returns a list of image file paths
def train(dataset):
    import matplotlib.pyplot as plt
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

def upload_and_display_csv(prediction_window):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if not file_path:  # User has cancelled the file open dialog
        return

    # Define the new name for the CSV file
    new_name = "uploaded_file.csv"
    # Get the directory where the script is running
    script_dir = os.path.dirname(os.path.abspath(__file__))
    new_path = os.path.join(script_dir, new_name)

    # Copy the file to the new location with the new name
    shutil.copy(file_path, new_path)

    # Load and display the prediction image
    image_path = train(new_path)
    img = Image.open(image_path)
    img = img.resize((400, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(prediction_window, image=img)
    panel.image = img
    panel.pack()


# Assume that the train function returns a list of image file paths
def open_prediction_window(User_Input):
    data_window = Toplevel(root_tk)
    data_window.geometry("300x200")
    prediction_window = Toplevel(data_window)
    prediction_window.title("Prediction Results")

    if User_Input == 1:
        # Add a button to the main window to open the upload dialog
        upload_csv_button = tkinter.Button(root_tk, text="Upload and Display CSV",
                                           command=lambda: upload_and_display_csv(prediction_window))
        upload_csv_button.pack()

    elif User_Input == 2:
        dataset = pd.read_csv('water_potability_augmented_v2.csv')
        # Load and display the prediction image
        image_path = train(dataset)
        img = Image.open(image_path)
        img = img.resize((400, 250), Image.ANTIALIAS)
        #img = ImageTk.PhotoImage(img)
        #panel = Label(prediction_window, image=img)
        #panel.image = img
        #panel.pack()
        global img_reference
        img_reference = ImageTk.PhotoImage(img)

        panel = Label(prediction_window, image=img_reference)
        panel.pack()


def display_csv():
    # Create a new Toplevel window
    csv_window = tkinter.Toplevel(root_tk)
    csv_window.title("CSV Display")
    csv_window.geometry("600x400")

    # Read the CSV file using pandas
    df = pd.read_csv('water_potability_augmented_v2.csv')

    # Create a Treeview widget
    tree = ttk.Treeview(csv_window)

    # Define our columns
    tree['columns'] = list(df.columns)

    # Format our columns
    for column in tree['columns']:
        tree.column(column, anchor=tkinter.W, width=120)
        tree.heading(column, text=column, anchor=tkinter.W)

    # Add data to the treeview
    for index, row in df.iterrows():
        tree.insert("", tkinter.END, values=list(row))

    # Pack the treeview finally
    tree.pack(expand=True, fill='both')

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(csv_window, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')


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
        data_button_pack.pack_forget()
        map_widget.delete_all_marker()

        # Display the login button
        login_button_map.pack()

    report_button = tkinter.Button(blank_space, text="Report", command=open_report_window)
    data_button_pack = tkinter.Button(blank_space, text="Predictive Model", command=open_data_window)
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
    report_window.geometry("275x320")

    # Create labels and entries for each parameter
    parameters = [
        ("pH:", "ph"),
        ("Hardness:", "hardness"),
        ("Solids:", "solids"),
        ("Chloramines:", "chloramines"),
        ("Sulfate:", "sulfate"),
        ("Conductivity:", "conductivity"),
        ("Organic Carbon:", "organic"),
        ("Trihalomethanes:", "trihalomethanes"),
        ("Turbidity:", "turbidity"),
    ]

    for i, (label_text, entry_name) in enumerate(parameters):
        label = tkinter.Label(report_window, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5)

        entry = tkinter.Entry(report_window)
        entry.grid(row=i, column=1, padx=5, pady=5)

    # Create a submit button that saves the data to a file
    submit_button = tkinter.Button(report_window, text="Submit", command=lambda: save_data(username))
    submit_button.grid(row=len(parameters), column=0, columnspan=2, padx=5, pady=5)

def diagnosis():
    perfectPara = [7, 1, 1, 4, 250, 400, 25, 1, 0.1]
    maxPara = [6.5, 500, 500, 100, 10000, 1000, 100, 100, 5]
    
    inputs = [float(value) for value in data]
    respct = 0

    for i in range(len(perfectPara)):
    # If i is on pH
        if i == 0:
            respct += 100 - (((inputs[i] - perfectPara[i])) / perfectPara[i]) * 100
        else:
            # If input is between ideal and max limit. Finds percent to be subtracted
            if perfectPara[i] < inputs[i] < maxPara[i]:
                respct += 100 - ((inputs[i] / (maxPara[i] - perfectPara[i]) * 100))
            # If input better than ideal. Considering still ideal
            elif inputs[i] < perfectPara[i] and i != 0:
                respct += 100
            # If input worse than max limit. Auto 0
            elif inputs[i] > maxPara[i]:
                respct += 0

    # Calculate the final adjusted percentage
    respct /= len(perfectPara)
        
    if respct < 68:
        result_text = "We recommend you do not drink this water. Click 'Report' below to report your findings to local water companies and agencies\n\n"
    elif 68 <= respct < 72:
        result_text = "Based on your entries, this water is on the verge of being unsafe for drinking. Use caution. Click 'Report' below to report your findings to local water companies and agencies\n\n"
    elif 72 <= respct < 85:
        result_text = "This water is safe for drinking. To improve quality, Click 'Report' below to report your findings to local water companies and agencies\n\n"
    elif 85 <= respct < 100:
        result_text = "This water is very safe to drink! Click 'Report' below to report your findings to local water companies and agencies"
    else:
        result_text = "Error in grading scale"

    # Create a new Tkinter window
    window = tkinter.Tk()
    window.title("Water Quality Diagnosis")

    # Create a text widget to display the results
    result_label = tkinter.Label(window, text=result_text, wraplength=400, justify="left")
    result_label.pack(padx=10, pady=10)
    close_button = tkinter.Button(window, text="Close", command=window.destroy)
    close_button.pack()
    def contact():
        # Destroy any existing windows
        window.destroy()

        # Create the new contact window
        contact_window = tkinter.Tk()
        contact_window.title("Contact")

        # Label at the top
        label = tkinter.Label(contact_window, text="Address concerns to local water quality companies and agencies")
        label.pack(pady=10)

        # Text box for multiline input
        text_box = tkinter.Text(contact_window, height=5, width=40)
        text_box.insert(tkinter.END, "Type Here")
        text_box.pack(pady=10)

        def submit():
            message = text_box.get("1.0", tkinter.END).strip()
            with open(f"chat_submissions.txt", "a") as file:
                # Write the data to the file, separated by commas
                file.write(",".join(data) + "\n" + message + "\n" + str(current_location) + "\n")
                contact_window.destroy()

        # Submit button
        submit_button = tkinter.Button(contact_window, text="Submit", command=submit)
        submit_button.pack(side=tkinter.LEFT, padx=10)

        # Cancel button
        cancel_button = tkinter.Button(contact_window, text="Cancel", command=contact_window.destroy)
        cancel_button.pack(side=tkinter.RIGHT, padx=10)

        # Run the Tkinter event loop
        contact_window.mainloop()

    contact_button = tkinter.Button(window, text="Contact Comapnies and Agencies", command=contact)
    contact_button.pack()
    

    
def save_data(username):
    # Get the values from the entries
    global data
    data = [entry.get() for entry in report_window.winfo_children() if isinstance(entry, tkinter.Entry)]

    # Open a file with the username as the name
    with open(f"USER_{username}.txt", "a") as file:
        # Write the data to the file, separated by commas
        file.write(",".join(data) + "\n" + str(current_location) + "\n")
    with open(f"global_reports.txt", "a") as file:
        # Write the data to the file, separated by commas
        file.write(",".join(data) + "\n" + str(current_location) + "\n")
    report_window.destroy()
    diagnosis()


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

    yes_button = tkinter.Button(button_frame, text="Yes", command=lambda: open_prediction_window(1))
    yes_button.pack(side=tkinter.LEFT)
    no_button = tkinter.Button(button_frame, text="No", command=lambda: open_prediction_window(2))
    no_button.pack(side=tkinter.RIGHT)

    info_label = tkinter.Label(data_window, text="If no, an example dataset will be used,\n if yes, \na dataset must be formatted similar \nto the dataset linked below:")
    info_label.pack()
    button_frame_low = tkinter.Frame(data_window)
    button_frame_low.pack()
    link_button = tkinter.Button(button_frame_low, text="Example Dataset", command=display_csv)
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

root_tk.mainloop()
