SHELL			?= /bin/bash
PYTHON_VERSION	?= python3.7

.PHONY	= init clean deploy

init:
	virtualenv -p ${PYTHON_VERSION} venv && \
		source venv/bin/activate && \
		pip install -r requirements.txt

clean:
	rm -f impose.log

deploy: ## Requires root
	cp infra/systemd/impose.service /etc/systemd/system/
