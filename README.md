# Progressibility
A simple web app made using Django. It is a simple to-do app with a to-do list and a simple interface for visualizing data through line charts.
Here's a [project demo](https://drive.google.com/file/d/1ovOjrn8Ki0ofOqt97jP_eNmkqVx9OSWA/view?usp=sharing).

>**Note:** All the images in the project have been taken from [Icons8](https://icons8.com/). [PlotlyJS](https://plotly.com/javascript/) is in `static/vendor`.

## Setup
It is assumed that you have already set up the database (for Django to use) for the project.
_Optionally you can set up the project in a [virtual environment](https://docs.python.org/3/library/venv.html)_.

1. Clone the repo using `git clone https://github.com/B4S1C-Coder/Progressibility.git`.
2. Install dependencies via (make sure you are in the same directory as `manage.py`) `pip install -r requirements.txt`.
3. Update the credentials for your database and the database backend in `main_site/creds.py` and `main_site/settings.py` respectively.
4. You should now be good to go! Try `python manage.py runserver` and navigate to the displayed url.

>**Note:** In _requirements.txt_ mysqlclient is there for mysql backend, if you wish to use any other backend then do install the client for the same.
