#!/bin/bash

function repositorium(){
    case "$1" in
    "install")
            if [[ "$#" -eq 0]] ; then
                pip install "$@"
            else
                pip install -r requirements.txt
            fi
            ;;
    "startapp"|"makeapp"|"newapp")
                                   mkdir repositorium/$2
                                   python manage.py startapp $2 repositorium/$2
                                   ;;
    "makemigrations"|"makemigration") python manage.py makemigrations --name $2 $3
                      ;;
    "migrate") python manage.py migrate
                ;;
    "jupyter") echo "Running jupyter with django"
               python manage.py shell_plus --notebook
               ;;
    "up") python manage.py runserver 0.0.0.0:8000
          ;;
    "test") pytest $2
            ;;
    *)
        echo "install: Install requirements or provided package"
        echo "startapp|makeapp|newapp: create new app with provided name"
        echo "makemigrations or makemigration: Run provided migrations"
        echo "migrate: Run the migrations on the database"
        echo "jupyter: Run jupyter notebook"
        echo "up: run local server"
        echo "test: run the tests with pytest"
        ;;
    esac
}
