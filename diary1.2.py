# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 04:53:32 2023

@author: Hari Prezadu
"""

# Import the necessary libraries
import os
import PySimpleGUI as sg
from datetime import datetime
import speech_recognition as sr

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Define the layout of the GUI
layout = [
    [sg.Text(f"Date: {current_date}")],
    [sg.Text("Enter your diary entry:")],
    [sg.Multiline(key="-CONTENT-", size=(40, 10))],
    [sg.Button("Save"), sg.Button("Exit"), sg.Button("Voice Input")]
]

# Create the window with the layout
window = sg.Window("Diary", layout)

# Function to convert speech to text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        sg.popup("Speech recognition service is currently unavailable.")
        return ""

# Loop through the events and values of the window
while True:
    event, values = window.read()

    # If the user clicks Exit or closes the window, break the loop
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # If the user clicks Save, get the content from the values
    if event == "Save":
        content = values["-CONTENT-"]
        file_name = current_date + ".txt"

        if os.path.exists(file_name):
            choice = sg.popup_yes_no("The file already exists. Do you want to overwrite (Yes) or append (No)?")
            if choice == "Yes":
                with open(file_name, "w") as f:
                    f.write(content)
                sg.popup("The file has been overwritten.")
            elif choice == "No":
                with open(file_name, "a") as f:
                    f.write("\n" + content)
                sg.popup("The file has been appended.")
            else:
                pass
        else:
            with open(file_name, "w") as f:
                f.write(content)
            sg.popup("The file has been created.")

    # If the user clicks Voice Input, convert speech to text and update the content
    if event == "Voice Input":
        text = speech_to_text()
        if text:
            window["-CONTENT-"].update(values["-CONTENT-"] + text)

# Close the window
window.close()