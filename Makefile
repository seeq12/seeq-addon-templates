# Get the local directory (where the Makefile is located)
LOCAL_DIR := $(CURDIR)
VENV := $(LOCAL_DIR)/.venv
UTILS := $(LOCAL_DIR)/{{project_name}}/_dev_tools/utils.py

create_env:
	@echo "\n********* Creating Virtual Environment **********************"
	@echo "  Creating virtual environment in $(VENV)"
	python entrypoint.py
	@echo "\n************************************************************"
	@echo "\nVirtual environment created. To activate the environment, run: \n"
	@echo "  source .venv/bin/activate"
	@echo "\n************************************************************"

addonEnv:
	@make create_env --no-print-directory
