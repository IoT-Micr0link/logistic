# Smart Logistics Project

Intelligent logistics system based on RFID technology for automatic control 
and management of inventory and warehouse processes. 
It uses RFID as the information capture technology and the basis for real-time 
automated management of the main logistics processes described above.

## Project Structure

The project is divided into the following modules:

- **rfid**: Data ingest, manages information capture in storage warehouses
- **Inventory**: Manages the main use cases for inventory processes
- **Warehouse**: Manages product or item inputs and outputs
- **API**: Connection for general data inputs and outputs of the system

## Project Initialization

To start the project, follow these steps:

1. Clone the repository from GitHub.
2. Build the Docker image `make build` 
3. Initialize the containers `make up`
4. Create the necessary initial information for the project
   - `make load-initial-rfid`
   - `make load-initial-data`
5. Go to the local address on your computer `localhost:8000`

To avoid the usage of all these commands simple run on terminal:
- `make start`

To shut down the project:
- `make down` add the flag -v to delete the db too `make down -v`

To clean the project from readings and warehouse or transfer orders run:
- `make clean-poc`

## Technologies Used

- Python 3.10.4
- Django
- Docker and Docker Compose 
- PostgreSQL

## Constraints

- If the data ingestion system via RFID is not available, it is possible to 
  simulate random data readings through a random process that obeys the initial 
  configuration of the PoC designed for this project. Use the command  
  `docker compose exec app python manage.py rfid_simulate`.
