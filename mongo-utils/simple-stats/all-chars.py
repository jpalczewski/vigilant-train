import pymongo
import matplotlib.pyplot as plt
import plotly
from collections import defaultdict
import json

client = pymongo.MongoClient('mongodb://localhost:27017/')
files = client.files.files
char_per_language = {}

languages = files.distinct("language")
for language in languages:
    char_per_language[language] = defaultdict(int)
    for file in files.find({'language':language}):
        for char, count in file['stats']['simple']['char_occurrences'].items():
            char_per_language[language][char] += count

sum_per_lang = {}
for l in languages:
    sum_per_lang[l] = sum(char_per_language[l].values())

with open ('spl.json', 'w') as f:
    json.dump(sum_per_lang, f)

#for title, data_dict in char_per_language.items():
#    x = list(data_dict.keys())
#   y = list(data_dict.values())
#    plt.figure()
#    plt.plot(x,y)
#    plt.title(title)

#plt.show()

