lint:
	@pipenv run black .
	@pipenv run isort .

logs:
	@cat ~/.local/share/qtile/qtile.log | grep "====>"
