lint:
	tofu fmt
	black mck
	flake8 mck --ignore E501
	find . -name '*.yml' | xargs yamllint

mod_update:
	git submodule update --recursive --remote
