lint:
	tofu fmt
	black .
	flake8 mck/*.py
