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

*pip install -r /requirements.txt*

This will install all required dependancies for the project. 

For now, during development we will just use the included db.sqlite3 for the database. it will function the same as if we were using MySQL, but the 
db file will be able to be kept updated on GitHub, so the team will have any and all changes. 

Username: jane@doe.com

Password: Testing123!

This testing account in the db as a superuser/admin, so you can see the localhost:8000/admin page as well - containing all the db and user account/profile info.

During deployment we will switch over to the MySQL server. 

If everything was installed correctly, and you have fetched/pulled the lastest code from the repo - start the server from the command line, in the moffat_bay (notice the lowercase project folder) and enter the command:

python manage.py runserver

Then open a browser for localhost:8000 ****notice port # is 8000, this is different than usual.****3

This is the internal development server for Django, it has its own webserver for the development built in. You can still work on the project while the server is running, it updates live. Just have to refresh the browser
to see any changes.

