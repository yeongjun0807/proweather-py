"""이 파일은 황영준이 손수 + 직접 만들었습니다"""
import os
from json import *

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        
    except OSError:
        print("Error : Creating directory" + directory)

data = {}
data['posts'] = []
data['posts'].append({
    "title": "Hi",
    "Url": None,
    "Other": 123
})

print(data)

createFolder("Json")
FileOpen = open("file.txt", "w")
FileOpen.write("151515151")
FileOpen.close()
print('dfd')
#FileOpen = open("Json/test.json", "w")
#dump(data, FileOpen)
#FileOpen.close()
