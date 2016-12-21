import pymongo
import plotly
import plotly.graph_objs as go


client = pymongo.MongoClient('mongodb://localhost:27017/')
files = client.files.files
sizes = {}

languages = files.distinct("language")
for l in languages:
    sizes[l] = files.find({'language':l}).count()

print(sizes)


plotly.offline.plot({
    'data':[{'labels':list(sizes.keys()), 'values': list(sizes.values()), 'type':'pie'}]
})