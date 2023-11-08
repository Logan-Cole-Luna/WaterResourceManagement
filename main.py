import tkinter
from tkintermapview import TkinterMapView
import geocoder
#from PredictionModel import train

def open_login_window():
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
    yes_button = tkinter.Button(button_frame, text="Yes")
    yes_button.pack()

    no_button = tkinter.Button(button_frame, text="No")
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
