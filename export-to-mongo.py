#it's freestyle code copied from workbook, it doesn't work.
#w tym pliku można jednokrotnie przepuszczać każdy hasz - wtedy nie byłby potrzebny w bazie
import pymongo
import os
from pathlib import Path

client = pymongo.MongoClient('mongodb://localhost:27017/')
files = client.files.files

def insert_file(language, content):
        files.insert_one({'language':language, 'content':content})


root = "./data/Incoming/"
p = Path(root)
allfiles = list(p.glob('*/*'))

allowed_types = ['js', 'vb', 'pl', 'php', 'cpp', 'c', 'bat', 'awk', 'py', 'rb', 'java', 'h', 'hpp', 'asm', 'cc','sh', 'scala']
translate = {'hpp':'cpp', 'h':'c', 'cc':'cpp'}
root = "./data/Incoming/"
p = Path(root)
allfiles = list(p.glob('*/*'))
for f in allfiles:
    if f.parts[2] in allowed_types:
        with f.open(mode='r') as fh:
            try:
                content = fh.read()
                if f.parts[2] in translate.keys():
                    insert_file(translate[f.parts[2]], content)
                else:
                    insert_file(f.parts[2], content)
            except Exception as e:
                print(f," to nie unikod lub " , e)