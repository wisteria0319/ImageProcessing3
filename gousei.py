import cv2
import numpy as np

#conding: utf-8

from IPython.display import display, Image

capture=cv2.VideoCapture(1)
capture.set(3,1280)
capture.set(4,960)
capture.set(5,15)

while(True):
	ret, img = capture.read()

	cv2.imshow("frame", img)
	k=cv2.waitKey(1)	
	if k==27:
		cv2.imwrite('image.jpg',img)
		break

capture.release()
cv2.destroyAllWindows()

cv2.imshow("image1",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,th1 = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)


image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


areas = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 10000:
        epsilon = 0.1*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        areas.append(approx)

cv2.drawContours(img,areas,-1,(0,255,0),3)

cv2.imshow("image2",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

img = cv2.imread('image.jpg')

dst = []

pts1 = np.float32(areas[0])
pts2 = np.float32([[600,300],[600,0],[0,0],[0,300]])

M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M,(600,300))

cv2.imshow("dst",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()



import pyocr
from PIL import Image
tools = pyocr.get_available_tools()

if len(tools) == 0:
      print("No OCR tool found")
      sys.exit(1)
tool = tools[0]

txt = tool.image_to_string(Image.fromarray(dst), lang="eng")

print(txt)
file = open('test.txt', 'w')
file.write(txt)
file.close()
