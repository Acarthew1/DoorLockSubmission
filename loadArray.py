import face_recognition
from pymongo import MongoClient
import numpy as np
from pprint import pprint
import cv2


client = MongoClient("mongodb+srv://alex:DexterDog!123@doorlock-4pc1c.mongodb.net/test?retryWrites=true&w=majority")
db=client.test
collection = db.users

rawFaceEncodings = collection.find_one({"username": "acarthew1"})



AlexEncoding1 = np.asarray(rawFaceEncodings['encoding'])
#pprint(AlexEncoding1[0])

img = face_recognition.load_image_file('alex.jpg')

unknownEncoding = face_recognition.face_encodings(img)[0]
#pprint(unknownEncoding)
#AlexEncoding = face_recognition.face_encodings(img)[0]
AlexEncoding = AlexEncoding1[0]
#pprint(AlexEncoding)
results = face_recognition.compare_faces([AlexEncoding], unknownEncoding)

print(results)


