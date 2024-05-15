import cv2
import face_recognition
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Function to open the attendance folder
def open_attendance_folder():
    attendance_folder_path = r"C:\Users\HP\Desktop\smart attendance system\Attendance Folder"
    os.makedirs(attendance_folder_path, exist_ok=True)
    print(f"Attendance folder opened successfully at: {attendance_folder_path}")
    return attendance_folder_path

# Function to select the Excel file to save attendance
def select_attendance_file():
    root = tk.Tk()
    root.withdraw()
    attendance_file_path = filedialog.askopenfilename(title="Select Excel File to Save Attendance", filetypes=[("Excel Files", "*.xlsx")])
    if not attendance_file_path:
        print("No file selected. Exiting the program.")
        exit()
    print(f"Attendance will be saved in the selected Excel file: {attendance_file_path}")
    return attendance_file_path

# Function to load images from the student data folder
def load_images():
    path = r"C:\Users\HP\Desktop\smart attendance system\Student Data"
    images = []
    classNames = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if len(images) >= 100:
                break
            curImg = cv2.imread(os.path.join(root, file))
            images.append(curImg)
            classNames.append(os.path.splitext(file)[0])
    return images, classNames

# Function to find encodings of the images
def find_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

# Function to save attendance to the Excel file
def save_attendance(attendance_df, attendance_file_path, name, registration_number):
    try:
        new_row = pd.DataFrame({'NAME': [name], 'REGISTRATION NUMBER': [registration_number], 'ATTENDANCE': ['Present']})
        attendance_df = pd.concat([attendance_df, new_row], ignore_index=True)  
        attendance_df.to_excel(attendance_file_path, index=False)
        print("Attendance saved successfully.")
    except Exception as e:
        print(f"Error occurred while saving attendance: {str(e)}")

# Main function to capture video from webcam and recognize faces
def main():
    try:
        # Open the attendance folder
        attendance_folder_path = open_attendance_folder()

        # Select the Excel file to save attendance
        attendance_file_path = select_attendance_file()

        # Load images from the student data folder
        images, classNames = load_images()

        # Encode the training faces
        encoded_face_train = find_encodings(images)

        # Create a DataFrame to store attendance data
        attendance_data = {'NAME': [], 'REGISTRATION NUMBER': [], 'ATTENDANCE': []}
        attendance_df = pd.DataFrame(attendance_data)

        # Capture video from webcam
        cap = cv2.VideoCapture(0)
        while True:
            success, img = cap.read()
            if not success:
                print("Failed to capture frame")
                break
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            faces_in_frame = face_recognition.face_locations(imgS)
            encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
            
            # Compare faces in the frame with the training faces
            for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
                matches = face_recognition.compare_faces(encoded_face_train, encode_face)
                faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
                matchIndex = np.argmin(faceDist)
                accuracy = (1 - faceDist[matchIndex]) * 100  # Calculate accuracy as a percentage
                print(f"Accuracy: {accuracy:.2f}%")
                
                if matches[matchIndex]:
                    name = classNames[matchIndex].upper().lower()
                    registration_number = name.split('_')[1]  # Assuming registration number is part of the file name
                    save_attendance(attendance_df, attendance_file_path, name, registration_number)
                    
                    y1, x2, y2, x1 = faceloc
                    # since we scaled down by 4 times
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Display the resulting frame
            cv2.imshow('Webcam', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break

        # Release the VideoCapture object and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
