import cv2

# Load the pre-trained Haar Cascade face detection model
face_cascade_path = (r"C:\Users\HP\Desktop\smart attendance system\haarcascade files\haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(face_cascade_path)

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Draw a square around each detected face and display accuracy
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        # You can use this confidence value to display the accuracy
        confidence = 100 - (100 * len(face_cascade.detectMultiScale(roi_gray)) / (w * h))

        # Draw the rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the accuracy below the square box
        cv2.putText(frame, f'Accuracy: {confidence:.2f}%', (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Webcam Face Detection', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
