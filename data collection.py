import cv2
import os

class DataCollectionApp:
    def __init__(self):
        self.image_path = None
        self.student_data_folder = "Student Data"
        self.data_file = "student_info.txt"

        if not os.path.exists(self.student_data_folder):
            os.makedirs(self.student_data_folder)

    def capture_front_faces(self, name, reg_number):
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        count = 0

        while count < 100:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face_img = gray[y:y + h, x:x + w]

                cv2.imshow("Front Face", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if face_img is not None:
                    cv2.imwrite(os.path.join(self.student_data_folder, f"{name}_{reg_number}_{count}.jpg"), face_img)
                    count += 1

        cap.release()
        cv2.destroyAllWindows()

        self.save_student_info(name, reg_number)

    def save_student_info(self, name, reg_number):
        with open(os.path.join(self.student_data_folder, self.data_file), 'a') as file:
            file.write(f"Name: {name}, Registration Number: {reg_number}\n")

if __name__ == "__main__":
    app = DataCollectionApp()
    name = input("Enter your name: ")
    reg_number = input("Enter your registration number: ")

    try:
        app.capture_front_faces(name, reg_number)
    except Exception as e:
        print(f"An error occurred: {e}")