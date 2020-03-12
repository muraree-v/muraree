from PIL import Image
import pytesseract
import cv2
import sys
from pdf2image import convert_from_path
import os
import numpy

##Reading the image and saving the contents to file new.txt
# data = pytesseract.image_to_string('sample.PNG')
# with open('new.txt','w') as f:
#     f.write(data)


image = cv2.imread(r'C:\zeta\sample\images3\5.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("converted text")
# crop = gray[450:700,10:1400]   ###multistage/ fixed stage use sample image
# crop = gray[5:50,5:1500]   ###uniform residential loan applic use capture image
# crop = gray[100:700,300:500]   ###closing use sample image
# crop = gray[300:330,10:1400]   ###loan  use loan image
# crop = gray[575:620,10:1400]   ###Appraisal use appr image

crop = gray[520:590,200:1130]   ###loan estimate final through images/38.jpg

# crop = gray[1980:2180,10:1700]   ###good faith estimate through images3/2.jpg

# crop = gray[1980:2180,10:1700]   ###closing cost worksheet through images3/1.jpg

cv2.imwrite(r'C:\zeta\sample\sample_ans.PNG',crop)
sec = pytesseract.image_to_string(crop,lang='eng')
print(sec)
