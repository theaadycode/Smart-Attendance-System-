import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pandas as pd

path = r"C:\Users\HP\Desktop\project\smart attendance system\student_data"
images = []
classNames = []
mylist = os.listdir(path)

for cl in mylist:
    curImg = cv2.imread(os.path.join(path, cl))
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

encoded_face_train = findEncodings(images)

def markAttendance(name, df):
    now = datetime.now()
    time = now.strftime('%I:%M:%S:%p')
    date = now.strftime('%d-%B-%Y')

    new_entry = pd.DataFrame({'Name': [name], 'Time': [time], 'Date': [date]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv('Attendance.csv', index=False)
    df.to_excel('Attendance.xlsx', index=False)

attendance_file_csv = 'Attendance.csv'
attendance_file_excel = 'Attendance.xlsx'

# Check if files exist, create them if not
if not os.path.exists(attendance_file_csv):
    df = pd.DataFrame(columns=['Name', 'Time', 'Date'])
    df.to_csv(attendance_file_csv, index=False)

if not os.path.exists(attendance_file_excel):
    df = pd.DataFrame(columns=['Name', 'Time', 'Date'])
    df.to_excel(attendance_file_excel, index=False)

df = pd.read_csv(attendance_file_csv)

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

    for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
        matchIndex = np.argmin(faceDist)
        print(matchIndex)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper().lower()
            y1, x2, y2, x1 = faceloc
            # since we scaled down by 4 times
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name, df)

    cv2.imshow('webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
