#Add any comments on this here

#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

.PHONY: help

help:
	@echo ""
	@echo "PROJECT HELP:"
	@echo "make               		- this prints out the help for this makefile."
	@echo "make help          		- this prints out the help for this makefile."
	@echo "Setup:"
	@echo "make venv	    		- this deletes and recreates the venv virtual environment from requirements.txt"
	@echo "make venv-static		- collect static files"
	@echo "make venv-migrations   		- DANGER - this makes the migration file and creates/pushes it onto the database."
	@echo "make venv-show-migrations   	- Show migrations"
	@echo "make venv-admin   		- DANGER - this can be used to setup an admin password for the admin site."
	@echo "make venv-docs	    		- delete and re-creates the html file in the docs directory using index.rst file"
	@echo "make venv-all	    		- delete and re-creates the virtual env, static files, migrations and docs"
	@echo "Run:"
	@echo "make venv-run      		- runs the script in the venv virtual environment."
	@echo "make venv-run-debug      	- runs the script in the venv virtual environment, in debug mode"
	@echo "Docker: (must have docker installed and running)"
	@echo "make doc-up			- Run docker compose to raise database and website."
	@echo "make doc-down			- DANGER - Clear the docker stack."
	@echo "Testing:"
	@echo "make venv-build-fixtures	- DANGER - rebuilds fixtures files from current database, which are used in tests."
	@echo "make venv-test   		- Run the Test in the virtual environment."
	@echo "make venv-cov-report		- Run the Test in the virtual environment using coverage and then display coverage report"
	@echo "make venv-cov-html		- Run the Test in the virtual environment using coverage and build an html report"
	@echo "Code Standard:"
	@echo "make pystat   			- Code standards for ebdjango and apps directories."
	@echo "Clean:"
	@echo "make venv-clean    		- Remove __pycache__ etc"
	@echo "make clean-venv    		- Remove venv virtual environment."
	@echo "make clean-static    		- Remove static from core directory."
	@echo "make clean-cov    		- Remove coverage from core directory."
	@echo "make clean-logging		- Remove log file ebdjango_logging.log"
	@echo "Distribution:"
	@echo "make venv-build-req    		- Rebuilds the requirements file from the venv virtual environment."
	@echo ""
venv:
	@echo ""
	@echo "Remove the venv virtual environment and then re-create it. using the requirements.txt file."
	@echo ""
	rm -rf venv
	@echo ""
	python3.6 -m venv venv
	@echo ""
	( source venv/bin/activate; pip3 install -r requirements.txt; )

venv-static:
	@echo ""
	@echo "Collect the static files"
	@echo ""
	( source venv/bin/activate; python3.6 manage.py collectstatic --noinput; )
	@echo ""

venv-migrations:
	@echo ""
	@echo "DANGER - Make migrations file and then push it onto the database"
	@echo ""
	( source venv/bin/activate; python3.6 manage.py makemigrations; python3.6 manage.py migrate; )
	@echo ""

venv-show-migrations:
	@echo ""
	@echo "Show migrations"
	@echo ""
	( source venv/bin/activate; python3.6 manage.py showmigrations; )
	@echo ""

venv-admin:
	@echo ""
	@echo "DANGER - Setup superuser for admin site."
	@echo ""
	( source venv/bin/activate; python3.6 manage.py createsuperuser; )
	@echo ""

