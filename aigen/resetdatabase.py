import json, os

#adds all videos to videodata.json
file_list = os.listdir("finals")

for file in file_list:
    entry = {
            "name": file,
            "uploaded": False,
            "quality": 0,
            "checked": False,
            "length": 0,
            "creationTime": 0,
            "era": 0
        }

    with open("videodata.json", "r+") as f:
        currentData =json.load(f)
        f.seek(0)
        currentData[file] =  entry
        f.write(json.dumps(currentData, indent=4))
        print(currentData)
        f.truncate()
