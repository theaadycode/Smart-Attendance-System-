import os
import cv2

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder: {e}")

def capture_faces(folder_path, name, reg_number):
    face_cascade_path = r"C:\Users\HP\Desktop\smart attendance system\haarcascade files\haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    cap = cv2.VideoCapture(0)
    
    count = 0
    while count < 100:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Webcam Face Detection', frame)

        if cv2.waitKey(1) == 13:  # Enter key
            cv2.imwrite(f'{folder_path}/{name}_{reg_number}_{count}.jpg', frame)
            count += 1

        if count == 100:  # Exit webcam capture after 100 pictures
            break

    cap.release()
    cv2.destroyAllWindows()

    save_user_info(folder_path, name, reg_number)

def save_user_info(folder_path, name, reg_number):
    file_path = f'{folder_path}/student_info.txt'
    with open(file_path, 'a') as file:
        file.write(f"Name: {name}, Registration Number: {reg_number}\n")

if __name__ == "__main__":
    folder_path = 'Student Data'
    create_folder(folder_path)

    name = input("Enter your name: ")
    reg_number = input("Enter your registration number: ")

    print("Press 'Enter' key to capture 100 photos of your face.")
    input("Press Enter to start...")

    try:
        capture_faces(folder_path, name, reg_number)
    except Exception as e:
        print(f"An error occurred during face capture: {e}")