# Build the Docker containers
build:
	docker-compose build

# Start the Docker containers
up:
	docker-compose up -d

# Load initial RFID data
load-initial-rfid:
	docker-compose exec app python manage.py load_initial_rfid

# Load initial data
load-initial-data:
	docker-compose exec app python manage.py load_initial_data

# Start the application and load all required data
start: up load-initial-rfid load-initial-data

# Stop and remove the Docker containers
down:
	docker-compose down${v:+ -v}

clean-poc:
	docker compose exec app python manage.py clean_poc

# Display help
help:
	@echo "Usage: make [command]"
	@echo ""
	@echo "Available commands:"
	@echo "  build                 Build the Docker containers"
	@echo "  up                    Start the Docker containers"
	@echo "  load-initial-rfid     Load initial RFID data"
	@echo "  load-initial-data     Load initial data"
	@echo "  start                 Start the application and load initial data"
	@echo "  down                  Stop and remove the Docker containers"
	@echo "                        Use '-v' to remove volumes"
	@echo "  help                  Display this help message"