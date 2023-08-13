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
**Warning**
**1.** Required software dependancies must be installed. to install these dependancies, run the following command from terminal in the moffat_bay parent directory:

*pip install -r /required_installs.txt*

This will install all required dependancies for the project. 

**2.** MySQL database must be configured and created. The included MySQL file (MySQL_Setup.sql) will setup the required user account within your MySQL database on your local machine. Please note: once the site is deployed it will have its own MySQL database on the host server which will hold all data. The local db will serve as a testing environment db to ensure funcionality. Please run the indicated sql file from your root account. 

This file sets up the database, creates the user account, and sets up the permissions for the user account. 

Username: **bravoteam**

Password: **Bravo123**

Permissions: **all on moffat_bay.***


To continue setup of the MySQL database, from the command line in the parent moffat_bay project directory, run the following commands:

*python manage.py makemigrations*

*python manage.py migrate*

Django will automatically setup the required db tables and structure for you. There is no need for further changes to the db, as django will not recognize them and this can cause errors. 

**Note** 
*If you are fetching/pulling from the repo, you must still perform the migrate commads before working on the project further. this will help ensure that the db structure is consistant at all times. **IF** we run into an issue with a db not working correctly due to these issues, we will switch over to the sqlite3 db that is included with the project, for the remainder of coding and testing. Deployment will still remain as MySQL, and the commands are basically the same for both.*