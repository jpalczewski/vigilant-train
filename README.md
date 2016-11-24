# vigilant-train
Python script which samples random github repo and saves them to database. 

## Requirements
 - requests
 - click

## Usage
Before first use create file `config.py` in root folder with content like this:
```
user = "<github-username>"
oauth = "<oauth-token-from-github>"
```

And installing all files provided by `requirements.txt` is nice idea, too.
```
$ pip install --user -r requirements.txt
```

## Known limitations
It's only supporting utf-8 files now.