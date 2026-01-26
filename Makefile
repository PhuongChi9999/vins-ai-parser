PYTEST := PYTHONPATH=./ uv tool run --with bs4 pytest
MAIN := uv run main.py

all:
	$(MAIN)

test:
	@echo "Running tests..."
ifndef NAME
	$(PYTEST)
else
	$(PYTEST) ./tests/$(NAME).py
endif


.PHONY: all test
