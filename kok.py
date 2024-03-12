import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
cap = cv2.VideoCapture(0)
while True:
    # Read the frame from the webcam
    ret, frame = cap.read()
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    # Apply a blur effect to the background
    blurred = cv2.GaussianBlur(frame, (99, 99), 0)
    # Process each detected face
    for (x, y, w, h) in faces:
        # Extract the region of interest (face) from the frame
        face = frame[y:y+h, x:x+w]
        
        # Replace the face region with the original, unblurred face
        blurred[y:y+h, x:x+w] = face
    # Display the result
    cv2.imshow('Background Blur with Visible Face', blurred)
    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()