PYTEST := PYTHONPATH=./ uv tool run --with bs4 pytest
DATASET := uv run dataset.py
CLEAN := uv run clean.py
LEARN := uv run learn.py

all:
	$(DATASET)
	$(CLEAN)
	$(LEARN)

clean:
	$(CLEAN)

dataset:
	$(DATASET)

learn:
	$(LEARN)

test:
	@echo "Running tests..."
ifndef NAME
	$(PYTEST)
else
	$(PYTEST) ./tests/$(NAME).py
endif


.PHONY: all dataset clean learn test
