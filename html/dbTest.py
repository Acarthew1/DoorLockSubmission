#!/usr/bin/env python
from pymongo import MongoClient
from pprint import pprint
import face_recognition
import os
import numpy as np

directory = "/var/www/html/uploads/"

for filename in os.listdir(directory):
  base = os.path.basename(filename)
  os.path.splitext(base)
  userName = os.path.splitext(base)[0]

  newImg = face_recognition.load_image_file(directory + filename)
  newEncoding = face_recognition.face_encodings(newImg)
  List = np.array(newEncoding).tolist()
#  os.remove(directory + filename)

#client = MongoClient('localhost', 27017)
client = MongoClient("mongodb+srv://user:DexterDog!123@cluster0-da4vs.mongodb.net/test?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")

db=client.test
collection = db.users

myquery = { "username": userName }
newvalues = {"$set" : {"encoding": List}}

collection.update_one(myquery, newvalues)









