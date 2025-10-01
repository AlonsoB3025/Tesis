PYTHON ?= python

.PHONY: run ingest preprocess train predict

run:
	$(PYTHON) -m src.run_pipeline

ingest:
	$(PYTHON) -m src.ingest

preprocess:
	$(PYTHON) -m src.preprocess

train:
	$(PYTHON) -m src.train

predict:
	$(PYTHON) -m src.predict
