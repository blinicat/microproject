# Recrutation project

## Running app

```console
pip install -r requirements.txt
uvicorn sql_app.main:app -- reload
```
Automatic api will be available at http://127.0.0.1:8000/docs


## Running tests
```console
pytest sql_app/tests.py
```
