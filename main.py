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
        upload_csv_button = tkinter.Button(root_tk, text="Upload and Display CSV", command=upload_and_display_csv(prediction_window))
        upload_csv_button.pack()

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


def open_login_window():
    # Function to open a new window with the prediction image
    def print_credentials():
        username = username_entry.get()
        password = password_entry.get()
        print("Username:", username)
        print("Password:", password)
        login_window.destroy()
        login_button_map.pack_forget()  # Remove the login button
        report_button = tkinter.Button(blank_space, text="Report", command=open_report_window)
        report_button.pack(side="left")
        logout_button = tkinter.Button(blank_space, text="Log Out", command=open_report_window)
        logout_button.pack(side="left")
        user_reports_button = tkinter.Button(blank_space, text="Your Reports", command=open_report_window)
        user_reports_button.pack(side="left")
        global_reports_button = tkinter.Button(blank_space, text="Global Reports", command=open_report_window)
        global_reports_button.pack(side="left")
        data_button_pack = tkinter.Button(blank_space, text="Predictive Model", command=open_data_window)
        data_button_pack.pack(side="right")

        # Function to open a new window with the prediction images

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

root_tk = tkinter.Tk()
root_tk.geometry(f"{600}x420")
root_tk.title("Water Quality Management")

# create map widget
map_widget = TkinterMapView(root_tk, width=600, height=400, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# google normal tile server
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

# Get current location
g = geocoder.ip('me')
current_location = g.latlng

# Set the map to the current location
if current_location:
    map_widget.set_address(f"{current_location[0]}, {current_location[1]}", marker=True)

# Create a blank space at the bottom
blank_space = tkinter.Frame(root_tk, height=20, bg="white")
blank_space.pack(fill="both", expand=True, side="bottom")

# Add a "Login" button to the blank space
login_button_map = tkinter.Button(blank_space, text="Login", command=open_login_window)
login_button_map.pack(side="left")



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
