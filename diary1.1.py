# This is a python code to create a program to enter daily diary and save it as .txt file
# The program also has a basic GUI using PySimpleGUI
# The program gets the current date from the system and asks the user for the content of the diary entry
# The program then creates a file with the current date as the name and writes the content to it
# The program also checks if the file already exists and asks the user if they want to overwrite it or append to it
 # Import the os module to check if the file exists
import os
 # Import PySimpleGUI to create the GUI
import PySimpleGUI as sg
 # Import the datetime module to get the current date
from datetime import datetime
 # Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")
 # Define the layout of the GUI
layout = [
    [sg.Text(f"Date: {current_date}")],
    [sg.Text("Enter your diary entry:")],
    [sg.Multiline(key="-CONTENT-", size=(40, 10))],
    [sg.Button("Save"), sg.Button("Exit")]
]
 # Create the window with the layout
window = sg.Window("Diary", layout)
 # Loop through the events and values of the window
while True:
    event, values = window.read()
    # If the user clicks Exit or closes the window, break the loop
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # If the user clicks Save, get the content from the values
    if event == "Save":
        content = values["-CONTENT-"]
        # Create the file name with the current date and .txt extension
        file_name = current_date + ".txt"
        # Check if the file already exists
        if os.path.exists(file_name):
            # Ask the user if they want to overwrite or append
            choice = sg.popup_yes_no("The file already exists. Do you want to overwrite (Yes) or append (No)?")
            # If the user chooses to overwrite
            if choice == "Yes":
                # Open the file in write mode and write the content
                with open(file_name, "w") as f:
                    f.write(content)
                # Show a confirmation message
                sg.popup("The file has been overwritten.")
            # If the user chooses to append
            elif choice == "No":
                # Open the file in append mode and write the content
                with open(file_name, "a") as f:
                    f.write("\n" + content)
                # Show a confirmation message
                sg.popup("The file has been appended.")
            # If the user cancels, do nothing
            else:
                pass
        # If the file does not exist
        else:
            # Open the file in write mode and write the content
            with open(file_name, "w") as f:
                f.write(content)
            # Show a confirmation message
            sg.popup("The file has been created.")
 # Close the window
window.close()