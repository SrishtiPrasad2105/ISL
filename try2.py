import tkinter as tk
from tkinter import Label, Text
import cv2
from PIL import Image, ImageTk
import numpy as np

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

        # Set up the video capture
        self.cap = cv2.VideoCapture(0)

        # Set up the camera feed label and place it in the middle of the left pane
        self.camera_label = Label(root)
        self.camera_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Set up the text display, styled and occupying the entire right pane
        self.text_display = Text(root, height=10, width=30, font=("Helvetica", 16), bg="#f0f0f0", fg="#333333", wrap=tk.WORD, padx=10, pady=10)
        self.text_display.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Center the camera label
        self.camera_label.grid_propagate(False)

        # Update the camera feed
        self.update_camera_feed()

    def update_camera_feed(self):
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
        # Here you would pass the frame to your ML model
        # For now, we'll use a placeholder that just returns "Hello"
        # Convert frame to the appropriate format if necessary

        # Predict the sign language gesture (placeholder)
        predicted_text = "Hello"  # This should be the output of your ML model

        # Display the predicted text
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, predicted_text)

    def __del__(self):
        self.cap.release()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    root.mainloop()
