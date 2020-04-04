import face_recognition
import cv2
import numpy as np
#Load Video (replace with 0 for webcam)
video_capture = cv2.VideoCapture(0)

#load sample picture and learn how to recognise it
alex_image = face_recognition.load_image_file("alex.jpg")
alex_encoding = face_recognition.face_encodings(alex_image)[0]

andrew_image = face_recognition.load_image_file("Andy.jpg")
andrew_encoding = face_recognition.face_encodings(andrew_image)[0]

amanda_image = face_recognition.load_image_file("amanda.jpg")
amanda_encoding = face_recognition.face_encodings(amanda_image)[0]
#Create an array of known face encodings and their names
known_face_encodings = [
  alex_encoding,
  andrew_encoding,
  amanda_encoding
]
known_face_names = [
  "Alex Carthew",
  "Andrew Haste",
  "Amanda Carthew"
]

#Initialize some variables
face_locations = []
face_encodinggs = []
face_names = []
process_this_frame = True

while True:
  #Grab a frame from the video
  ret, frame = video_capture.read()

  #resize the frame to 1/4 of the size so it processes faster
  small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

  #Convert from BGR color that openCV uses to RGB
  rgb_small_frame = small_frame[:,:,::-1]

  #Only process every other frame of the video to save processing time
  if process_this_frame:
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
      #See if there is a match for a known face
      matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
      name = "unknown"

      #USe the known face with the smallest distance to the new face
      face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
      best_match_index = np.argmin(face_distances)
      if matches[best_match_index]:
        name = known_face_names[best_match_index]
	print("door Unlocked"
      face_names.append(name)

  process_this_frame = not process_this_frame

  #display the results
  for(top,right,bottom,left), name in zip(face_locations, face_names):
    #Scale back up to normal size
    top *=4
    bottom *=4
    left *= 4
    right *=4

    #Draw a box around the face
    cv2.rectangle(frame,(left,top), (right,bottom), (0,0,255),2)

    #Draw a label with the name below the face
    cv2.rectangle(frame,(left,bottom - 35),(right,bottom),(0,0,255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame,name,(left + 6,bottom - 6), font ,1.0,(255,255,255),1)

  cv2.imshow('Video', frame)

  if cv2.waitKey(1) == ord('q'):
      break
 #cv2.waitKey(0)


Video_capture.release()
cv2.destroyAllWindows()
