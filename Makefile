debug:
	./venv/bin/python -m flask --app webapp.flaskr --debug run

run:
	./venv/bin/python -m flask --app webapp.flaskr run

format:
	yapf -i -r webapp/

.PHONY: debug run format
