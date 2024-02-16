import cv2
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class DataCollectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Collection App")

        self.name_label = tk.Label(root, text="Enter Your Name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.choose_option_label = tk.Label(root, text="Choose an option:")
        self.choose_option_label.pack()

        self.webcam_button = tk.Button(root, text="Use Webcam", command=self.capture_from_webcam)
        self.webcam_button.pack()

        self.gallery_button = tk.Button(root, text="Choose from Gallery", command=self.choose_from_gallery)
        self.gallery_button.pack()
        
        self.save_button = tk.Button(root, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack()

        self.image_path = None

    def capture_from_webcam(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            cv2.imshow("Webcam", frame)

            key = cv2.waitKey(1)
            if key == 13:  # Enter key
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(faces) > 0:
                    name = self.name_entry.get()

                    # Create folder if not exists
                    folder_path = "student_data"
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    self.image_path = os.path.join(folder_path, f"{name}_webcam_capture.jpg")
                    cv2.imwrite(self.image_path, frame)
                    self.save_button.config(state=tk.NORMAL)  # Enable the Save button
                    break
                else:
                    print("No face detected. Please try again.")

            elif key == ord('q'):  # 'q' key to stop webcam and save
                break

        cap.release()
        cv2.destroyAllWindows()

    def save_image(self):
        if self.image_path:
            name = self.name_entry.get()

            folder_path = "student_data"
            new_image_path = os.path.join(folder_path, f"{name}_webcam_capture_saved.jpg")

            # Rename the file and save
            os.rename(self.image_path, new_image_path)
            self.image_path = None
            self.save_button.config(state=tk.DISABLED)  # Disable the Save button

    def choose_from_gallery(self):
        name = self.name_entry.get()

        # Create folder if not exists
        folder_path = "student_data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = filedialog.askopenfilename(title="Select a picture", filetypes=[("Image files", "*.jpg;*.png")])

        if file_path:
            image = Image.open(file_path)
            image.show()
            self.image_path = os.path.join(folder_path, f"{name}_gallery_picture.jpg")
            image.save(self.image_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = DataCollectionApp(root)
    root.mainloop()
