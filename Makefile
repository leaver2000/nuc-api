SHELL=/bin/bash

# to see all colors, run
# bash -c 'for c in {0..255}; do tput setaf $c; tput setaf $c | cat -v; echo =$c; done'
# the first 15 entries are the 8-bit colors

# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	BLACK        := $(shell tput -Txterm setaf 0)
	RED          := $(shell tput -Txterm setaf 1)
	GREEN        := $(shell tput -Txterm setaf 2)
	YELLOW       := $(shell tput -Txterm setaf 3)
	LIGHTPURPLE  := $(shell tput -Txterm setaf 4)
	PURPLE       := $(shell tput -Txterm setaf 5)
	BLUE         := $(shell tput -Txterm setaf 6)
	WHITE        := $(shell tput -Txterm setaf 7)
	RESET := $(shell tput -Txterm sgr0)
else
	BLACK        := ""
	RED          := ""
	GREEN        := ""
	YELLOW       := ""
	LIGHTPURPLE  := ""
	PURPLE       := ""
	BLUE         := ""
	WHITE        := ""
	RESET        := ""
endif

# set target color
TARGET_COLOR := $(BLUE)

POUND = \#

.PHONY: no_targets__ info help build deploy doc
	no_targets__:

.DEFAULT_GOAL := help

colors: ## show all the colors
	@echo "${BLACK}BLACK${RESET}"
	@echo "${RED}RED${RESET}"
	@echo "${GREEN}GREEN${RESET}"
	@echo "${YELLOW}YELLOW${RESET}"
	@echo "${LIGHTPURPLE}LIGHTPURPLE${RESET}"
	@echo "${PURPLE}PURPLE${RESET}"
	@echo "${BLUE}BLUE${RESET}"
	@echo "${WHITE}WHITE${RESET}"

job1:  ## help for job 1
	@echo "job 1 started"
	@$(MAKE) job2
	@echo "job 1 finished"

job2:  ## help for job 2
	@echo "job 2"

job%:  ## help for job with wildcard
	@echo "job $@"

help:
	@echo ""
	@echo "    ${BLACK}:: ${RED}Self-documenting Makefile${RESET} ${BLACK}::${RESET}"
	@echo ""
	@echo "Document targets by adding '$(POUND)$(POUND) comment' after the target"
	@echo ""
	@echo "Example:"
	@echo "  | job1:  $(POUND)$(POUND) help for job 1"
	@echo "  | 	@echo \"run stuff for target1\""
	@echo ""
	@echo "${BLACK}-----------------------------------------------------------------${RESET}"
	@grep -E '^[a-zA-Z_0-9%-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "${TARGET_COLOR}%-30s${RESET} %s\n", $$1, $$2}'




deploy:
	@echo ""
	@echo "    ${BLACK}:: ${RED}STARTING MINIKUBE${RESET} ${BLACK}::${RESET}"
	@echo ""
	minikube start
	@echo ""
	@echo "    ${BLACK}:: ${RED}APPLYING CONFIG${RESET} ${BLACK}::${RESET}"
	@echo ""
	minikube kubectl -- apply -f ./.kube
	minikube kubectl -- get services nuc-api-svc
	@echo ""
	@echo "    ${BLACK}:: ${RED}EXPOSING PORT 8080${RESET} ${BLACK}::${RESET}"
	@echo ""
	minikube kubectl -- expose deployment nuc-api --type=NodePort --port=80
	minikube kubectl -- port-forward service/nuc-api-svc 8080

public.push:
	git add . && \
	git commit -m "making relase" && \
	git push origin master




public: public.push
	echo DONE