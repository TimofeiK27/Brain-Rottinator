import json, os

f = open("videodata.json", "r") 
currentData = json.load(f)
for key in currentData.keys():
    if currentData[key]['quality']!='' and int(currentData[key]['quality']) <= 4 and int(currentData[key]['quality']) != 0:
        print('deleted ' + key)
        os.remove(os.path.abspath("finals/" + key))