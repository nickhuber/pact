Platform Agnostic Combat Tracker (PACT)
==============

A simple web application for preparing and running various d20 combat systems.

© 2015 Nick Huber


Developing
----------
You need python3 (3.4 or greater) and nodejs/npm to get going. These can likely be installed for you with `setup_dev.sh`

You can then get started by running 2 programs: `start_backend.sh` and `start_frontend.sh`, both in the root directory.
The output should tell you which port to connect your browser to to get started.

It should be at `localhost:8080`

There will be a default user with *admin* as the username and *pass* as the password

Deployment
----------
Deployment is pretty simple, and supports Fedora and sort of supports FreeBSD. See the services directory for more details

Make a user for the pact program

    sudo useradd pact

Install postgresql-server and then run

    sudo systemctl enable postgresql
    sudo systemctl restart postgresql.service

    sudo su - postgres
    psql
    CREATE DATABASE pact;
    CREATE USER pact;

    ALTER ROLE pact SET client_encoding TO 'utf8';
    ALTER ROLE pact SET default_transaction_isolation TO 'read committed';
    ALTER ROLE pact SET timezone TO 'UTC';

    GRANT ALL PRIVILEGES ON DATABASE pact TO pact;
    \q
    exit