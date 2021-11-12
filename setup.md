# Getting Started

If you're on OSX or Linux, you should be able to run `./scripts/bootstrap.sh` and your environment will get set up.

If that fails, or you're on Windows, you can follow the instructions below.

## Dev environment

Install requirements
- python 3.9.6
- psql 14

## Database setup

We need to create a psql database as well as a user to access that data.
Need to make a new user, a password for that user, a database, and make sure the new user has permissions to create new databases (this is important for testing).

The password for local dev database does not need to be secure because it should not be exposed to the internet. It will not be exposed by default.

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

The .env.example file has an example of what the database connection string should look like.
It's in the form of `postgres://<username>:<password>@<host ex localhost>:<port which default is 5432>/<db_name>`


## .env file

This file is where secure settings should be saved, a different .env file is used in production. Absolutely no API keys, passwords should be committed into GitHub so .env file is how these are stored instead

Each person should have the same fields in their .env file but potentially different values. In production .env will have things like API keys, logging to external services, etc as well which local devs won't.


# Docker

A few main differences when running it with docker locally.
One difference will be the database connection string, the `docker-compose` has a default set of psql username, password, db name than what will be in your local .env file but these can be easily changed.
The biggest difference is the host name when running on docker will actually be the service name in the docker-compose which is currently `web-db`.

It is normally easy and faster to do dev when not running in docker unless you mount your local filesystem to the container. This way no rebuild is required after every change.