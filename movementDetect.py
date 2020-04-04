import numpy as np
import cv2

vid = cv2.VideoCapture(0)
before = cv2.imread('before.jpg')
after = cv2.imread('after.jpg')

fgbg = cv2.createBackgroundSubtractorMOG2()

while(1):
 # frame = after
  #fgmask = fgbg.apply(after) 
  ret, frame = vid.read()
  fgmask = fgbg.apply(frame)
  median = cv2.medianBlur(fgmask,5)
 # bilateral = cv2.bilateralFilter(fgmask,15,75,75)


  cv2.imshow('fgmask',median)
  cv2.imshow('frame', fgmask)
 
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break

cap.release()
cv2.destroyAllWindows()
