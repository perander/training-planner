## How to install

### Locally

You can download the source code as ZIP from https://github.com/perander/training-planner or clone it on your machine with

`git clone git@github.com:perander/training-planner.git`

Providing you have python3 and pip, you can create a virtual environment with

`python3 -m venv venv`

and activate it with 

`source venv/bin/activate` 

You can then install dependencies with

`pip install -r requirements.txt`.

The application should start on localhost with

`python3 run.py`.

### In Heroku

Providing you have the project as a git repository on your machine, as well as a Heroku account and the command line tools for Heroku, you can create a name for the app with

`heroku create my-app-name`.

Add Heroku as a remote with

`git remote add https://git.heroku.com/my-app-name.git`
 
Then you can push the local version to Heroku remote with

`git push heroku master`.