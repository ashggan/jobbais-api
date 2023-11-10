source venv/Scripts/activate

<!-- ######################################################### -->

pip list
pip freeze > requirements.txt
pip uninstall -r requirements.txt -y

pip install -r requirements.txt

<!-- ######################################################### -->

flask --app main run --reload

<!-- ######################################################### -->

gcloud create app --project=[]

gcloud components install app-engine-python

gcloud app deploy
