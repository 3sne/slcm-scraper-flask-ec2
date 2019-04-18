## Backend for SLcM Scraper

* This project has some dependencies that must be installed to successfully run the scripts. They are mentioned in `requirements.txt`
<br>

* It is also recommended to create your own local python environment and load these dependencies on that venv, so that you don't end up in python version hell.<br>

### To setup your environment:

Assuming python3 and pip/pip3 are already installed on your machine, run

1. Install python virtual environment packages
```
$ sudo pip3 install virtualenv 
```

2. Create a virtual environment in your project's root dir
```
$ python3 -m venv venv_name
```

3. Activate the venv (All the modules will be referenced from this environment now)
```
$ source venv_name1/bin/activate
```

4. Install dependencies for this project
```
(venv_name) $ pip install -r requirements.txt
```

5. To deactivate venv later on (brings back normal prompt)
```
(venv_name) $ deactivate
```
