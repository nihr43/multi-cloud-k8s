lint: mod_update
	tofu fmt
	black .
	flake8 mck --ignore E501

mod_update:
	git submodule update --recursive --remote
