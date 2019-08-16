import os
import json
from DAL.UnitOfWork.UnitOfWork import UnitOfWork

with open(os.getcwd()+"/config.json") as json_file:
    data = json.load(json_file)

print(data)
