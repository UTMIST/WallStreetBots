# Getting Started

If you're on OSX or Linux, you should be able to run `./scripts/bootstrap.sh` and your environment will get set up.

If that fails, or you're on Windows, you can follow the instructions below.

## Dev environment

Install requirements
- python 3.9.6
- psql 14

## Database setup

We need to create a psql database as well as a user to access that data.

Open up a psql shell:

```
psql postgres
```

Then create the database:

```
createdb wsbots
```

Followed by:

```
CREATE USER wsbots WITH PASSWORD 'password';
```

## Library requirements

In `./`: run `pip install -r requirements.txt`

## Testing locally

Making sure you have the correct python virtual environment run 

`python -Wa ./manage.py test backend`


This `-Wa` enables all warnings so things like depreciation warnings will also show up. 

Need to make sure whatever database user you're using has createdb permissions.
If you get an error related to missing permissions try running opening a psql shell then running

`ALTER ROLE <role_name> createdb`

Where role_name is whatever is set in the .env file. 
