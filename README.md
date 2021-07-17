
         _______.____    ____      _______..___  ___.  __   __  ___      ___              _______. _______   __  ___ 
        /       |\   \  /   /     /       ||   \/   | |  | |  |/  /     /   \            /       ||       \ |  |/  / 
       |   (----` \   \/   /     |   (----`|  \  /  | |  | |  '  /     /  ^  \          |   (----`|  .--.  ||  '  /  
        \   \      \_    _/       \   \    |  |\/|  | |  | |    <     /  /_\  \          \   \    |  |  |  ||    <   
    .----)   |       |  |     .----)   |   |  |  |  | |  | |  .  \   /  _____  \     .----)   |   |  '--'  ||  .  \  
    |_______/        |__|     |_______/    |__|  |__| |__| |__|\__\ /__/     \__\    |_______/    |_______/ |__|\__\
    ====================================================================================================================



# About

Tools to enhance the Sysmika ERPs by adding integrations with external systems. Each integration is built using
a microservice approach, in which each service (integration) comes OOTB with a basic set of operations:
* Authentication against the external system
* Basic CRUD operations 
* An internal in-memory database to cache transactions
* Test suite

Each service exposes an API, which is defined using the [OpenAPI](https://swagger.io/) specification. 

# Installation

## Windows (for development only)

* Install [Python 3.9](https://www.python.org/downloads/)
* Install [Pip](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)
* Install pipenv by running __pip install --user pipenv__
* Clone this repo and install all depencies by running __pipenv install__ from the root of the repository
* [Run Flask](#flask)

## Linux (for develoopment/production)

* Install Python 3.9 and Pip
* Run __sudo apt install pipenv__

## Flask

To run the Flask server (Windows):

* On cmd type:
  * __set FLASK_APP=run:run_app()__
  *  __set FLASK_ENV=development__
  * Go the directory __inbound__ in the integrations folder (for example: __src/integrations/mercadolibre/inbound__)
  * Run __flask run__ . Use --port to change the port of the server (default is 5000) 
  
## Gunicorn

Gunicorn is a WSGI HTTP Server that sits on top of the Flask API. It's recommended to use a reverse proxy (preferably Nginx) if the API is going to be exposed directly to the web

* Ensure that all dependencies are installed in the virtual env by running __pipenv install__
* From the root of the  repository run __gunicorn 'wsgi:run_app()'__ 
* The file __gunicorn.conf.py__ contains configurations for the Gunicorn server. More can be found [here](https://docs.gunicorn.org/en/latest/settings.html)

# Project Structure

* The __src__ folder contains the application code. Inside the __integration__ direction we have a specific directory for each service.

* The __test__ folder contains all unit tests for each service, and the necessary mock data. Check the [README](tests/README.md) for more information.

# Current Integrations

 [MercadoLibre](src/integrations/mercadolibre/README.md)
 

# Roadmap

`TODO`