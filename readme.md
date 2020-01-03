# Task 1 | SKJ Corp

## Running locally
First install the prerequisites

`sudo apt install python3 python3-pip virtualenv libpq-dev python3-dev build-essential postgresql-server-dev-all`

Then use the command `./start`

If the above command fails:
1. `virtualenv -p python3 venv`
2. `. venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py collectstatic`
6. Set the proper environmental variables in `.env` file
7. `python manage.py runserver`
