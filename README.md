#Whatsapp Python Selenium Automation Script.

This is a script file for whatsapp reply feature functionality.


Versioning:-

	Python3 (version=3.6.6)
	Chrome Browser (version==70.0.3538.67)
	Chrome Webdriver (version==2.4.2) 
	Selenium (version==3.14.1)

Steps to setup Script :-

1. Create an environment in Python version 3.6

	virtualenv env_name

2. Install all the requirements stated in requirement.txt

 	pip install -r requirements.txt

3. Install Mysql on machine follow below url

	https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/

4. Bydefault Mysql providers a user called "root" having password "root" login in to Mysql and create a database and run the command for restore dump file. 

	Restore MySql Dump file 
	mysql -u username -p database_name < whatsapp_script_db.sql

5. Open Script file and update database name.

6. Execute script in console

 	python whatsapp_script.py
