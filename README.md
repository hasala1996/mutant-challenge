# mutant-challenge

# Description
- The Mutant Detection API is an application that allows you to identify if a DNA sequence belongs to a mutant. The API analyzes the DNA sequence for specific patterns and determines whether the DNA is mutant based on the presence of more than one sequence of four consecutive identical letters in any direction (horizontal, vertical or diagonal).

- The application is implemented in FastAPI and uses a hexagonal architecture to separate business logic, data access, and API entry points.

- The hexagonal architecture allows a high degree of decoupling between business logic and infrastructure details, which facilitates code scalability and maintainability. The layers of this architecture and how they are implemented in this project are described below.

##  Basic Project Structure

```
├── app/
│   ├── adapters/               # Infrastructure adapters (DB, API)
│   │   ├── api/                # Adapter for APIs (endpoints)
│   │   │   └── endpoints/      # API endpoints
│   │   ├── database/           # Database adapter
│   │   │   ├── models.py       # Database models
│   │   │   ├── repository/     # Repositories (concrete and abstract)
│   │   │   └── __init__.py
│   ├── core/                   # Application core (business logic)
│   │   ├── mutant/             # Logic module for mutant detection
│   │   │   ├── services.py     # Business services
│   │   │   └── ports/          # Ports (interfaces)
│   │   └── middleware/         # Error handling middleware
│   └── fast_api/               # FastAPI configuration file
│   ├── alembic                 # Alembic configuration
├── .env                        # Environment variables
└── README.md                   # README file
```

# Hexagonal Architecture

1. Endpoint (API Layer)
    The endpoint is the layer that exposes entry points to the application and allows interaction with external clients. In this project, endpoints are defined in adapters/api/endpoints.

    The endpoint to detect whether a DNA is mutant or not is /mutant/, and calls a core application service (MutantService) that handles the mutant detection logic.

    Endpoint flow:

    Receives the HTTP request and the DNA data.
    Calls the MutantService service to process the business logic.
    Returns the response to the client, indicating whether it is a mutant or not.

2. Service (Core Service)
    The service (MutantService) is responsible for the business logic of the application. In this case, the service is located in core/mutant/services.py. The main function of the service is to verify if the DNA is mutant or human.

    Service Responsibilities:

    Process mutant detection business logic.
    Use the DNA repository to access the database (for example, saving new sequences or viewing statistics).
    Encapsulate the business rules, so that the endpoint is only responsible for handling the HTTP request.

3. Repository
    In the hexagonal architecture, the repository acts as the adapter to access the database. There are two types of repositories in the project:

    Abstract Repository (Interface or Port): It is an interface in core/mutant/ports/repository.py, which defines the methods that specific repositories must implement. This allows business logic to depend on an abstraction rather than a specific implementation, making it easier to test and change the database if necessary.
    Concrete Repository: It is the implementation of the abstract repository interface and is located in adapters/database/repository/dna_repository.py. This particular repository handles direct interaction with the database, such as saving and retrieving DNA sequences.

    Repository Responsibilities:

    The concrete repository (DNARepository) implements database operations, such as creating DNA records and querying statistics.
    The service (MutantService) uses the abstract repository to access the database, allowing you to change the concrete implementation without modifying the service logic.

    Interaction Flow between Layers

    HTTP Request: The client sends an HTTP request to the /mutant/ endpoint, passing a DNA sequence.
    Endpoint: The endpoint receives the request, validates the data and calls MutantService.
    Service: MutantService processes the logic to check if the DNA is mutant. During this process, you can call the repository to save the sequence to the database or check if it already exists.
    Repository: MutantService uses the abstract repository, which is implemented by the concrete repository DNARepository, to interact with the database.
    Answer: The service returns the result to the endpoint, and the endpoint sends an HTTP response to the client, indicating whether the DNA is a mutant or not.


## Configuration and Execution
# Prerequisites
- Python 3.8+
- PostgreSQL (for database)
- Alembic (for migrations)

# Environment Configuration
- Clone the repository.
- Copy the .env_example file to .env and update the environment variables according to your configuration.
- Install the dependencies:
  pip install -r requirements.txt
- Run database migrations:
  alembic upgrade head

## Running the app
- To start the application in development mode, use the following command within app folder :
  uvicorn fast_api.fast_api_app:create_app --reload --port 8001
- To run the tests, use the following command:
  coverage run -m pytest
- to see coverage use:
  coverage report

## PRODUCTION
To test the deployed app, access:
- https://mutant-challenge-production.up.railway.app/docs#
Here the backend is already deployed using free services, such as a database and so on, the endpoints are available to be used.