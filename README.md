
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

For development for now just set a pipenv using the Pipfile of the repo for dependencies. In __integrations/<service>/credentials__ we have two YAML files: 
* One to hold real credentials (__credentials.yml__)
* One to hold mock credentials (__credentials.example.yml__)

`TODO: build a dist package`

## Flask

`TODO: add documentation from Notion.`

To run the Flask server (Windows):

* On cmd type:
  * __set FLASK_APP=run:run_app()__ // If we pass False to run_app, the Flask application will use Production credentials
  *  __set FLASK_ENV=development__
  * Go the directory __inbound__ in the integration folder (for example: __src/integrations/mercadolibre/inbound__)
  * Run __flask run__ . Use --port to change the port of the server (default is 5000)  


# Project Structure

* The __src__ folder contains the application code. Inside the __integration__ direction we have a specific directory for each service.

* The __test__ folder contains all unit tests for each service, and the necessary mock data. Check the [README](tests/README.md) for more information.

# Current Integrations

 [MercadoLibre](src/integrations/mercadolibre/README.md)
 

# Roadmap

`TODO`