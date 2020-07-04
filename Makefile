SHELL			= /bin/bash
PYTHON_VERSION	?= python3.7

.PHONY	= init clean deploy

init: venv
	source venv/bin/activate && pip install -r requirements.txt

venv:
	virtualenv -p ${PYTHON_VERSION} venv

clean:
	rm -f impose.log

deploy: ## Requires root
	cp infra/systemd/impose.service /etc/systemd/system/
	systemctl enable impose.service
