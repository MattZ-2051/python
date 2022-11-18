# Python Project



## Description

Develop and program object that prepares and loads data to mapped tables/fields - beginning with Subdivisions (using collected preliminary plat document)

## How to Install and Run the Project

- Install pip on your machine

- If pipenv is not installed on your system install using `pip install pipenv`

- Once pipenv is installed clone the repository and create a shell with `pipenv shell` and run `pipenv install`

- Create .env in local repo and add values based on .env.example

- Create key.json at top level of folder this comes from your google service account (ex):

```

{

"type": "",

"project_id": "",

"private_key_id": "",

"private_key": "",

"client_email": "",

"client_id": "",

"auth_uri": "",

"token_uri": "",

"auth_provider_x509_cert_url": "",

"client_x509_cert_url": ""

}

```
## Repo Structure
```
📦src
 ┣ 📂app
 ┃ ┣ 📂google - dir for google related classes
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜storage.py - class for gc storage
 ┃ ┃ ┗ 📜vision.py - class for gc vision
 ┃ ┣ 📂models - dir containing classes for model in db
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜lpd_data.py - data processor class
 ┃ ┃ ┗ 📜subdivision.py - subdivision class
 ┃ ┣ 📂py_utils - dir for files containing classes that are used to help with data
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜associate_data.py
 ┃ ┃ ┣ 📜categorize.py
 ┃ ┃ ┣ 📜events.py
 ┃ ┃ ┣ 📜locate.py
 ┃ ┃ ┣ 📜log.py
 ┃ ┃ ┣ 📜relate.py
 ┃ ┃ ┗ 📜util.py - util class for helper funcs
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜config.py - configuration class
 ┃ ┣ 📜database.py - database class
 ┃ ┗ 📜ftp.py - ftp class
 ┗ 📜main.py - main script
 🔐key.json - file for google credentials
 ⚙.env file for env config vars

`


## Useful Documentation

-  [pipenv](https://pipenv.pypa.io/en/latest/basics/) for python virtual env

-  [my-sql-connector-python](https://dev.mysql.com/doc/dev/connector-python/8.0/installation.html) for connection and api for mysql

-  [pytest](https://docs.pytest.org/en/7.1.x/) for testing in python

-  [google-cloud-storage-python](https://googleapis.dev/python/storage/latest/index.html) for interacting with google cloud storage

-  [google-cloud-vision](https://googleapis.dev/python/vision/latest/index.html) for interacting with google cloud vision

-  [pandas](https://pandas.pydata.org/docs/)
