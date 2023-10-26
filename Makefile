lint:
	tofu fmt
	black .
	flake8 mck --ignore E501
