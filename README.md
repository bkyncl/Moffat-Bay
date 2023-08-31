# Moffat-Bay Project - CSD 460 Capstone
Group capstone project for Moffat Bay website (Edit for more clarity at later date)
## Contributors
* Brittany Kyncl
* Mark Witt
## PROJECT SETUP

Once the project is cloned from GitHub, Follow these steps to complete setup of the project.

### File Structure:
The Moffat_Bay full repo contains the folders:
html_css_pages - This folder is for putting completed html and css files for the project. This will make it easier for the buidling of the project. Later on they will be added to the corresponding project folders
moffat_bay - This is the django projects 'parent' folder. to execute any commands listed in this readme, you must be in this folder in the terminal. this is where the manage.py and required_installs.txt files are located.
TDD_and_documents - This folder is for all required documentation for the project. This is the working folder. 
turn_in_stuff - This folder will contain copies of all documentation that has been turned in as assignments. 


### Before running the server, some setup steps must be taken. 
> **Warning**

**1.** Required software dependancies must be installed. to install these dependancies, run the following command from terminal in the moffat_bay parent directory:

*pip install -r /required_installs.txt*

This will install all required dependancies for the project. 

For now, during development we will just use the included db.sqlite3 for the database. it will function the same as if we were using MySQL, but the 
db file will be able to be kept updated on GitHub, so the team will have any and all changes. 

Username: **bkyncl**

Password: **Bravo123**

you are in the db as a superuser/admin, so you can see the localhost:8000/admin page as well - containing all the db and user account/profile info.

During deployment we will switch over to the MySQL server. 

If everything was installed correctly, and you have fetched/pulled the lastest code from the repo - start the server from the command line, in the moffat_bay (notice the lowercase project folder) and enter the command:

python manage.py runserver

Then open a browser for localhost:8000 ****notice port # is 8000, this is different than usual.****3

This is the internal development server for Django, it has its own webserver for the development built in. You can still work on the project while the server is running, it updates live. Just have to refresh the browser
to see any changes.

For the project structure:
each app (section of the project) has its own folder. 
the moffat_bay folder is the main project folder, containing the project settings files, and overall url configurations for the project.
the media folder will hold all images used on the site, and the profile_pic subfolder will hold and organize user profile pictures should they choose to upload one
the users folder contains everything for the users accounts for the project. this includes user login information and profile info (email, address, whatever else we want )
    The users app takes advantage of Django's built in user account framework, including the login and authentication system, all handled behind the scences for us with Django.
the reservations folder contains everything for the main part of the site. it will hold all of the back end for making/looking up reservations, as well as the rest of the html for the site
    the static folder inside reservations holds the css for the entire site

How each app/folder is setup by Django-
Each app gets the same type of structure, so they all work in unison together:
a templates/(appname) folder which is where all html pages are kept
admin.py file registers the app with the project's built in admin page, so any db models can be viewed/edited in the admin page
models.py is the database models for the app. this is the database structure or ERD of how the database tables are set up. think of each model as a table in the db
urls.py is the file that handles the urls between html pages, including the routing and names for each link. html link structure is: a href="{% url 'home' %}" this will take you to whatever is view is setup in the url file
    for the name of 'home'. think of this file as the connector between the view and the server, telling the server what view to use.
views.py is the file that serves each view - or renders data and the html. this file feeds whatever data we want from the db and back end into the server with the required html page. it holds many different views,
    depending on what you are wanting the page to display.
forms.py - this file handles the forms that will be used on the html page. it creates the forms based on the model, and gets served to the html/server within a view. forms get passed into the html as a variable, so no
    need to create extra form html all seperate, it gets handled by the back end and the server
apps.py is the config for the app (users/reservations). this is setup by Django automatically and we dont have to mess with. 

optional files:
we can create extra python files as needed, to handle extra little tasks. just have to import them into the other files we will need the methods for. as an example, in the users app there is a states.py file, which contains a 
dictionary of all 50 states, and that is used in the forms for the user to choose a state when entering their address. the form has a state variable that is listed as a choice field with the parameters of the choices being the 
state.py states dictionary.
Another example in users: signals.py recieves a signal when a user registers for a new account. during post the signal.py file detects the new user registration, and creates their user profile automatically. 
*** currently this only creates the profile, i'll have it finished soon where it will also populate the profile with info entered by the user registration form****

the templates/(app) folders currently have sample html pages as placeholders until we get the html parts coded. the reservations app has the base.html (which everything else extends) containing 
header/navbar/message-area/footer. the home.html will contain the actual page. all pages will just extend the base.html so we only have to code the header/footer/navbar areas once.
the templates/users folder contains sample login, logout, user registration/password reset pages. these also extend base.html, and just need to be coded to match the rest of the site design. forms are all rendered by the Django
view, so we dont have to manually create them in html each time. Django also handles the back end user authentication for us.  These are all in place for getting the user login/profile stuff setup for now, but the html is open 
for whatever design we choose.

Just wanted to give a quick overview of how it all works and is setup/structured. hope this helps!
Any questions or issues dont be afraid to reach out.
