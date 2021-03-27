# => Object Detection WebApp <=

1. How application works?
=> <p>You need to add image with (.png,jpg,jpeg) format if you want to add image with any different format so you need to make some changes to the line 28 in Baggaeai/objdetection/views.py file. 
Then need to pass a xml file which contains the object details like(object name, and cordinates to locate object in the image, etc.) if you pass a wrong files then error will be shown.</p>


2.How to generate report?
=>click on generate report button -> pass the start date and end date. So that you get the report for that time period about Iamge and the object that is found inside image. 
  
3.Install require Libraries/Packages
=> open terminal in project folder and run this command pip(if you mention version) install -r requirements.txt

4.How to run Program file.
=>open terminal in project folder and run this commands
i) python manage.py makemigrations
ii) python manage.py migrate
iii) python(if you mention version) manage.py runserver


5. How web page looks?
![image](https://user-images.githubusercontent.com/47074753/112622502-2047be80-8e51-11eb-9835-e233b4e5bc83.png)

6.after passing image and xml file
![image](https://user-images.githubusercontent.com/47074753/112623520-7701c800-8e52-11eb-8361-9e5fa5eed2c7.png)
