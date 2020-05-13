import face_recognition
from pymongo import MongoClient
import numpy as np
from pprint import pprint
import cv2


client = MongoClient("mongodb+srv://user:DexterDog!123@cluster0-da4vs.mongodb.net/test?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db=client.test
collection = db.users

name = "peter123"
log = {"name": name,
       "count": 3
       }
#print(log["count"])
myquery = { "username": "adcarthew1"}
newvalues = {"$push" :{"logs": log}}
#newVals = {"$set" : {"lastTime" : date}}
#newvals2 = {"$push" : {name : date}}
#obj = collection.update_one({"logs.name": name}, {"$inc": {"logs.count": 1}})

#collection.update_one({"logs.name": name}, {"$push" :{"logs.count": 1}})
collection.update_one(myquery, newvalues)

#rawFaceEncodings = collection.find_one({"username": "acarthew1"})

#TrustedList = rawFaceEncodings['TrustedUsers']
#for user in TrustedList:

 # print(user)


#AlexEncoding1 = np.asarray(rawFaceEncodings['encoding'])
#pprint(AlexEncoding1[0])

#img = face_recognition.load_image_file('alex.jpg')

#unknownEncoding = face_recognition.face_encodings(img)[0]
#pprint(unknownEncoding)
#AlexEncoding = face_recognition.face_encodings(img)[0]
#AlexEncoding = AlexEncoding1[0]
#pprint(AlexEncoding)
#results = face_recognition.compare_faces([AlexEncoding], unknownEncoding)
#
#print(results)