venv-docs:
	@echo ""
	@echo "Remove the documents and then recreate it using index.rst"
	@echo ""
	(rm -rf ./docs/*.html; source venv/bin/activate; rst2html5.py ./docs/index.rst ./docs/index.html; )
	@echo ""

venv-all:
	@echo ""
	@echo "Deletes coverage, re-creates the virtual env, static files, migrations and docs"
	@echo ""
	@echo ""
	@echo ""
	@echo "   Delete Coverage"
	@echo ""
	( rm -rf .coverag*; rm -rf htmlcov; )
	@echo ""
	@echo ""
	@echo "   Delete Logging"
	@echo ""
	( rm -rf ebdjango_logging*; )
	@echo ""
	@echo "   Rebuild Virtual Environment"
	@echo ""
	( rm -rf venv; sleep 1; )
	@echo ""
	python3.6 -m venv venv
	@echo ""
	( source venv/bin/activate; pip3 install -r requirements.txt; )
	@echo ""
	@echo "   Rebuild Static"
	@echo ""
	( rm -rf static; sleep 1; )
	@echo ""
	( source venv/bin/activate; python3.6 manage.py collectstatic --noinput; )
	@echo ""
	@echo "   Run Migrations"
	@echo ""
	( source venv/bin/activate; python3.6 manage.py makemigrations; python3.6 manage.py migrate; )
	@echo ""
	@echo "   Build Doc's"
	@echo ""
	( rm -rf ./docs/*.html; sleep 1;)
	@echo ""
	(source venv/bin/activate; rst2html5.py ./docs/index.rst ./docs/index.html; )
	@echo ""

venv-run:
	@echo ""
	@echo "Running application using venv virtual environment."
	@echo "  (WARNING - May not work properly due to use of "
	@echo "   ManifestStaticFilesStorage)"
	@echo ""
	( source venv/bin/activate; python3.6 manage.py runserver; )
	@echo ""

venv-run-debug:
	@echo ""
	@echo "Running application using venv virtual environment, in debug mode"
	@echo ""
	@echo ""
	( export DJANGO_DEBUG=1; source venv/bin/activate; python3.6 manage.py runserver; )
	@echo ""

doc-up:
	@echo ""
	@echo "Run docker compose to raise the database and then the website."
	@echo ""
	docker-compose -f ./docker/docker-compose.yml up --build -d
	@echo ""

doc-down:
	@echo ""
	@echo "Clear the stack (I tend to use command lines or Desktop)."
	@echo ""
	docker-compose -f ./docker/docker-compose.yml down --rmi all -t 30
	@echo ""

venv-build-fixtures:
	@echo ""
	@echo "DANGER - rebuild fixtures files from current database (assume local/test database)"
	@echo ""
	( source venv/bin/activate; python3.6 manage.py dumpdata --natural-primary --natural-foreign --indent 4 --exclude=contenttypes --exclude=auth.Permission > ./apps/MyProjects/fixtures/myprojects_testdata.json; )
	( source venv/bin/activate; python3.6 manage.py dumpdata --natural-primary --natural-foreign --indent 4 --exclude=contenttypes --exclude=auth.Permission > ./apps/Training/fixtures/training_testdata.json; )
	( source venv/bin/activate; python3.6 manage.py dumpdata --natural-primary --natural-foreign --indent 4 --exclude=contenttypes --exclude=auth.Permission > ./apps/MySearch/fixtures/mysearch_testdata.json; )
	@echo ""

venv-test:
	@echo ""
	@echo "Running test in venv virtual environment."
	@echo ""
	@echo "   to debug, you could use the --keepdb option"
	@echo ""
	( source venv/bin/activate; python3.6 manage.py test --noinput; )
	@echo ""

venv-cov-report:
	@echo ""
	@echo "Running test using coverage and then display report in venv virtual environment."
	@echo ""
	( source venv/bin/activate; rm -rf .coverag*; rm -rf htmlcov; sleep 1; coverage run manage.py test --noinput ; coverage report)
	@echo ""

venv-cov-html:
	@echo ""
	@echo "Running test using coverage and then display report in venv virtual environment."
	@echo ""
	( source venv/bin/activate; rm -rf .coverag*; rm -rf htmlcov; sleep 1; coverage run manage.py test --noinput ; coverage html)
	@echo ""

pystat:
	@echo ""
	@echo "Code standards for ./ebdjango and ./apps"
	@echo ""
	( ./scripts/codestyle.sh; )
	@echo ""
	
venv-clean:
	@echo ""
	@echo "Remove __pycache__, etc"
	@echo ""
	rm -rf ./*/__pycache__*
	@echo ""

clean-venv:
	@echo ""
	@echo "Remove venv virtual environment directory"
	@echo ""
	rm -rf venv
	@echo ""

clean-static:
	@echo ""
	@echo "Remove static directory from main project"
	@echo ""
	rm -rf static
	@echo ""

clean-cov:
	@echo ""
	@echo "Remove coverage results and directory from main project"
	@echo ""
	( rm -rf .coverag*; rm -rf htmlcov; )
	@echo ""

clean-logging:
	@echo ""
	@echo "Remove log file ebdjango_logging.log"
	@echo ""
	( rm -rf ebdjango_logging*; )
	@echo ""

venv-build-req:
	@echo ""
	@echo "Rebuild requirements.txt from the venv virutal environment."
	@echo ""
	rm -rf requirements.txt
	@echo ""
	( source venv/bin/activate; pip3 freeze > requirements.txt; )
	@echo ""
