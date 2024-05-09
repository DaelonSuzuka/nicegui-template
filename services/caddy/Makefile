# **************************************************************************** #
# General Make configuration

# This suppresses make's command echoing. This suppression produces a cleaner output. 
# If you need to see the full commands being issued by make, comment this out.
MAKEFLAGS += -s

# **************************************************************************** #
# stack commands

STACK_NAME := nicegui_caddy

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
