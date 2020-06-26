SHELL			= /bin/bash
PYTHON_VERSION	?= python3.7

.PHONY	= init

init:
	virtualenv -p ${PYTHON_VERSION} venv && \
		source venv/bin/activate && \
		pip install -r requirements.txt
