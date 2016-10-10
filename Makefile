##############
# Deployment #
##############

deploy:
	sudo mkdir -p /docker/dazzar_web
	sudo mkdir -p /docker/dazzar_postgres
	sudo rsync -av --delete . /docker/dazzar_web

############
# Database #
############

# Start db
db-start: deploy
	-docker stop dazzar_postgres
	-docker rm dazzar_postgres
	docker-compose -f docker/docker-compose.yml up -d --build dazzar_postgres

# Migrate database from models
db-migrate: build
	docker run --rm --name dazzar_migrate --link dazzar_postgres -v $$(pwd):/dazzar -w /dazzar -e FLASK_APP=/dazzar/web/web_application.py dazzar_web flask db migrate

# Upgrade database on running postgres
db-upgrade: build
	docker run --rm --name dazzar_upgrade --link dazzar_postgres -v $$(pwd):/dazzar -w /dazzar -e FLASK_APP=/dazzar/web/web_application.py dazzar_web flask db upgrade

###########
# General #
###########

# Stop all running dockers
all-stop:
	-docker stop dazzar_migrate
	-docker rm dazzar_migrate
	-docker stop dazzar_upgrade
	-docker rm dazzar_upgrade
	-docker stop dazzar_bot
	-docker rm dazzar_bot
	-docker stop dazzar_web
	-docker rm dazzar_web
	-docker stop dazzar_postgres
	-docker rm dazzar_postgres

# Start all
all-start: build deploy
	docker-compose -f docker/docker-compose.yml up  -d

# Start web
web-start: build deploy
	docker-compose -f docker/docker-compose.yml up dazzar_web

# Start bot
bot-start: build deploy
	docker-compose -f docker/docker-compose.yml up dazzar_bot

# Build
build:
	docker-compose -f docker/docker-compose.yml build
