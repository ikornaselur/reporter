mypy:
	@poetry run mypy src/reporter/* tests/*

flake8:
	@poetry run flake8 src/reporter/* tests/*

lint: mypy flake8

test: unit_test

unit_test:
	@poetry run pytest tests/unit -xvvs

shell:
	@poetry run ipython

install_git_hooks:
	@ln -s /Users/axel/Projects/dict-typer/reporter/.hooks/pre-push .git/hooks/pre-push
