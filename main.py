import os
import json

with open(os.getcwd()+"/config.json") as json_file:
    data = json.load(json_file)

print(data)
