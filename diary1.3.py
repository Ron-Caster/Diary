import PySimpleGUI as sg
import speech_recognition as sr
from datetime import datetime
import re
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
 # Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")
 # Define the layout of the GUI
layout = [
    [sg.Text(f"Date: {current_date}")],
    [sg.Text("Enter your text:")],
    [sg.Multiline(key="-CONTENT-", size=(40, 10))],
    [sg.Button("Save"), sg.Button("Voice Input", button_color=("white", "green")), sg.Button("Auto Capitalize")]
]
 # Create the window with the layout
window = sg.Window("Text Editor", layout)
 # Loop through the events and values of the window
while True:
    event, values = window.read()
     # If the user closes the window, break the loop
    if event == sg.WINDOW_CLOSED:
        break
     # If the user clicks Save, save the content as a txt file
    if event == "Save":
        content = values["-CONTENT-"]
        file_name = current_date + ".txt"
        with open(file_name, "w") as f:
            f.write(content)
        sg.popup(f"The file has been saved as {file_name}")
     # If the user clicks Voice Input, start recording and update the content
    if event == "Voice Input":
        text = speech_to_text()
        if text:
            content = values["-CONTENT-"] + text
            window["-CONTENT-"].update(content)
     # If the user clicks Auto Capitalize, update the content with capitalized first letters,
    # add a space after punctuation marks, and add a full stop at the end of the last word
    if event == "Auto Capitalize":
        content = values["-CONTENT-"]
        content = re.sub(r"(?<=\w)([.,!?;])(?=\w)", r"\1 ", content)  # Add space after punctuation marks
        content = content.rstrip()  # Remove trailing whitespace
        if content[-1] not in [".", "!", "?"]:
            content += "."  # Add a full stop at the end if absent
        sentences = re.split(r'(?<=[.!?;])\s*', content)
        capitalized_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                capitalized_sentences.append(sentence.capitalize())
        content = " ".join(capitalized_sentences)
        window["-CONTENT-"].update(content)
 # Close the window
window.close()