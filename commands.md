uvicorn main:app --port 8080 --reload
uvicorn main:app --host 0.0.0.0 --port 8000
source venv/Scripts/activate

pip list
pip freeze > requirements.txt
pip uninstall -r requirements.txt -y

pip install -r requirements.txt
python.exe -m pip i pip install --upgrade pip

C:\Users\alsfa\jobbais-api\myenv\Scripts\python.exe -m pip install --upgrade pip
