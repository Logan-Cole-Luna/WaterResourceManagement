import tkinter
from tkintermapview import TkinterMapView
import geocoder
from tkinter import Toplevel, Label, Button
from PredictionInputs import open_data_window


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

    # Main login window configuration
    login_window = tkinter.Toplevel(root_tk)
    login_window.title("Login Window")
    login_window.state('zoomed')  # This will maximize the window

    # Center frame for login form
    center_frame = tkinter.Frame(login_window)
    center_frame.grid(row=1, column=1, sticky="nsew")

    # Configure weights for centering the frame
    login_window.grid_rowconfigure(0, weight=1)
    login_window.grid_rowconfigure(1, weight=0)
    login_window.grid_rowconfigure(2, weight=1)
    login_window.grid_columnconfigure(0, weight=1)
    login_window.grid_columnconfigure(1, weight=0)
    login_window.grid_columnconfigure(2, weight=1)

    # Login form setup
    username_label = tkinter.Label(center_frame, text="Username:")
    username_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    username_entry = tkinter.Entry(center_frame)
    username_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    password_label = tkinter.Label(center_frame, text="Password:")
    password_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    password_entry = tkinter.Entry(center_frame, show="*")
    password_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    login_button = tkinter.Button(center_frame, text="Login", command=print_credentials)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Bottom buttons configuration
    bottom_buttons_frame = tkinter.Frame(login_window)
    bottom_buttons_frame.grid(row=2, column=1, sticky="ew")

    report_button = tkinter.Button(bottom_buttons_frame, text="Report", command=open_report_window)
    report_button.pack(side='left', padx=10)

    data_button_pack = tkinter.Button(bottom_buttons_frame, text="Predictive Model",
                                      command=lambda: open_data_window(root_tk))
    data_button_pack.pack(side='left', padx=10)

    logout_button = tkinter.Button(bottom_buttons_frame, text="Log Out", command=log_out)
    logout_button.pack(side='right', padx=10)

    # Top buttons configuration
    top_buttons_frame = tkinter.Frame(login_window)
    top_buttons_frame.grid(row=0, column=1, sticky="ew")

    user_reports_button = tkinter.Button(top_buttons_frame, text="Your Reports", command=your_reports)
    user_reports_button.pack(side='left', padx=10)

    global_reports_button = tkinter.Button(top_buttons_frame, text="Global Reports", command=global_reports)
    global_reports_button.pack(side='left', padx=10)

    # Ensure the bottom and top frames fill their grid cell
    login_window.grid_rowconfigure(0, weight=1)
    login_window.grid_columnconfigure(1, weight=1)
    login_window.grid_rowconfigure(2, weight=1)

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
    result_text = ""

    if respct < 68:
        result_text += "We recommend you do not drink this water. Click 'Report' below to report your findings to local water companies and agencies\n\n"
    elif 68 <= respct < 72:
        result_text += "Based on your entries, this water is on the verge of being unsafe for drinking. Use caution. Click 'Report' below to report your findings to local water companies and agencies\n\n"
    elif 72 <= respct < 85:
        result_text += "This water is safe for drinking. To improve quality, Click 'Report' below to report your findings to local water companies and agencies\n\n"
    elif 85 <= respct < 100:
        result_text += "This water is very safe to drink! Click 'Report' below to report your findings to local water companies and agencies\n\n"
    else:
        result_text += "Error in grading scale\n\n"

    # ph
    if inputs[0] < 6.5:
        result_text += "You have low ph water which is more acidic than normal drinking water and can corrode a number of metallic materials.\n"
        result_text += "This can bring unwanted metals in your water system and cause neorvous and organ damage to people who drink low ph water.\n"
        result_text += "Sources can be from mine waste, acide generating soil and rock, industrial discharge, increase ammonium, and draining of wetlands or flood plains.\n"
        result_text += "To fix low ph water systems you will need something to raise to raise the ph level or such as neutralizing filters containing calcite or other mateirals.\n"
        result_text += "Contact your local water company and ask what solutions might be the right fit for your water needs.\n\n"
    elif inputs[0] > 8.5:
        result_text += "You have high ph water which is more alkaine than normal dirnking water which is not necessaruly dangerous above 8.5 but can cause some effects above ph levels 11.\n"
        result_text += "High ph can build up calcium and magnusim carbonate in your pipes. High ph don't have any studies for harming other than skin problems.\n"
        result_text += "Sources can be from industrail discharges, agricultrial runoff or manufacturing that use lye, lime, sodium hydroxide, or solvents.\n"
        result_text += "To fix high ph  water systems you will have to install a water filter or an acid injection system to lower the water ph.\n"
        result_text += "Contact your local water company and ask what solutions might be the right fit for your water needs.\n\n"
    else:
        result_text += "ph is in range of EPA freshwater standard.\n\n"

    # hardness
    if inputs[1] <= 100:
        result_text += "Your water is soft to moderately hard which no health related effectes but have a greater tendency to cause corrosion of pipes which can lead to the presence of certain heavy metals.\n"
        result_text += "There might be potential problem with your pipes and best to see if your pipes are non-corrosive and talk to a lcoal plumbing comapny if not.\n\n"
    elif inputs[1] > 100 and inputs[1] <= 120:
        result_text += "Your water hardness is moderately hard but no harmful effects have been attributed to hardness at this range.\n\n"
    elif inputs[1] > 120 and inputs[1] <= 180:
        result_text += "Your water hardness is hard but no harmful effects have been attributed to hardness at this range.\n\n"
    elif inputs[1] > 180 and inputs[1] <= 200:
        result_text += "Your water hardness is very hard but no harmful effects have been attributed to hardness at this range.\n\n"
    elif inputs[1] > 200:
        result_text += "Your water hardness is very hard and the hardness of water can lead to calicum magesium and mineral build up in the pipes.\n"
        result_text += "A solution is purchase a water softner to remove calcium, magnesium, and other minerals in your water."
        result_text += "Talk to your water company for options to your problem.\n\n"

    # Solids
    if inputs[2] <= 500:
        result_text += "Your water is in the desirable range of drinkable water and no changes to water recommended.\n\n"
    elif inputs[2] > 500 and inputs[2] <= 1000:
        result_text += "Your water is in the acceptable range of drinkable water but perfer to lower the TDS of your water.\n"
        result_text += "It's best to consider a filtration system and talk to a water company if there is concern for your water source.\n\n"
    elif inputs[2] > 1000 and inputs[2] <= 2000:
        result_text += "Your water is not in the acceptable range of drinkable water and it necessary to have a filter to drink the water.\n"
        result_text += "Talk to your water company for options of a filtration system as soon as possible.\n\n"
    else:
        result_text += "Your water is no longer in the rage for filters to properly filter water. Contact local authorities to notify the situation.\n\n"

    # Chloramines
    if inputs[3] <= 4:
        result_text += "Your water have safe levels of chloramines and no changes is need.\n\n"
    else:
        result_text += "Your water is not in safe levels of chloramines which can cause bodily harm in the form of irritation to eyes and nose and cause respiratory problems.\n"
        result_text += "A standard carbon water filter won't remove the chloramines and a reverse osmosis or a catalyic carbon filter is required to remove chloramines.\n"
        result_text += "Talk to your water company for options to your problem.\n\n"

    # Sulfate
    if inputs[4] <= 250:
        result_text += "Your water is in the safe range of sulfate and no changes is needed.\n\n"
    else:
        result_text += "Your water past the safe range of sulfate concentration which is harmful to health and piping.\n"
        result_text += "Health risk include diarrhea and dehydration. High concentration of sulfate is highly corrosive to copper piping.\n"
        result_text += "Sulfate naturally occur as water travels through soil and rock containing sulfate and can naturally lead to high levels of sulfate in water.\n"
        result_text += "Some ways to fix sulfate is to use reverse osmosis, distillation, anion exchange, and adsorptive media filtration.\n"
        result_text += "Talk to your water company for options to your problem.\n\n"

    # Conductivity
    if inputs[5] <= 400:
        result_text += "Your water is in the range of conductivity for drinking water and no changes is needed.\n\n"
    else:
        result_text += "Your water is beyond the range of conductivity for drinking water standards and can cause water to be very hard or/and be high alkalinity.\n"
        result_text += "Some ways to fix high conductivity are distillation, reverse osmosis, ion exchange, electrodialysis, and dilution.\n"
        result_text += "Talk to your water company for options to your problem.\n\n"

    # Organic Carbon
    if inputs[6] <= 2:
        result_text += "Your water is in the range of total organic carbon for treated water and require no changes.\n\n"
    elif inputs[6] <= 4:
        result_text += "Your water is in the rnage of total organic carbon for source water but if is treated water changes is needed for safe levels.\n"
        result_text += "You might have problems with your water treatmenet and need contact with your water company for options for your needs.\n\n"
    else:
        result_text += "Your water is out of range for total organic carbon for both treated and source water and can cause DBP.\n"
        result_text += "Which can cause health problem such as bladder cancer and reproductive issues for human beings.\n"
        result_text += "Solutions to total organic carbon are cogulation/flocculation, activated carbon, activated oxidation, ion exchange, reverse osmosis and nanofiltration.\n"
        result_text += "Talk to your water company for options to your problem.\n\n"

    # Trihalomethanes
    if inputs[7] <= 80:
        result_text += "Your water is in safe range of concentration of Trihalomethanes in drinking water.\n"
    else:
        result_text += "Your water is not in safe levels for drinking water and can cause a multitiude of cancers.\n"
        result_text += "Solutions to high levels of trihalomethanes are enchanced cogulation, carbon filters, reverse osmosis, and if the former do not aply boiling water can lower trihalomethanes.\n"
        result_text += "Talk to your water company for options to your problem.\n\n"

    # Turbidity
    if inputs[8] <= 5:
        result_text += "Your water turbidity levels are in safe range for drinking water and no changes needed.\n"
    else:
        result_text += "Your water turbidity levels are not in safe range for drinking water and high tubidity in drinking water incidenticate disease causeing organisms.\n"
        result_text += "Solution to turbidity are coagulation-flocculation, settling and decanting, backwashing filter, reverse osmosis filtration, and ultrafiltration.\n"
        result_text += "Talk to your water company for options to your problem.\n\n"

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
