import tkinter as tk
from tkinter import Label, Text, Button
import cv2
from PIL import Image, ImageTk
import numpy as np
import pyttsx3

class SignLanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Interpreter")
        
        # Set the size of the window
        self.root.geometry("1000x600")
        
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)

        # Set up the video capture
        self.cap = cv2.VideoCapture(0)
        
        # Set up the camera feed label
        self.camera_label = Label(root)
        self.camera_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Set up the text display
        self.text_display = Text(root, height=10, width=30, font=("Helvetica", 16), bg="#f0f0f0", fg="#333333", wrap=tk.WORD, padx=10, pady=10)
        self.text_display.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Add tags for text alignment
        self.text_display.tag_configure("left", justify='left')
        self.text_display.tag_configure("right", justify='right')
        
        # Set up the buttons
        self.start_button = Button(root, text="Start Translation", command=self.start_translation, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        self.start_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.speech_button = Button(root, text="Text-to-Speech", command=self.text_to_speech, font=("Helvetica", 14), bg="#2196F3", fg="white")
        self.speech_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Center the camera label
        self.camera_label.grid_propagate(False)
        
        # Variables to control the translation state
        self.translation_active = False
        
    def start_translation(self):
        if not self.translation_active:
            self.translation_active = True
            self.update_camera_feed()
        else:
            self.translation_active = False
        
    def update_camera_feed(self):
        if not self.translation_active:
            return
        
        _, frame = self.cap.read()
        
        # Convert the frame to RGB (Tkinter uses RGB, OpenCV uses BGR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize the frame to fit in the camera label
        frame_rgb = cv2.resize(frame_rgb, (480, 360))
        
        # Convert the image to a PhotoImage to display it in Tkinter
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img)
        
        # Update the image in the label
        self.camera_label.imgtk = img_tk
        self.camera_label.configure(image=img_tk)
        
        # Call the function to process the frame and update the text
        self.process_frame(frame)
        
        # Schedule the next update
        self.root.after(33, self.update_camera_feed)
        
    def process_frame(self, frame):
        # Placeholder for ML model integration
        predicted_text = "Hello"  # Replace this with your ML model's output
        
        # Display the predicted text (left-aligned)
        # self.text_display.insert(tk.END, f"Machine: {predicted_text}\n", "left")
        
    def user_input(self, text):
        # Display the user's input (right-aligned)
        self.text_display.insert(tk.END, f"You: {text}\n", "right")
        
    def text_to_speech(self):
        text = self.text_display.get(1.0, tk.END).strip()
        if text:
            self.engine.say(text)
            self.engine.runAndWait()

    def __del__(self):
        self.cap.release()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    
    # Example of user input for testing
    app.user_input("Hi there!")
    
    root.mainloop()
