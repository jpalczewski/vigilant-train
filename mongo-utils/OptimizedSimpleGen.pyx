import pymongo
from collections import Counter
from multiprocessing import Pool, TimeoutError
import re

def generate_simple_stat(dict f):
    cdef dict c_char
    cdef dict c_token
    cdef str cleaned
    if 'stats' in f.keys():
        if 'char_occurrences' in f['stats'].keys() and 'token_occurrences' in f['stats'].keys():
            return f

    if 'stats' not in f.keys():
        f['stats'] = {}

    #calculate
    pattern = re.compile('(\$|\.|\0)')
    cleaned = pattern.sub("", f['content'])

    c_char = dict(Counter(cleaned).items())
    c_token = dict(Counter(cleaned.split()).items())

    f['stats']['simple'] = {'char_occurrences': c_char, 'token_occurrences': c_token}
    return f


def run():
    files = pymongo.MongoClient('mongodb://localhost:27017/').files.files
    allFiles = files.find({})
    listAllFiles = list(allFiles)
    results = []
    with Pool(processes=4) as pool:
        results = pool.map(generate_simple_stat, listAllFiles)

    files.remove({})
    files.insert_many(results, ordered=False)
#    for r in results:
#        files.replace_one({'_id': r['_id']}, r)
