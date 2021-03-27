from django.db import models
# from datetime import datetime
from datetime import date

# Create your models here.
class ObjectDetection(models.Model):
    Img=models.ImageField(upload_to="images")
    xmlfile=models.FileField(upload_to="xmlfiles")
    objs_found=models.ImageField(upload_to="obj_found_imgs",blank=True)
    # now=datetime.now()default=now.strftime("%H:%M:%S")
    date=models.DateField(default=date.today)
    # time=models.CharField(max_length=50)
class ObjCordinates(models.Model):
    img_id=models.IntegerField(default=0)
    obj_name=models.CharField(max_length=50)
    x_min=models.IntegerField(default=0)
    y_min=models.IntegerField(default=0)
    x_max=models.IntegerField(default=0)
    y_max=models.IntegerField(default=0)

