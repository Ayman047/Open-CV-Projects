import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from lane_detection import process_frame

class LaneDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lane Detection GUI")

        # Set up video source
        self.video_source = r"C:\Users\MGIT\Desktop\project\RoadLane Detection\videoplayback.mp4"
        self.vid = cv2.VideoCapture(self.video_source)

        if not self.vid.isOpened():
            messagebox.showerror("Error", "Failed to open video file.")
            self.root.quit()

        # Create a canvas with the size of the video resolution
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()

        # Button to open a new video file
        self.btn_open = tk.Button(root, text="Open Video", width=10, command=self.open_video)
        self.btn_open.pack(padx=20, pady=5)

        # Start updating frames
        self.update()

    def open_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if file_path:
            self.vid.release()
            self.video_source = file_path
            self.vid = cv2.VideoCapture(self.video_source)
            
            if not self.vid.isOpened():
                messagebox.showerror("Error", "Failed to open video file.")
                return

            # Update canvas size to new video resolution
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.canvas.config(width=self.width, height=self.height)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            processed_frame = process_frame(frame)

            # Resize the frame if needed
            frame_resized = cv2.resize(processed_frame, (self.width, self.height))

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        else:
            # If no frame is returned, the video might have ended or failed to read
            self.vid.release()
            messagebox.showinfo("Info", "Video playback has ended.")
            return
        
        self.root.after(10, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = LaneDetectionApp(root)
    root.mainloop()
