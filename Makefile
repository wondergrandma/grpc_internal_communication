format:
	isort .
	black .

lint:
	flake8 .

clean:
	pyclean -v .