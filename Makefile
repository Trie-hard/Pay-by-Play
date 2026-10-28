PYTHON ?= C:/Users/niksh/AppData/Local/Programs/Python/Python312/python.exe

.PHONY: install pipeline validate app

install:
	$(PYTHON) -m pip install -r requirements.txt

pipeline:
	$(PYTHON) -m src.pipeline

validate:
	$(PYTHON) scripts/validate.py

app:
	$(PYTHON) -m streamlit run app/streamlit_app.py
