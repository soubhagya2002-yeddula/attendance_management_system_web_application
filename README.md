#Attendance management system Application

A simple web based application named ATTENDANCE MANAGEMEENNT SYSTEM built using Django,
simple HTML,CSS and for responsive bootstrap, Django REST Framework and JWT Authentication

If we want to create any application by using django we make sure that whether  the python and pip are installed are not
to check whether both are  installed are not the commands are like 
#to check python is installed or not:python --version
#to check pip is installed or not:pip --version

step-1: Intially we have to create one folder
step-2: We have to open that folder in vs code
step-3:here we have to create virtual environment and we have to install django

#If we have to create virtual environment first we have to install virtual environment
-to install virtual environment the command is- pip install virtualenv
-now we have to create  virtualenv the command is -python -m virtualenv (environment name)
-after that we have to activate the environment
-Then we have to install django  the command- pip install django


step-4:After that we have to create one project by using django command
-to create project command is django-admin startproject (project-name)
-after this we have to change the directory the command is - cd project-name
-Finally whether django is installed or not we have to check for that
the command is ---python manage.py runserver-----
visit: http://127.0.0.1:8000/admin

step-5:From this step written the code as per requirements

supports ADMIN,MANAGER,AND EMPLOYEE roles

#Features
###Admin
-create,update, and delete users
-Assign employees to managers
-view all attendance records
-admin can change or edit the manager and employee details

###Manager
-view employees under them
-view weekly attendance summaries
-Approve attendance for a weeek

###Employee
-Mark daily attendance (Present/absent/leave)


##Technologies used
BACKEND: Django+Django REST Framework
Auth: JWT (using djangorestframework-simplejwt')
Database: SQLite (default it will come )
Frontend: HTML,CSS,BOOTSRAP
Documentation: Swagger and postman

In last we have to apply migrations the commands are:
python manage.py makemigrations
python manage.py migrate

-to create superuser
python manage.py createsuperuser

----LOGIN CREDENTIALS-----
-for aadmin
USERNAME:y_soubhagya
PASSWORD:Soubhagya@1234

-for managers

Username:Roopa
Email:
Password:Roopa@1234

Username:Sowmya
Email:sowmya1234@gmail.com
Password:Ramya@1234

Username: Sharmila 
Email:sharmila@gmail.com
Password:Sunny@1234

-for employees

Username:bhoomika
Email:bhoomika1234@gmail.com
Password:Bunny@1234

Username:Manvitha
Email:
Password:Princy@1234
Manvitha Manager roopa

Username:Hanshik
Email:hanshik1234@gmail.com
Password:vicky@1234
Hanshik manager sowmya

Username :Mamatha
Password:Amma@1234
Email:mamatha123@gmail.com
Manager Sharmila

Username: srilekha
Password: Chitti@1234
Email: srilekha1234@gmail.com
Manager Prasanthi

