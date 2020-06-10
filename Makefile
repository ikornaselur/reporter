mypy:
	@poetry run mypy src/reporter/*

flake8:
	@poetry run flake8 src/reporter/*

lint: mypy flake8

test: unit_test

shell:
	@poetry run ipython

install_git_hooks:
	@ln -s /Users/axel/Projects/dict-typer/reporter/.hooks/pre-push .git/hooks/pre-push

dev:
	poetry run uvicorn reporter.main:app --reload

deploy:
	git push dokku master
