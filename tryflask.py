from flask import Flask
import tkinter
from tkintermapview import TkinterMapView
import geocoder

app = Flask(__name__)

@app.route("/")
def home():



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

    root_tk.mainloop()
    return "Hello, World!"

@app.route("/login")
def login():
    return "login page"
    
if __name__ == "__main__":
    app.run(debug=True)