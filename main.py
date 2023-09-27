import tkinter as tk
import geocoder

def button_click(label_text):
    # Use the geocoder library to get the user's location
    g = geocoder.ip('me')
    user_location = g.latlng

    label.config(text=f"You selected {label_text}!\nYour location: {user_location}")
    # Hide the buttons after a selection
    good_water_button.grid_forget()
    okay_water_button.grid_forget()
    bad_water_button.grid_forget()

# Create the main window
window = tk.Tk()
window.title("Water Quality")

# Set a fixed window size
window.geometry("400x200")

# Create a label to display the selected option
label = tk.Label(window, text="", font=("Arial", 16))
label.grid(row=0, column=0, columnspan=3, pady=20)

# Create the three buttons
good_water_button = tk.Button(window, text="Good Water", command=lambda: button_click("Good Water"))
okay_water_button = tk.Button(window, text="Okay Water", command=lambda: button_click("Okay Water"))
bad_water_button = tk.Button(window, text="Bad Water", command=lambda: button_click("Bad Water"))

# Place the buttons in the grid
good_water_button.grid(row=0, column=1, padx=10, pady=10)
okay_water_button.grid(row=1, column=1, padx=10, pady=10)
bad_water_button.grid(row=2, column=1, padx=10, pady=10)

# Start the GUI event loop
window.mainloop()
