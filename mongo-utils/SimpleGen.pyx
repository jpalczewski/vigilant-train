# cython: profile=True
import pymongo
from collections import Counter
from multiprocessing import Pool, TimeoutError
import re

#from libcpp.map cimport map
#from libcpp.string cimport string
#from libcpp.vector cimport vector
#from cython.operator cimport dereference, preincrement



def generate_simple_stat(dict f):
    cdef int count
    cdef str char
    cdef set uniqueTokens
    cdef str t
    cdef str cleaned
    cdef dict simple_stat
    cdef list allTokens
    if 'stats' in f.keys():
        if 'char_occurrences' in f['stats'].keys() and 'token_occurrences' in f['stats'].keys():
            return

    if 'stats' not in f.keys():
        f['stats'] = {}

    files = pymongo.MongoClient('mongodb://localhost:27017/').files.files

    #calculate
    pattern = re.compile('(\$|\.|\0)')
    cleaned = pattern.sub("", f['content'])

    c = Counter(cleaned)
    simple_stat = {'char_occurrences': {}, 'token_occurrences': {}}
    for char, count in c.items():
        simple_stat['char_occurrences'][char] = count

    allTokens = cleaned.split()
    uniqueTokens = set(allTokens)
    for t in uniqueTokens:
        simple_stat['token_occurrences'][t] = allTokens.count(t)
    f['stats']['simple'] = simple_stat
    files.replace_one({'_id': f['_id']}, f)


def run():
    allFiles = pymongo.MongoClient('mongodb://localhost:27017/').files.files.find({})
    cdef list listAllFiles = list(allFiles)
    with Pool(processes=4) as pool:
        pool.map(generate_simple_stat, listAllFiles)


