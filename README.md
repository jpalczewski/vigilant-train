# vigilant-train
Python script which samples random github repo and saves them to database. 

## Requirements
 - requests
 - PyMongo

## Usage
Before first use create file `config.py` in root folder with content like this:
```
user = "<github-username>"
oauth = "<oauth-token-from-github>"
```