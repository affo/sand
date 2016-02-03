TEST_DIR=.

test:
	python -m unittest discover -v -s $(TEST_DIR)
