from flask import Flask, request, render_template
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

#################
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
dic = {}
uc_txt = []
pp = []

lista = ["Closing Cost Worksheet","LOAN ESTIMATE","Uniform Residential Loan Application","Form 3021",
        "MULTISTATE FIXED","CLOSING DISCLOSURE","appraisal software by a la mode","unclassified"]
###############
c=0
uc=0
cd=[]
a=[]
W2=[]
CAN=[]
URLNF=[]
DOT=[]
doc_pdf=[]
fnma=[]
counter=0
fixed=[]
assign=[]
paatalo=[]
data1={}
data2={}
data3={}
start_time = time.time()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" ##only for windows
app = Flask(__name__)  ###give me a web application
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0     #not classified doc open a file and appen at the last
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def process_images( prefix, suffix, out_fname,a):  ##images to pdf
    images = []
    for i in a:
        fname = prefix + str(i) + suffix
        # Load and process the image
        im = Image.open(fname)
        if im.mode == "RGBA":
            im = im.convert("RGB")
        images.append(im)
    images[0].save(out_fname, save_all = True, quality=100, append_images = images[1:])  #### image[0] sart
    print("pdf Created")

def close_range(el, it):
    while True:
        el1 = next(it, None)
        if el1 != el + 1:
            return el, el1
        el = el1

def compress_ranges(seq):  ##take a list like [1,2,3,4,9,10] cd = 1234 cd2 9,10
    iterator = iter(seq)
    left = next(iterator, None)
    while left is not None:
        right, left1 = close_range(left, iterator)
        yield [left, right]
        left = left1

st_time = time.time()
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/uploaded", methods=['POST'])
def uploaded():
    global assign
    global fixed
    global cd
    global CAN

    cd.clear()
    CAN.clear()
    W2.clear()
    URLNF.clear()
    DOT.clear()
    folder = './static/fnma'
    i=0
    dele=[]
    while i <len(fixed):
        dele=str(fixed[i])+".jpg"
        i=i+1
    for filename in os.listdir(folder):
        print(filename)
        file_path = os.path.join(folder, filename)
        try:
            if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename not in dele:
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    data=[]
    doc=[]
    fnma.clear()
    paatalo.clear()
    target = os.path.join('./uploads')
    ##print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        ##print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        ##print("Accept incoming file:", filename)
        ##print(destination)
        file.save(destination)   #i made change here
        if ".pdf" in filename:
            import pytesseract
            from PIL import Image
            x='./uploads/{}'.format(filename)
            pages = convert_from_path(x)
            print("--- %s seconds converted ---" % (time.time() - start_time))
            for i, im in enumerate(pages):
                im.save("./static/images/{}.jpg".format(i+1))
            print("--- %s seconds After Naming images ---" % (time.time() - start_time))
            print("images done")
            pdf=PdfFileReader(request.files['file'])
            print(pdf.getNumPages())
            counter=0
            i=0
            global pp
            global c
            global uc
            CCW.clear()
            LE.clear()
            GFE.clear()
            URLA.clear()
            F3021.clear()
            MF.clear()
            CD.clear()
            APP.clear()
            a.clear()
            unc.clear()
            dic.clear()
            uc_txt.clear()
            pp.clear()
            dic.clear()
            unc.clear()
            for i in range(pdf.getNumPages()):
                i=i+1
                print(i)
                result = ''
                image = cv2.imread('./static/images/{}.jpg'.format(i))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                crop = gray[1950:2180,10:1700].copy()
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
                        image = Image.open('./static/images/{}.jpg'.format(i))
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
                    image = Image.open('./static/images/{}.jpg'.format(i))
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
                    out_fname = "./static/pdf/{0} {1}.pdf".format(nam,counter)
                    for z in range(x[0],x[1]+1):
                        a.append(z)
                    process_images(prefix, suffix, out_fname,a)
                    a.clear()
                    data.append(str(x[0])+".jpg")
                    doc.append("pdf/{0} {1}.pdf".format(nam,counter))



            print("count of classified is  {}".format(c))
            print("count uclassfied is {}".format(uc))
            print("data {}".format(data))

            return render_template('index.html', data=data,doc=doc)

@app.route("/View", methods=['POST'])
def View():
    return "heyy"

if __name__ == "__main__":
    app.run(debug=True)
