SHELL			= /bin/bash
PYTHON_VERSION	?= python3.10

.PHONY	= init clean deploy

init: venv
	source venv/bin/activate && pip install -r requirements.txt

venv:
	${PYTHON_VERSION} -m venv venv

clean:
	rm -f impose.log

deploy: ## Requires root
	cp /tmp/impose.service /etc/systemd/system/
	systemctl enable impose.service
