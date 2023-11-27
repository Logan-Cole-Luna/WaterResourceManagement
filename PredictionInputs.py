import tkinter
from tkinter import Toplevel, Label, Button
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import shutil
import os
from PredictionModel import train

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
def open_prediction_window(User_Input, root_tk):
    prediction_window = Toplevel(root_tk)
    prediction_window.title("Prediction Results")

    if User_Input == 1:
        # Add a button to the main window to open the upload dialog
        upload_csv_button = tkinter.Button(root_tk, text="Upload and Display CSV",  command=lambda: upload_and_display_csv(prediction_window))
        upload_csv_button.pack()

    elif User_Input == 2:
        dataset = pd.read_csv('water_potability_augmented_v2.csv')
        # Load and display the prediction image
        image_path = train(dataset)
        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img)
        panel = Label(prediction_window, image=img)
        panel.image = img
        panel.pack()


def display_csv(root_tk):
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

def open_data_window(root_tk):
    data_window = tkinter.Toplevel(root_tk)
    data_window.title("Data Input Window")
    # Add username label and entry
    answer_label = tkinter.Label(data_window,
                                 text="Would you like to give a Dataset\n for Predictive Analysis (Yes/No):")
    answer_label.pack()

    # Create a frame for buttons
    button_frame = tkinter.Frame(data_window)
    button_frame.pack()

    yes_button = tkinter.Button(button_frame, text="Yes", command=lambda: open_prediction_window(1, root_tk))
    yes_button.pack(side=tkinter.LEFT)
    no_button = tkinter.Button(button_frame, text="No", command=lambda: open_prediction_window(2, root_tk))
    no_button.pack(side=tkinter.RIGHT)

    info_label = tkinter.Label(data_window,
                               text="If no, an example dataset will be used,\n if yes, \na dataset must be formatted similar \nto the dataset linked below:")
    info_label.pack()
    button_frame_low = tkinter.Frame(data_window)
    button_frame_low.pack()
    link_button = tkinter.Button(button_frame_low, text="Example Dataset", command=display_csv(root_tk))
    link_button.pack()
