uvicorn main:app --port 8080 --reload
uvicorn main:app --host 0.0.0.0 --port 8000
source myenv/Scripts/activate

pip list
pip freeze > requirements.txt
pip uninstall -r requirements.txt -y

pip install -r requirements.txt
