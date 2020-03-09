# Boggle Game Backend
Boggle is a word game that is played on a 4x4 board with 16 letter tiles. 
The goal is to find as many words as possible given a time constraint.  

This project was created using Django framework


## Deployment

- Clone the project `git clone https://github.com/zhuoli1987/Boggle-django.git`
- CD to the Project Directory `cd Boggle-django`
- Create a virtual environment `virtualenv <name>`
- Activate (mac) `source <name>/bin/activate`
- Run `pip install -r requirements.txt`
- Run `./manage.py makemigrations`
- Run `./manage.py migrate`
- Run Application `./manage.py runserver` this will run the application on port 8000

## Run tests

- CD to the the top folder
- Run `./manage.py test` (make sure your venv is activated)


