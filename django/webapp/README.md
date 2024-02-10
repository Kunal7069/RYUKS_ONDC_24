# How to run Django app locally

:information_source: Clone the project into your choice of directory on your computer, then
  
```bash
cd django/webapp
pipenv sync
pipenv shell
python manage.py runserver
```

Additionally you can run if you have made some changes to the model

```bash
python manage.py makemigrations
python manage.py migrate
```

Make migrations will scan and compare the changes against the current version of your migration files, and the migrate command will apply the changes if any changes reported/discovered by the makemigrations. So everytime you make changes to your model you can apply the changes.

:warning: for the complex changes sometimes makemigrations unable to detect changes.

Go to your browser and type

```
http://127.0.0.1:8000/
```
