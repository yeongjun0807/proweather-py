from json import *

data = {}
data['posts'] = []
data['posts'].append({
    "title": "Hi",
    "Url": None,
    "Other": 123
})

print(data)

FileOpen = open("Json/test.json", "w")
dump(data, FileOpen)
FileOpen.close()