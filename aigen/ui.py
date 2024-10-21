from tkinter import *
import os, json, random, math
from os import startfile
# create root window
root = Tk()

file_list = os.listdir("finals")
unranked = []
ranked = []

f = open("videodata.json", "r") 
currentData = json.load(f)
for key in currentData.keys():
    if currentData[key]['quality'] == 0 and currentData[key]['uploaded'] == False and currentData[key]['era'] == 0:
        unranked.append(key)
    else:
        ranked.append(key)


# root window title and dimension
root.title("Quality Assurance")
# Set geometry (widthxheight)
root.geometry('550x100')

lbl = Label(root, text = "No Videos")
lbl.grid()

entry = Entry(root, width= 42)
entry.place(relx= .5, rely= .5, anchor= CENTER)



def next():        
    entry.delete(0, 'end')
    index = math.floor(random.random() * len(unranked))
    lbl.configure(text = unranked[index])
    startfile(os.path.abspath("finals/" + unranked[index]))

def rate():
    video = lbl.cget("text")
    currentData[video]['quality'] = entry.get()
    currentData[video]['checked'] = True
    unranked.remove(video)
    ranked.append(video)

    with open("videodata.json", "r+") as f:
        data =json.load(f)
        f.seek(0)
        data[video]['quality'] = entry.get()
        data[video]['checked'] = True
        f.write(json.dumps(data, indent=4))
        f.truncate()

    next()

def uploaded():
    video = lbl.cget("text")
    currentData[video]['uploaded'] = True
    unranked.remove(video)
    ranked.append(video)

    with open("videodata.json", "r+") as f:
        data =json.load(f)
        f.seek(0)
        data[video]['uploaded'] = True
        f.write(json.dumps(data, indent=4))
        f.truncate()

    next()

def delete():
    video = lbl.cget("text")
    os.remove(os.path.abspath("finals/" + video))
    next()

btn = Button(root, text = "rate" ,
            fg = "blue", command=rate)
btn.grid(column=1, row=0)
btn = Button(root, text = "next" ,
            fg = "green", command=next)
btn.grid(column=2, row=0)
btn = Button(root, text = "mark uploaded" ,
            fg = "yellow", command=uploaded)
btn.grid(column=3, row=0)
btn = Button(root, text = "DELETE VIDEO" ,
            fg = "red", command=delete)
btn.grid(column=4, row=0)

# all widgets will be here

next()


# Execute Tkinter
root.mainloop()