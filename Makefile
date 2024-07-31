# Get the local directory (where the Makefile is located)
LOCAL_DIR := $(CURDIR)
VENV := $(LOCAL_DIR)/.venv

addonEnv:
	#python entrypoint.py
	@echo "\n|********* Virtual Environment Created *********|"
	@echo "  To activate the environment, run: \n"
	@echo "      source $(VENV)/bin/activate"
	@echo "\n|***********************************************|"
