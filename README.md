# Smart-Attendance-System-

cam.py:

This script uses the OpenCV library to capture video from the webcam and perform real-time face detection using the Haar Cascade face detection model.
Detected faces are highlighted with green rectangles.
The loop continues until the 'q' key is pressed, at which point it releases the webcam and closes the OpenCV windows.
datacollection.py:

This script defines a simple GUI application using tkinter for data collection.
Users can input their name and choose between capturing an image from the webcam or selecting an image from the gallery.
Images are saved in a "student_data" folder, and users can choose to save the captured image or loaded gallery image after inputting their name.
main.py:

This script uses face_recognition, a face recognition library built on top of dlib, to recognize faces in the webcam feed.
It loads pre-existing images from the "student_data" folder, encodes them, and compares the captured face encoding with the stored encodings.
If a match is found, it marks the attendance by writing the name, time, and date to a CSV file (Attendance.csv) and an Excel file (Attendance.xlsx).
The attendance data is displayed in real-time on the webcam feed with rectangles around recognized faces, and the person's name is shown along with the timestamp.
Overall, this project combines face detection, recognition, and data storage to create a rudimentary smart attendance system. It provides a foundation that could be expanded upon for more advanced features and functionality.
