# you can lint the rules in this Makefile by running
# go run github.com/mrtazz/checkmake/cmd/checkmake@latest Makefile
# (you need to have Go installed for this to work)
.DEFAULT_GOAL := help

help: ## Show this help
	@echo "Available commands:"
	#@echo "MAKEFILE_LIST = $(MAKEFILE_LIST)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'


dspy-clear-cache: ## Clear dspy cache
	@cd src && pdm run python -m scripts.dspy_clear_cache