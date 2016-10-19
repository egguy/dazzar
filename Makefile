############
# database #
############

# create dabase persistence
/docker/dazzar_postgres:
	sudo mkdir -p $@

# start db
db-start: /docker/dazzar_postgres
	docker-compose -f docker/docker-compose.yml up -d --build dazzar_postgres

# stop db
db-stop:
	-docker stop dazzar_postgres
	-docker rm dazzar_postgres

# migrate database from models
db-migrate: build
	mkdir -p /tmp/migrations
	rsync -av --delete migrations /tmp
	-docker run --rm --name dazzar_migrate --link dazzar_postgres -v $$(pwd)/migrations:/migrations -w /dazzar -e flask_app=/dazzar/web/web_application.py dazzar_web flask db migrate --directory /migrations
	sudo rm -rf migrations/__pycache__ migrations/versions/__pycache__
	sudo chown -r `stat . -c %u:%g` migrations/versions/*


# upgrade database on running postgres
db-upgrade: build
	docker run --rm --name dazzar_upgrade --link dazzar_postgres -w /dazzar -e flask_app=/dazzar/web/web_application.py dazzar_web flask db upgrade

###########
# general #
###########

# stop all running dockers
all-stop:
	-docker stop dazzar_postgres
	-docker rm dazzar_postgres
	-docker stop dazzar_upgrade
	-docker rm dazzar_upgrade
	-docker stop dazzar_migrate
	-docker rm dazzar_migrate
	-docker stop dazzar_web
	-docker rm dazzar_web
	-docker stop dazzar_bot
	-docker rm dazzar_bot

# start all
all-start:
	docker-compose -f docker/docker-compose.yml up -d --build

# start web
web-start:
	docker-compose -f docker/docker-compose.yml up --build dazzar_web

# start bot
bot-start:
	docker-compose -f docker/docker-compose.yml up --build dazzar_bot

# build
build:
	docker-compose -f docker/docker-compose.yml build
