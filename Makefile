# **************************************************************************** #
# General Make configuration

# This suppresses make's command echoing. This suppression produces a cleaner output. 
# If you need to see the full commands being issued by make, comment this out.
MAKEFLAGS += -s

# Fix bad built-in make behaviors
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# **************************************************************************** #
# Development Targets

# run the application
run:
	echo "run"

compile:
	uv pip compile pyproject.toml -o requirements.txt

sync:
	uv pip sync requirements.txt


# **************************************************************************** #
# docker commands

STACK_NAME := nicegui_template

# build the application's docker image locally
image:
	docker build . -t $(STACK_NAME)

# create the application's network
network:
	docker network create --driver=overlay --attachable $(STACK_NAME)_network

# deploy the application's docker stack
deploy:
	docker stack deploy -c stack.yml $(STACK_NAME) --detach=true

# delete the application's docker stack
undeploy:
	docker stack rm $(STACK_NAME)

# delete then deploy the stack
redeploy: undeploy deploy

# check the status of the stack
ps:
	docker stack ps $(STACK_NAME) --no-trunc
