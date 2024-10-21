import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['SAFETENSORS_FAST_GPU']= '1'

from ai import chatGPT, promptE
from PIL import Image
import torch, random, json, time

import re, math, numpy, glob, datetime
from sub import add_subtitles
from moviepy.editor import *
from padder import CombinePad

# text to speech
from pyt2s.services import stream_elements

#length of mp3
from mutagen.mp3 import MP3

#subtitles
import assemblyai as aai

from dotenv import load_dotenv
load_dotenv()
aai.settings.api_key = os.environ.get("AAI_KEY")

from skimage.filters import gaussian

from getimg import generate

from kivy.clock import Clock

#create zoom
def zoom_in_effect(clip, zoom_ratio=0.015):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)

"""
    length - length of story in sentances
    subject - story about
    setting - in a 
    action - that
    solution + solAct - so
    plot - what happens in story 
        example: Have the first 2 sentances be about the { solution } searching
    
    imgprompt - example: f"Focus on the provided sentance. Make it descriptive and visual and breif and emphasize the characters emotions, 
                            story about {action} in {setting}, Max 10 words, only if the word dad, mom, mother, or father appear, 
                            write the words 'Muscular Human' before it otherwise do not, write that it is night and dark and " + setting
                to aid in image generation

    secondImgPrompt - SET TO NONE TO IGNORE - takes as input output from imgprompt and does another chatgpt request, 
        example: f"only if there are no Nouns or Mom in the sentance, have the first word be {subject}, only return the modified sentance"
    
    topbot - if == 'top', subtitles at top, if != 'top', then at bottom
    voice - text to speach voice
    era - value given to era field in json file
"""
def generateVideo2(savename, prompt, imgprompt, secondImgPrompt, uiUpdate, debug=False, topbot=None, voice=None):

    
    # Sets voice and topbot to random 
    if voice == None:
        voice =random.choice(['Russell', 'Justin', 'Matthew','Salli']) # Benched 'Zhiyu'

    if topbot == None and random.random() > .5:
        topbot = 'top'
    else:
        topbot = 'bottom'

    # Keeps track of how expensive video is
    totalCost = 0

    # Send prompt to chatgpt to generate story
    story = chatGPT(prompt)[0:35] # remove [0:40]
    print(story)

    # Parses story into parts which are used to generate images
    storyParsed = re.split(r"(?<!^)\s*[.|;|,|—\n]+\s*(?!$)", story)
    sent = len(storyParsed)
    remove = []
    # Merges sentances that are less than 25 characters into next sentance, manipulates storyParsed
    for i in range(sent):
        if len(storyParsed[i]) < 25 and i != sent-1:
            storyParsed[i+1] = storyParsed[i] + ", " + storyParsed[i+1]
            remove.append(storyParsed[i])
    for item in remove:
        storyParsed.remove(item)
        sent-=1

    picText = []

    print("Length: " + str(sent))

    # Generate image based on every sentance
    for i in range(sent):
        # Process the sentance to make image generation more accurate
        Clock.schedule_once(lambda dt: uiUpdate.num_update(i + 1, sent), 0)
        Clock.schedule_once(lambda dt: uiUpdate.bar_update(), 0)
        print(storyParsed[i])
        imgprompt  = promptE(f"Turn the next sentence into a text to image ai prompt which I can generate accurately with: {storyParsed[i]}. {imgprompt}") #, change any instance of son or child to {subject}
        if secondImgPrompt != None:
            imgprompt = promptE(f"In the sentance : { imgprompt }, make the following changes : { secondImgPrompt }" )
        print(imgprompt)
         
        if i==0: Clock.schedule_once(lambda dt: uiUpdate.promps_update(storyParsed[i], imgprompt), 0)

        # Generate image based on processed sentance
        filename, cost = generate(imgprompt,i)

        if i!=0: Clock.schedule_once(lambda dt: uiUpdate.promps_update(storyParsed[i], imgprompt), 0)
        Clock.schedule_once(lambda dt: uiUpdate.image_update(filename), 0)

        # Allows user to reject image and redo it
        if debug:
            userInput = input(f"\033[1;32;40m saved into {filename}, Enter new prompt, or Press Enter to Continue... \n")
            while userInput != '':
                filename, newcost = generate(userInput,i)
                cost += newcost
                userInput = input(f"\033[1;32;40m saved into {filename}, Enter new prompt, or Press Enter to Continue... \n")

        picText.append([storyParsed[i], filename])
        totalCost += cost

    # Combines story, images, and music into final video
    clips = []
    blurred_clips = []
    for i in range(sent):

        # Text to speech on story
        obj = stream_elements.StreamElements()
        data = obj.requestTTS(picText[i][0], voice)

        with open("temp/" + str(i) + '.mp3', '+wb') as file:
            file.write(data)

        audio = MP3("temp/" + str(i) + '.mp3') 
        length = audio.info.length

        # Duration buffer for end of video
        if i == sent-1:
            length = length+1

        # Creates blurred video and not blurred from images and adds audio from text to speech
        blurred_clip = zoom_in_effect(ImageClip(picText[i][1]).resize(0.1).resize(10).set_duration(length + .15), 0.1)
        clip = zoom_in_effect(ImageClip(picText[i][1]).set_duration(length + .15), 0.1)

        clip.audio = AudioFileClip("temp/" + str(i) + '.mp3')

        blurred_clips.append(blurred_clip)
        clips.append(clip)

    # Combines all blurred and non-blured clips into one w/o subtitles or music
    video = concatenate_videoclips(clips,method='compose')
    blurred_video = concatenate_videoclips(blurred_clips,method='compose')

    # Selects song and adds to video
    #song = random.choice(os.listdir("music"))
    #['Experience.wav', 'kanye.wav', 'moon.wav', 'Mystery of Love.wav', 'neon.wav', 'OMFG.wav', 'rihanna.wav', 'Sugar.wav', 'Waves.wav']
    song = random.choice(['Mystery of Love.wav','OMFG.wav','Experience.wav', 'kanye.wav', 'moon.wav','rihanna.wav','neon.wav'])#, 'Mystery of Love.wav','OMFG.wav', 'OMFG.wav', 'Sugar.wav', 'Waves.wav','Waves.wav',])

    video.audio =  CompositeAudioClip([AudioFileClip("music/" + str(song)),video.audio]).subclip(0,video.duration)
    video.write_videofile("temp/test.mp4",fps=24)
    Clock.schedule_once(lambda dt:uiUpdate.show_video("temp/test.mp4"), 0)
    blurred_video.write_videofile("temp/blurred.mp4",fps=24, codec='libx264')
    
    # Runs transcriber to sync text to speech with subtitles
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe("temp/test.mp4")
    words = transcript.export_subtitles_srt(chars_per_caption=18)
    f = open("temp/subtitles.srt","a")
    f.write(words)
    f.close()
    outputSub = "temp/withSubs.mp4"

    # Adds subtitles to not blurred video and combines non blurred to blurred to make final video
    add_subtitles("temp/test.mp4", "temp/subtitles.srt", outputSub, topbot)
    CombinePad(outputSub, "temp/blurred.mp4", "finals/" + savename + ".mp4")

    Clock.schedule_once(lambda dt: uiUpdate.final_video("finals/" + savename + ".mp4"), 0)
    time.sleep(2)
    # Clean temp files
    files = glob.glob('temp/*')
    for f in files:
        os.remove(f)
    name =  savename
    
    # Set data of specific video
    entry = {
            "name": name + ".mp4",
            "uploaded": False,
            "quality": 0,
            "checked": False,
            "length": math.floor(video.duration),
            "creationTime": str(datetime.datetime.now().year) +"-" + str(datetime.datetime.now().month) +"-" + str(datetime.datetime.now().day) + "-" + str(datetime.datetime.now().hour) +"-" + str(datetime.datetime.now().minute),
        }

    # Saves video to database
    with open("videodata.json", "r+") as f:
        currentData =json.load(f)
        f.seek(0)
        currentData[name + ".mp4"] =  entry
        f.write(json.dumps(currentData, indent=4))
        f.truncate()

    print("TOTAL COST OF VIDEO IS : " + str(totalCost) + "$")
    return "finals/" + savename