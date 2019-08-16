import os
import json

with open(os.path.dirname(os.path.realpath(__file__))+"/config.json") as json_file:
    data = json.load(json_file)

print(data)
