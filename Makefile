debug:
	./venv/bin/python -m flask --app webapp.flaskr --debug run

run:
	./venv/bin/python -m flask --app webapp.flaskr run

run_macos:
	./venv/bin/python -m flask --app webapp.flaskr run --port 3000

run_macos_debug:
	./venv/bin/python -m flask --app webapp.flaskr --debug run --port 3000

format:
	yapf -i -r webapp/

migrate:
	python migrate.py

.PHONY: debug run format migrate run_macos run_macos_debug
