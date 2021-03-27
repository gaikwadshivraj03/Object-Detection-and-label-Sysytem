from django.shortcuts import render
import os
import csv
from django.http import HttpResponse
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import Image
import io

import lxml
import cv2
import base64

import shutil
from datetime import date
# Create your views here.
from .models import ObjectDetection, ObjCordinates
def index(request):
    return render(request,"index.html")
def uploadfiles(request):
    msg = []
    if request.method=="POST":
        if not request.FILES:
            msg.append("add files first")
            return render(request, 'index.html', {'msg': msg})
        pic=request.FILES['imgfile']
        xmlfile=request.FILES['xmlfile']
        if str(pic).lower().split('.')[1] in ['png', 'jpg', 'jpeg'] and str(xmlfile).lower().split('.')[1] !='xml':
            msg.append("pls make sure you upload proper image and xml file.")
            return render(request, 'index.html', {'msg': msg})
        if os.path.exists(os.getcwd()+'/media'):
            if str(pic) in os.listdir(os.getcwd()+'/media'):
                msg.append("Iamge already exist")
                return render(request, 'index.html', {'msg': msg})
        """
            saved image and xml file into ObjectDetection model
        """
        obj=ObjectDetection(Img=pic,xmlfile=xmlfile)#date=now.strftime("%Y-%m-%d")
        obj.save()
        # print(pic)
        getimage=ObjectDetection.objects.get(Img='images/'+str(pic))
        img_id=getimage.id
        filepath=getimage.xmlfile.name
        # path=os.path.join('E:\PycharmProjects\Baggageai\media\\',str(filepath))
        with open('media/'+str(filepath), 'r') as f:
            data = f.read()
        # print(data)
        Bs_data = BeautifulSoup(data, "lxml")
        b_unique = Bs_data.find_all('object')
        b_unique
        objects = {}
        l = []
        x = ""
        for i in b_unique:
            x = i.find('name').string
            for j in i.find('bndbox'):
                for k in j:
                    if k != '\n':
                        l.append(k)
                    # print(k)

            objects[x] = l
            l = []
            x = ""
        for key,val in objects.items():
            obj=ObjCordinates(img_id=img_id,obj_name=key,x_min=val[0],y_min=val[1],x_max=val[2],y_max=val[3])
            obj.save()
        cordinates=ObjCordinates.objects.filter(img_id=img_id)
        # print('cordinates',cordinates)
        window_name = 'Image'
        # print("path",Image.Img.url)
        image = cv2.imread(os.getcwd()+str(getimage.Img.url))#'E:/PycharmProjects/Baggageai/'
        # print(image)
        color = (0, 0, 255)
        thickness = 2
        fontScale = 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i in cordinates:
            # print("inloop")
            start_point = (i.x_min,i.y_min)
            end_point=(i.x_max,i.y_max)
            org=(i.x_min,i.y_min)
            # print(start_point,end_point,org)
            image = cv2.rectangle(image, start_point, end_point, color, thickness)
            # print("to",image)
            # return render(request, 'index.html', {'imgurl': image})
            image = cv2.putText(image, i.obj_name, org, font, fontScale,color, thickness, cv2.LINE_AA)
        # image = cv2.rotate(image, cv2.ROTATE_180)
        # image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)
        ret, frame_buff = cv2.imencode('.jpg', image)  # could be png, update html as well

        frame_b64 = base64.b64encode(frame_buff)
        image_64_decode = base64.b64decode(frame_b64)
        filename=str(getimage.Img.name)[7:]
        with open(os.getcwd()+"/media/"+filename, "wb") as fh:
            fh.write(image_64_decode)
        # shutil.move("E:/PycharmProjects/Baggageai/"+filename,  "E:/PycharmProjects/Baggageai/media/")
        #
        # print(filename,type(filename))
        # print(getimage.Img.url)
        getimage.objs_found=filename
        getimage.save()
        if len(msg)>0:
            return render(request,'index.html',{'msg':msg})
        if getimage.objs_found.url:
            return render(request,'index.html',{'imgurl':getimage.objs_found.url})#"/media/"+filename

    return render(request,'index.html')
def report(request):
    msg=[]
    if request.method=="POST":
        startdate=request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        fstdate=startdate
        snddate=enddate

        startdate=startdate.split('-')
        enddate=enddate.split('-')

        if int(startdate[0])==int(enddate[0]) and  int(startdate[1]) <=int(enddate[1]) and int(startdate[2]) <=int(enddate[2]):
            data=ObjectDetection.objects.filter(date__gte=fstdate, date__lte=snddate)
        elif int(startdate[0])<int(enddate[0]):
            data=ObjectDetection.objects.filter(date__gte=fstdate, date__lte=snddate)
        else:
            msg.append("Please enter a <strong>start</strong> date that is less than the <strong>end</strong> date you entered.")
        img_data={}
        fields = ['Iamge_name', 'Object_name', 'x_min', 'y_min','x_max','y_max']
        objs_data=[]
        for i in data:
            if i.id not in img_data:
                obj_data = ObjCordinates.objects.filter(img_id=i.id)
                for j in obj_data:

                    objs_data.append([str(i.Img.name).split('/')[1],j.obj_name,j.x_min,j.y_min,j.x_max,j.y_max,i.date])
                img_data[i.id]=objs_data
        filename=""
        x=0
        if os.path.exists(os.getcwd()+'/reports/'):
            x=len(os.listdir(os.getcwd()+'/reports'))
            print("x",x)
            filename='reports/'+str(x)+"report.csv"
        else:
            x = len(os.listdir(os.getcwd()+'/reports'))
            print("x", x)
            filename = 'reports/' + str(x) + "report.csv"
            # filename=f"reports/{x}report.csv"
        with open(filename,'w') as csvfile:
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(fields)

            # writing the data rows
            for key in img_data:
                for val in img_data[key]:
                    csvwriter.writerow(val)

    return render(request,'index.html')






# cv2.imshow(window_name, image)
# print(type(image))
# print("base64", frame_b64)

# with open(filename, "rb") as file:
#     img = base64.b64encode(file.read())
#
# img = Image.open(io.BytesIO(img))
# getimage.objs_found = img
# getimage.save()
# filename="E:/PycharmProjects/Baggageai/"+filename
# "E:\PycharmProjects\Baggageai\\"