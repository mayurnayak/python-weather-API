Directories:

1.	templates- This contains all the HTML files required for web. They are written in Django templating language (https://djbook.ru/rel1.5/ref/templates/api.html )

2.	wapp- Djngo app that does the actual work. All logic is separated into apps within a projects. It consists of:
A)	 admin.py- This is where you register your database objects to Django.
B)	 forms.py- This is where you create your website application forms. The forms are rendered to HTML form tags (https://docs.djangoproject.com/en/1.11/topics/forms/ )
C)	 models.py- This is where you define your database tables and the fields. After you create the tables”:
	$./manage.py makemigrations
	$./manage.py migrate 
D)	views.py- These are python functions that are mapped to specific URL in urls.py file within the main project. The views can also be class bases and handle multiple HTTP methods like POST, GET, PUT etc.

3. weather- This contains the project files:-
A) urls.py- This contains path definitions that map python functions to specific URL.
B) settings.py- This is where all the settings and Django specific applications are registers or placed. 
C) wsgi.py- This is used during hosting.

4. manage.py This contains the initialization code for the projects. It supports all Django specific command line arguments as well as application start and loading.