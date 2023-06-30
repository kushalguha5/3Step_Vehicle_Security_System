import face_recognition
#from gpiozero import LED
from time import sleep
#relay = LED(17)
#relay.off()
import cv2
import numpy as np
import serial
import time

arduino = serial.Serial('COM7')
arduino.baudrate=9600
arduino.bytesize=8
arduino.parity='N'
arduino.stopbits = 1
#arduino.open()
time.sleep(3)

# Demo of running face recognition on live video from webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a first picture and learn how to recognize it.
kushal_image = face_recognition.load_image_file("kushal.jpg")
kushal_face_encoding = face_recognition.face_encodings(kushal_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a third sample picture and learn how to recognize it.
sushmita_image = face_recognition.load_image_file("sushmita.jpeg")
sushmita_face_encoding = face_recognition.face_encodings(sushmita_image)[0]

# Load a fourth sample picture and learn how to recognize it.
shreya_image = face_recognition.load_image_file("shreya.jpeg")
shreya_face_encoding = face_recognition.face_encodings(shreya_image)[0]

# Load a fifth sample picture and learn how to recognize it.
poulami_image = face_recognition.load_image_file("poulami.jpeg")
poulami_face_encoding = face_recognition.face_encodings(poulami_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    kushal_face_encoding,
    biden_face_encoding,
    sushmita_face_encoding,
    shreya_face_encoding,
    poulami_face_encoding
]
known_face_names = [
    "Kushal Guha",
    "Joe Biden",
    "Sushmita Bhattacharjee",
    "Shreya Chakravarty",
    "Poulami Podder"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                 first_match_index = matches.index(True)
                 name = known_face_names[first_match_index]
                 print(name);
                 #relay.on()
                 arduino.write(b'1')
                 #arduino.close()
                 face_names.append(name)
                 break
                 
                 
     
            if False in matches:
                 print(name);
                 face_names.append(name)
                 
            
            # Or instead, use the known face with the smallest distance to the new face
            #face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            #best_match_index = np.argmin(face_distances)
            #if matches[best_match_index]:
                #name = known_face_names[best_match_index]

            #face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
