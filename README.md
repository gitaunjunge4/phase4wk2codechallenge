PHASE 4 WEEK2 CODE CHALLENGE

HEROES AND SUPERHEROES API
    -This is a Flask-based web application that serves as an API for managing heroes, superheroes, their powers, and related information. 
    -The application uses SQLAlchemy for database management and Marshmallow for serialization/deserialization of data.

GETTING STARTED

-These instructions will help you set up and run the application on your local machine.

    PREREQUISITES
    -Before you begin, make sure you have the following installed from a sutable Pipfile:

        -Python
        -Flask
        -Flask-SQLAlchemy
        -Flask-Migrate
        -Flask-RESTful
        -SQLAlchemy
        -Marshmallow


    INSTALLATION
        -Clone the repository to your local machine

        -Change to the project directory

        -Create a virtual environment

        -Activate the virtual environment

        -Install the project dependencies

    CONFIGURATION
        -Modify the database URI in the config.py file to suit your database setup: app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db" # Example SQLite URI

        -Create the database tables by running the following commands:
            flask db revison --autogenerate 'Created tables'
            flask db upgrade

RUNNING THE APPLICATION
    -To run the application, execute the following command:

    -python run.py 
    -The application should now be running on http://localhost:5555. You can access the API endpoints using tools like curl or Postman.

    ENDPOINTS
    This API provides endpoints for managing heroes, superheroes, powers, and their relationships. 

        -GET /heroes: Get a list of all heroes.
        -GET /heroes/{id}: Get details of a specific hero by ID.
        -POST /heroes: Create a new hero.
        -PUT /heroes/{id}: Update details of a specific hero by ID.
        -DELETE /heroes/{id}: Delete a hero by ID. 
        -Similar endpoints are available for superheroes, powers, and their relationships.

    Data Serialization
        -This application uses Marshmallow for data serialization. Serialization schemas are defined in the app.py file. You can customize these schemas as needed to format API responses.

AUTHOR 
GITAU NJUNG'E