# **************************************************************************** #
# General Make configuration

# This suppresses make's command echoing. This suppression produces a cleaner output. 
# If you need to see the full commands being issued by make, comment this out.
MAKEFLAGS += -s

# Fix bad built-in make behaviors
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Use > instead of \t
.RECIPEPREFIX = >

# **************************************************************************** #
# Development Targets

# run the application
run: venv
> $(VENV_PYTHON) src/main.py

# build the application's docker image locally
image:
> docker build . -t nicegui_template

# **************************************************************************** #
# stack commands

STACK_NAME := nicegui_template

# create the application's network
network:
> docker network create --driver=overlay --attachable nicegui_network

# deploy the application's docker stack
deploy:
> docker stack deploy -c stack.yml $(STACK_NAME) --detach=true

# delete the application's docker stack
undeploy:
> docker stack rm $(STACK_NAME)

# delete then deploy the stack
redeploy: undeploy deploy

# check the status of the stack
ps:
> docker stack ps $(STACK_NAME) --no-trunc

# **************************************************************************** #
# python venv settings
VENV_NAME := .venv
REQUIREMENTS := requirements.txt

VENV_DIR := $(VENV_NAME)
PYTHON := python

ifeq ($(OS),Windows_NT)
	VENV := $(VENV_DIR)/Scripts
else
	VENV := $(VENV_DIR)/bin
endif

VENV_CANARY_DIR := $(VENV_DIR)/canary
VENV_CANARY_FILE := $(VENV_CANARY_DIR)/$(REQUIREMENTS)
VENV_TMP_DIR := $(VENV_DIR)/tmp
VENV_TMP_FREEZE := $(VENV_TMP_DIR)/freeze.txt
VENV_PYTHON := $(VENV)/$(PYTHON)
VENV_PYINSTALLER := $(VENV)/pyinstaller
RM := rm -rf 
CP := cp

# Add this as a requirement to any make target that relies on the venv
.PHONY: venv
venv: $(VENV_DIR) $(VENV_CANARY_FILE)

# Create the venv if it doesn't exist
$(VENV_DIR):
> uv venv

# Update the venv if the canary is out of date
$(VENV_CANARY_FILE): $(REQUIREMENTS)
> uv pip install -r $(REQUIREMENTS)
> -$(RM) $(VENV_CANARY_DIR)
> -mkdir $(VENV_CANARY_DIR)
> -$(CP) $(REQUIREMENTS) $(VENV_CANARY_FILE)

# forcibly update the canary file
canary: $(VENV_CANARY_DIR)
> -$(RM) $(VENV_CANARY_DIR)
> -mkdir $(VENV_CANARY_DIR)
> $(CP) $(REQUIREMENTS) $(VENV_CANARY_FILE)

# update requirements.txt to match the state of the venv
freeze_reqs: venv
> $(VENV_PYTHON) -m pip freeze > $(REQUIREMENTS)

# try to update the venv - expirimental feature, don't rely on it
update_venv: venv
> uv pip sync $(REQUIREMENTS)
> -$(RM) $(VENV_CANARY_DIR)
> -mkdir $(VENV_CANARY_DIR)
> -$(CP) $(REQUIREMENTS) $(VENV_CANARY_FILE)

# remove all packages from the venv
clean_venv:
> $(RM) $(VENV_CANARY_DIR)
> mkdir $(VENV_TMP_DIR)
> uv pip freeze > $(VENV_TMP_FREEZE)
> uv pip uninstall -y -r $(VENV_TMP_FREEZE)
> $(RM) $(VENV_TMP_DIR)

# clean the venv and rebuild it
reset_venv: clean_venv update_venv
