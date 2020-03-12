import json
from pdf2image import convert_from_path
import os, shutil
import os.path
from PIL import Image
import pytesseract
import cv2
import re
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
import numpy
import time
import image
import copy
import csv
from csv import writer
import time
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

###taking the page count
pdf_dir = r'C:\zeta\flaskV8\uploads\Sample Set 3.pdf'
pages = convert_from_path(pdf_dir)
pdf=PdfFileReader(pdf_dir)
print(pdf.getNumPages())
for i, im in enumerate(pages):
    im.save(r"C:\zeta\sample\images3\{}.jpg".format(i+1))
print("##### pdf to images done ####")

## list of forms
lista = ["Closing Cost Worksheet","LOAN ESTIMATE","Uniform Residential Loan Application","Form 3021",
        "MULTISTATE FIXED","CLOSING DISCLOSURE","appraisal software by a la mode","unclassified"]

new_list = []
CCW= []
LE= []
GFE= []
URLA= []
F3021= []
MF= []
CD= []
APP= []
a = []
unc = []
counter=0
dic = {}
uc_txt = []
########pdf###########
def process_images( prefix, suffix, out_fname,a):
    images = []
    for i in a:
        fname = prefix + str(i) + suffix
        # Load and process the image
        im = Image.open(fname)
        if im.mode == "RGBA":
            im = im.convert("RGB")
        images.append(im)
    images[0].save(out_fname, save_all = True, quality=100, append_images = images[1:])
    print("pdf Created")

###Accessing the pages
def close_range(el, it):
    while True:
        el1 = next(it, None)
        if el1 != el + 1:
            return el, el1
        el = el1

def compress_ranges(seq):
    iterator = iter(seq)
    left = next(iterator, None)
    while left is not None:
        right, left1 = close_range(left, iterator)
        yield [left, right]
        left = left1
c=0
uc=0
#######classification begins########
start = time.time()
for i in range(pdf.getNumPages()):
    i=i+1
    print(i)
    result = ''
    image = cv2.imread('./images3/{}.jpg'.format(i))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    crop = gray[1950:2180,10:1700].copy()
    #cv2.imwrite(r'C:\Users\Admin\Downloads\Documents\Uniform Residential Loan Application.png',crop)
    test = pytesseract.image_to_string(crop)
    uc_txt.append(test)

    for l in range(len(lista)):
        if lista[l] in test:
            path = os.path.join("./directoies/",lista[l])
            if(os.path.isdir(path)):
                print("{} Already exists".format(lista[l]))
            else:
                path = os.path.join("./directoies/",lista[l])
                os.mkdir(path,mode=755)
            print("path of {} is {}".format(lista[l],path))

            print("{} found".format(lista[l]))
            image = Image.open('./images3/{}.jpg'.format(i))
            img = image.convert('RGB')
            img.save("{}/{}.jpg".format(path,i))

##########Appending the respective pages to the list #############
            if(lista[l]=="Closing Cost Worksheet"):
                CCW.append(i)
                dic["Closing Cost Worksheet"]=CCW
                c+=1
                break
            elif(lista[l]=="LOAN ESTIMATE"):
                LE.append(i)
                dic["LOAN ESTIMATE"] = LE
                c+=1
                break
            elif(lista[l]=="Uniform Residential Loan Application"):
                URLA.append(i)
                dic["Uniform Residential Loan Application"]=URLA
                c+=1
                break
            elif(lista[l]=="Form 3021"):
                F3021.append(i)
                dic["Form 3021"] = F3021
                c+=1
                break
            elif(lista[l]=="MULTISTATE FIXED"):
                MF.append(i)
                dic["MULTISTATE FIXED"] = MF
                c+=1
                break
            elif(lista[l]=="CLOSING DISCLOSURE"):
                CD.append(i)
                dic["CLOSING DISCLOSURE"] = CD
                c+=1
                break
            elif(lista[l]=="appraisal software by a la mode"):
                APP.append(i)
                dic["appraisal software by a la mode"] = APP
                c+=1
                break

    else:
        path = os.path.join("./directoies/",lista[l])
        if(os.path.isdir(path)):
            print("{} Already exists".format(lista[l]))
        else:
            path = os.path.join("./directoies/",lista[l])
            os.mkdir(path,mode=755)
        print("path of {} is {}".format( lista[l],path))

        print("{} found".format(lista[l]))
        image = Image.open('./images3/{}.jpg'.format(i))
        img = image.convert('RGB')
        img.save("{}/{}.jpg".format(path,i))

        if(("Closing Cost Worksheet"and "LOAN ESTIMATE"and "Uniform Residential Loan Application" and "Form 3021" and "MULTISTATE FIXED" and "CLOSING DISCLOSURE" and "appraisal software by a la mode") not in uc_txt):
            uc+=1
            unc.append(i)
            dic["unclassified"] = unc



#######Assembling the images and converting to pdf ###########
for nam,pag in dic.items():
    pp=list(compress_ranges(pag))
    counter=0
    for x in pp:
        counter=counter+1
        pre_path = os.path.join("./directoies/",nam)
        prefix = ("{}/".format(pre_path))
        suffix=".jpg"
        out_fname = "./pdf/{0} {1}.pdf".format(nam,counter)
        for z in range(x[0],x[1]+1):
            a.append(z)
        process_images(prefix, suffix, out_fname,a)
        a.clear()


print("count of classified is  {}".format(c))
print("count uclassfied is {}".format(uc))
