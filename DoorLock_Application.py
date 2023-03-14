#Import List
import face_recognition
import cv2
import numpy as np
from pymongo import MongoClient
from pprint import pprint
import sys
import datetime



#Check username is given
if len(sys.argv) > 1:
  username = sys.argv[1]
else:
  print("Please specify a username")
  sys.exit()

#This section will connect to the database and load the encodings for the selected user
client = MongoClient("mongodb+srv://user:{passwordone!}@cluster0-da4vs.mongodb.net/test?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db=client.test
collection = db.users

#Get encodings for user
rawFaceEncodings = collection.find_one({"username": username})
#Get trusted user list
TrustedList = rawFaceEncodings['TrustedUsers']


#Convert to numpy array for face_recognition
Encoding1 = np.asarray(rawFaceEncodings['encoding'])

#Load Video (replace with 0 for webcam)
video_capture = cv2.VideoCapture(-1)
#video_capture = cv2.VideoCapture('/home/user/Desktop/VID_20200504_172231.mp4')
#Create a check Frames number
CheckFrames = 0
checkUnrec = 0
TotalUnlocks = 0
TotalUnrec = 0
#Create an array of known face encodings and their names
known_face_encodings = [
  Encoding1[0]
]
known_face_names = [
  username
]

for user in TrustedList:
  rawData = collection.find_one({"username": user});
  if rawData == None:
    continue
  else:
    RawEncoding = np.asarray(rawData['encoding'])
    encoding = RawEncoding[0]
    known_face_encodings.append(encoding)
    known_face_names.append(user)


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
      face_names.append(name)
      if name != "unknown":
        CheckFrames = CheckFrames + 1
        if CheckFrames >= 20:
          TotalUnlocks = TotalUnlocks + 1
          CheckFrames = 0
          date = datetime.datetime.now()
          date = date.strftime("%X")
          myquery = { "username": username}
          newvalues = {"$set" : {"unlocks": TotalUnlocks}}
          newVals = {"$set" : {"lastTime" : date}}
        #  newvals2 = {"$push" : {name : date}}

          collection.update_one(myquery, newvalues)
          collection.update_one(myquery, newVals)

          print ("DoorUnlocked")
      elif name == "unknown":
          checkUnrec = checkUnrec + 1
          if checkUnrec >= 20:
            checkUnrec = 0
            TotalUnrec = TotalUnrec + 1
            print("Unrecognised User at the door")
            myquery = { "username": username}
            newvalues = {"$set" : {"totalUnrec": TotalUnrec}}

            collection.update_one(myquery, newvalues)
           


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
