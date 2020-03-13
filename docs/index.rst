==========================
MYWEBSITE - DJANGO AND AWS
==========================

Overview
========

This project is used to deploy MyWebsite on my Localhost a test environment and production environment.

It uses a number of technologies including:

    - Python's Django framework
    - AWS
    - HTML, CSS, Javascript
    - The Bootstrap framework

The system is designed to integrate with AWS's CodePipeline with GitHub being the source.

The site was based on the Aladin template written largely using bootstrap 4.   As such it may not work
effectively on older browsers.

Installation Guide
==================

Manual Installation
-------------------

Installation for this project is complicated.

- Firstly, for local development, a MySQL database is used with an account that has the ability to create
  and load data into into test databases.   The settings file contains two sets of code beginning with 
  'DATABASES = {'.   These indicate the connection requirements for the database which will need to be
  updated for the local database.

- In addition to this, when the application is run within AWS it is assumed that two elasticbeanstalk
  environments exist with the following characteristics:

-  Test Environment:
    - Currently an Application Load Balancer is used, but this may be changed in the future due to cost considerations.
    - WSGIPath is set to ebdjango/wsgi.py
    - Static Files are set so that /static/ is equal to static/
    - The following environment variables are set:
        - DJANGO_SETTINGS_MODULE is set to ebdjango.settings
        - EnvType is set to test
    - A MySQL database needs to exist and the connection details are stored in AWS Parameter Store under the following paths:
        - /MarksWebsite/test/DBHOST, /MarksWebsite/test/DBPORT, /MarksWebsite/test/DBPWD, /MarksWebsite/test/DBUser
    - The following record exists in the Parameter Store and is used for Unit Testing:
        - /MarksWebsite/test/PARAMSTORE_TEST   with value   'SUCCESS'
    - The remaining records also need to exist in the parameter store and are used to store things such as Django's secret key:
        - /MarksWebsite/test/SecretKey


-  Production Environment:
    - Currently an Application Load Balancer is used, but this may be changed in the future due to cost considerations.
    - WSGIPath is set to ebdjango/wsgi.py
    - Static Files are set so that /static/ is equal to static/
    - The following environment variables are set:
        - DJANGO_SETTINGS_MODULE is set to ebdjango.settings
        - EnvType is set to prod
    - A MySQL database needs to exist and the connection details are stored in AWS Parameter Store under the following paths:
        - /MarksWebsite/prod/DBHOST, /MarksWebsite/prod/DBPORT, /MarksWebsite/prod/DBPWD, /MarksWebsite/prod/DBUser
    - The remaining records also need to exist in the parameter store and are used to store things such as Django's secret key:
        - /MarksWebsite/prod/SecretKey


MakeFile - Mac (possibly linux)
------------------------------------------   

A makefile exists in core directory where the manage.py file exists and this may make using this code
easier.   I would normally test the scripts on Linux and create a batch file for windows, but I didn't want
to install another 2 MySQL databases on my computer (I have Windows and Ubuntu running on parallels).
As such this makefile has only been tested on a mac, it MAY work on linux and I have not provided an
equivalent for Windows.

Typical commands include:


- make               		    - this prints out the help for this makefile.
- Setup:
- make venv	    		    - this deletes and recreates the venv virtual environment from requirements.txt
- make venv-static		    - collect static files
- make venv-migrations   		- DANGER - this makes the migration file and creates/pushes it onto the database.
- make venv-show-migrations   - Show migrations
- make venv-admin   		    - DANGER - this can be used to setup an admin password for the admin site.
- make venv-docs	    		- delete and re-creates the html file in the docs directory using index.rst file
- make venv-all	    		- delete and re-creates the virtual env, static files, migrations and docs
- Run:
- make venv-run      		    - runs the script in the venv virtual environment (may not work well due to ManifestStaticFilesStorage).
- make venv-run-debug      	- runs the script in the venv virtual environment, in debug mode
- Testing:
- make venv-build-fixtures	- DANGER - rebuilds fixtures files from current database, which are used in tests.
- make venv-test   		    - Run the Test in the virtual environment.
- make venv-cov-report		- Run the Test in the virtual environment using coverage and then display coverage report
- make venv-cov-html		    - Run the Test in the virtual environment using coverage and build an html report
- Code Standard:"
- make pystat   			    - Code standards for ebdjango and apps directories.
- Clean:
- make venv-clean    		    - Remove __pycache__ etc
- make clean-venv    		    - Remove venv virtual environment.
- make clean-static    		- Remove static from core directory.
- make clean-cov    		    - Remove coverage from core directory.
- Distribution:
- make venv-build-req    		- Rebuilds the requirements file from the venv virtual environment.