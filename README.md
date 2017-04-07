# py_vosfactures
Python wrapper to the VosFactures API

The author, Brice PARENT, is not related in any way with the company providing the VosFactures service.

This project is meant to be used in some of my own projects, and is only made available here to help other Pythonistas to get into it. Please read the source, make it yours, and provide your own guarantees if you need any.


## Python version
Created for Python 3.6, should work with many older 3.x versions. Launch the tests to be sure (and use at your own risk anyway).

## Usage

### Standalone
* Execute this in a virtual environment :

    `pip install -R requirements.txt`
    
* Create a local_settings.py file based on local_settings_model.py, and replace the values of HOST and API_TOKEN.

### In django
* Make sur all dependencies from requirements.txt are satisfied

* In your django's project's settings file, set the following two variables :
    * `VOSFACTURES_HOST` (like my_company.vosfactures.fr)
    * `VOSFACTURES_API_TOKEN`

## Launch the tests
You can find the tests in the tests package.

To launch them, launch the following command at the root of the project (in the virtualenv) :

    python -m unittest

The last line should be `OK` (and not `FAILED(errors=x)`)


## Bugs, ideas, anything else ?
Open issues, I'll try to (help you) fix it !
