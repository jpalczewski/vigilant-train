#it's freestyle code copied from workbook, it doesn't work.
#w tym pliku można jednokrotnie przepuszczać każdy hasz - wtedy nie byłby potrzebny w bazie
import pymongo
import hashlib
from pathlib import Path

files = pymongo.MongoClient('mongodb://localhost:27017/').files.files

def insert_file(language, content):
        files.insert_one({'language':language, 'content':content})

#let's remove everything
files.remove({})

skipped, inserted, failed = 0,0,0
insertedFiles = set()
root = "../data/Incoming/"
p = Path(root)
allfiles = list(p.glob('*/*'))
allowed_types = ['js', 'vb', 'pl', 'php', 'cpp', 'c', 'bat', 'awk', 'py', 'rb', 'java', 'h', 'hpp', 'asm', 'cc','sh', 'scala']
#allowed_types = ['js']
translate = {'hpp':'cpp', 'h':'c', 'cc':'cpp'}


for f in allfiles:
    if f.parts[3] in allowed_types:
        with f.open(mode='r') as fh:
            try:
                content = fh.read()
                hash = hashlib.md5(content.encode()).hexdigest()
                if hash in insertedFiles:
                    skipped = skipped + 1
                    continue

                if f.parts[3] in translate.keys():
                    insert_file(translate[f.parts[3]], content)
                else:
                    insert_file(f.parts[3], content)
                inserted = inserted + 1
                insertedFiles.add(hash)
            except Exception as e:
                failed = failed + 1
                #print(f," it isn't unicode or " , e)

print("Export stats:")
print("{skipped} skipped files, {inserted} inserted into database, {failed} failed".format(skipped=skipped, inserted=inserted, failed=failed))