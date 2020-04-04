import face_recognition
import numpy as np

#load the image to encode
newImg = face_recognition.load_image_file("/var/www/html/uploads/acarthew1.jpg")
newEncoding = face_recognition.face_encodings(newImg)
list = np.array(newEncoding).tolist()
backToArray = np.array(list)
print(backToArray)
