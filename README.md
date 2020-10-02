
# MyWebsite - Mark Wilson

I do not display the live website code on a public github repository and this version of the README file
may in fact point to a replica of the repository.   As a result the code may be out of date.   Please follow this link to see the live [site](https://markjohnwilson.net).

The code has a high level of coverage (over 90%) and has been checked with pycodestyle.

## Description

---

This project is a personal website setup using Python and the Django Framework.   It has a number of key characteristics:

* At the time of writing I used Python 3.6
* The project has been designed so that it works and can be developed on a local computer, but largely runs on an AWS EB Environment.
* Initially the project was written using a multiple instance application load balancer, however due to cost considerations the technology has been adjusted to a single instance.
* There is test and prod EB environment setup, which is used with GitHub and CodePipeline to form a CI/CD pipeline.   As this may well be a replica of the production code, the code would need considerable adjustment to get it working.


## Local Environment

---

Local development work tends to be done on a Macbook Pro.   A local MySQL database needs to be setup and then the ebdjango/settings.py file needs to
be updated for the local connection:

```
# Assume localc computer and connecting to localhost.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbMarksWebsite',
        'USER': 'mark',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## AWS Test Elastic Beanstalk Environment

---

A test AWS Elastic Beanstalk Environmnet needs to be setup as a single instance (NOT AN APPLICATION LOAD BALANCER), with the following characteristics:

* EB Configuration Includes:
    * WSGI Path:   ebdjango/wsgi.py
    * Num Proess and Num Threads:   currently set to 3 and 15.
    * Static Files:
        * Path: /static/
        * Dir: static/
    * Deployment Policy:    'All at Once'
    * Environment Properties:
        |   Name                    |   Value                 |
        |---------------------------|-------------------------|
        |   DJANGO_SETTINGS_MODULE  |   ebdjango.settings     |
        |   EnvType                 |   test                  |
        |   LoggingLevel            |   Debug                 |

    

* In addition to the EB Environment, a MySQL database for the test environment needs to be created.

## AWS Prod Elastic Beanstalk Environment

---

* EB Configuration Includes:
    * WSGI Path:   ebdjango/wsgi.py
    * Num Proess and Num Threads:   currently set to 3 and 15.
    * Static Files:
        * Path: /static/
        * Dir: static/
    * Deployment Policy:    'Immutable'
    * Environment Properties:
        |   Name                    |   Value                 |
        |---------------------------|-------------------------|
        |   DJANGO_SETTINGS_MODULE  |   ebdjango.settings     |
        |   EnvType                 |   prod                  |
        |   LoggingLevel            |   ERROR                 |

* In addition to the EB Environment, a MySQL database for the prod environment needs to be created.

## Parameter Store

---

The parameter store is used extensively to store secret information such as keys and passwords.   The following needs to be setup with
suitable inputs:

|   Parameter Name                          |   Parameter Name                           |
|-------------------------------------------|--------------------------------------------|
|   /MarksWebsite/prod/DBHOST               |    /MarksWebsite/prod/DBPORT               |
|   /MarksWebsite/prod/DBPWD                |    /MarksWebsite/prod/DBUser               |
|   /MarksWebsite/prod/Recaptcha_SecretKey  |    /MarksWebsite/prod/Recaptcha_SiteKey    |
|   /MarksWebsite/prod/SESAccessKeyID       |    /MarksWebsite/prod/SESSecretAccessKey   |
|   /MarksWebsite/prod/SecretKey            |    /MarksWebsite/test/PARAMSTORE_TEST      |
|   /MarksWebsite/test/DBPWD                |    /MarksWebsite/test/DBUser               |
|   /MarksWebsite/test/Recaptcha_SecretKey  |    /MarksWebsite/test/Recaptcha_SiteKey    |
|   /MarksWebsite/test/SESAccessKeyID       |    /MarksWebsite/test/SESSecretAccessKey   |
|   /MarksWebsite/test/SecretKey            |                                            |

*Please note that DBPWD, Recaptcha_SecretKey, SESSecretAccessKey and SecretKey were setup using SecureString parameters.*

## HTTPS

---

Originally when this website was written using an application load balancer it was fairly easy to add HTTPS to the website,
however in order to reduce costs, I modified the code so that it uses a single instance.   If you use this code on a website
you may need to get a certificate signing request and purchase a new certificate, which is beyound the scope of this document.
More information can be found from your certificate provider.

It is important to note that a copy of the certificate is saved on an S3 bucket, which is downloaded by the config files and they
may need to be adjusted appropriately.

Within the .ebextensions directory, the following two files are the core files that may need to be adjusted for a new https
certificate or http redirection to a new website address:

|   File      Name                          |   Impact                                   |
|-------------------------------------------|--------------------------------------------|
|   https-instancecert-python34.config      |    HTTPS Certificate Keys                  |
|   https-redirect-python.config            |    Controls where HTTP redirects to.       |

## CODEPIPELINE

---

I have a github repository that feeds directly into CodePipeline.   Any processes such as unittests and migrations are then run and finally the
code is pushed into a 'test' environment.   Once I am happy with this, codepipeline then feeds into a similar 'prod' environment.
If you were to use this code, it would be advisable to setup CodePipeline in a similar manner once the EB environments have been created.

## DOCKER

---

I wanted to explore the use of Docker more, however I have recently reduced the website from an application load balancer to a
single instance to reduce costs and for this reason I have decided to hold off on any work using Kubernetes.   A docker directory
exists which contains a dockerfile and docker-compose.yml file.   I tend to use a makefile for ease, so the following commands
may be useful:

```
make doc-up   or
```

```
docker-compose -f ./docker/docker-compose.yml up --build -d
```

```
make dow-down   or
```

```
docker-compose -f ./docker/docker-compose.yml down --rmi all -t 30
```

## MAKEFILES

---

I tend to use a makefiles to simplify the execution of code.   I suggest you investigate the makefile and a full list of commands can be found using either of the following:

```
make
```

```
make help
```

I tend to use the following command frequently to setup the local environment:

```
make venv-all
```

However I believe that it is particularly important to pay attention to the following tasks when setting up the site:

* Setting up a virtual environment:

    ```
    make venv   ,or
    ```

    ```
    rm -rf venv; python3.6 -m venv venv; source venv/bin/activate; pip3 install -r requirements.txt;
    ```

* Collecting Static Files:

    ```
    make venv-static   ,or
    ```

    ```
    source venv/bin/activate; python3.6 manage.py collectstatic --noinput;
    ```

* Migrations:

    ```
    make venv-migrations   ,or
    ```

    ```
    source venv/bin/activate; python3.6 manage.py makemigrations; python3.6 manage.py migrate;
    ```

* Setting up an admin account:

    ```
    make venv-admin   ,or
    ```

    ```
    source venv/bin/activate; python3.6 manage.py createsuperuser;
    ```

I tend not to use the following command within my local environment because the use of ManifestStaticFilesStorage means that the
static files are not displayed properly:

```
make venv-run   ,or
```

```
source venv/bin/activate; python3.6 manage.py runserver;
```

Instead, I suggest either usig the debug environment:

```
make venv-run-debug   ,or
```

```
export DJANGO_DEBUG=1; source venv/bin/activate; python3.6 manage.py runserver;
```

Alternatively use the docker files:

```
make doc-up   ,or
```

```
docker-compose -f ./docker/docker-compose.yml up --build -d
```
