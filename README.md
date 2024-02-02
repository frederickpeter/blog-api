# My Blog

An api for a blog platform

## Getting Started

### Running using Docker (Windows & Mac Users)
Make sure you have docker installed and running.

- To build the **docker images**, use this command: 

      $ docker compose -f local.yml build

- To run **migrations**, use this command: 

      $ docker compose -f local.yml run --rm django python manage.py migrate

- To create a **superuser account**, use this command:

      $ docker compose -f local.yml run --rm django python manage.py createsuperuser

- To start the **containers**, use this command:

      $ docker compose -f local.yml up


### Documentation
- To access the docs for this api, visit http://127.0.0.1/api/docs



