import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['SAFETENSORS_FAST_GPU']= '1'

from ai import chatGPT, promptE
from PIL import Image
import torch, random, json, time, asyncio, aiohttp, base64, io

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

from getimg import generate, get_tasks_photo, get_tasks_prompt

from kivy.clock import Clock

import asyncio

class GenerateVideo:
    def __init__(self, savename, prompt, imgprompt, secondImgPrompt, uiUpdate, size, debug=False, topbot=None, voice=None):
        self.uiUpdate = uiUpdate
        if voice == None:
            self.voice =random.choice(['Russell', 'Justin', 'Matthew','Salli']) # Benched 'Zhiyu'
        else:
            self.voice = voice
        if topbot == None and random.random() > .5:
            self.topbot = 'top'
        else:
            self.topbot = 'bottom'
        self.debug = debug
        self.savename = savename
        self.prompt = prompt
        self.imgprompt = imgprompt
        self.secondImgPrompt = secondImgPrompt
        self.size = size
        # After initialized
        self.sent = 0
        self.totalCost = 0
        self.sent = 0
        self.picText = []

    def create_images(self):
        # Send prompt to chatgpt to generate story
        story = chatGPT(self.prompt) # remove [0:30]
        print(story)

        # Parses story into parts which are used to generate images
        storyParsed = re.split(r"(?<!^)\s*[.|;|,|—\n]+\s*(?!$)", story)
        self.sent = len(storyParsed)
        remove = []
        # Merges sentances that are less than 25 characters into next sentance, manipulates storyParsed
        for i in range(self.sent):
            if len(storyParsed[i]) < 25 and i != self.sent-1:
                storyParsed[i+1] = storyParsed[i] + ", " + storyParsed[i+1]
                remove.append(storyParsed[i])
        for item in remove:
            storyParsed.remove(item)
            self.sent-=1

        print("Length: " + str(self.sent))

        #Clock.schedule_once(lambda dt: self.uiUpdate.image_update(filename), 0)
        self.fetch_photos(storyParsed)

    def fetch_photos(self,storyParsed):
        asyncio.run(self.get_image_prompts(storyParsed))
        #if i==0: Clock.schedule_once(lambda dt: self.uiUpdate.promps_update(storyParsed[i], self.imgprompt), 0)

        # Generate image based on processed sentance
        asyncio.run(self.get_photos(self.prompt_results))
        
        for i in range(len(self.image_results)):
            decoded_img = base64.b64decode(self.image_results[i]["image"])
            img = Image.open(io.BytesIO(decoded_img))
            img.thumbnail((1080,1080), Image.LANCZOS)
            img.save(f'temp/{i}','JPEG')
            self.picText.append([storyParsed[i], f'temp/{i}',self.prompt_results[i]])
            self.totalCost += self.image_results[i]["cost"]
        Clock.schedule_once(lambda dt: self.uiUpdate.display_images(self.picText), 0)

    def fetch_photo(self,prompt,filename):
        asyncio.run(self.get_photos([prompt]))
        decoded_img = base64.b64decode(self.image_results[0]["image"])
        img = Image.open(io.BytesIO(decoded_img))
        img.thumbnail((1080,1080), Image.LANCZOS)
        img.save(filename,'JPEG')
        self.totalCost += self.image_results[0]["cost"]
        Clock.schedule_once(lambda dt: self.uiUpdate.regenerated(), 0)    

    async def get_photos(self,storyParsed):
        results = []
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks_photo(session, storyParsed)
            responses = await(asyncio.gather(*tasks))
            for response in responses:
                results.append(await response.json())
        self.image_results = results

    async def get_image_prompts(self,storyParsed):
        results = []
        
        async with aiohttp.ClientSession() as session:
            tasks = get_tasks_prompt(session, storyParsed, self.imgprompt, self.secondImgPrompt)
            responses = await(asyncio.gather(*tasks))
            for response in responses:
                results.append(await response.json())
        
        self.prompt_results = []
        for item in results:
            print(item["choices"][0]["message"]["content"] + "  GENERATED")
            self.prompt_results.append(item["choices"][0]["message"]["content"])
    

    def create_videos(self):
        # Combines story, images, and music into final video
        clips = []
        blurred_clips = []
        for i in range(self.sent):

            # Text to speech on story
            obj = stream_elements.StreamElements()
            print(self.picText[i][0])
            data = obj.requestTTS(self.picText[i][0], self.voice)

            with open("temp/" + str(i) + '.mp3', '+wb') as file:
                file.write(data)

            audio = MP3("temp/" + str(i) + '.mp3') 
            length = audio.info.length

            # Duration buffer for end of video
            if i == self.sent-1:
                length = length+1

            # Creates blurred video and not blurred from images and adds audio from text to speech
            blurred_clip = zoom_in_effect(ImageClip(self.picText[i][1]).resize(0.1).resize(10).set_duration(length + .15), 0.1)
            clip = zoom_in_effect(ImageClip(self.picText[i][1]).set_duration(length + .15), 0.1)

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
        self.duration = video.duration
        Clock.schedule_once(lambda dt:self.uiUpdate.show_video("temp/test.mp4"), 0)
        blurred_video.write_videofile("temp/blurred.mp4",fps=24, codec='libx264')
        self.create_final()
       
    def create_final(self):
        # Runs transcriber to sync text to speech with subtitles
        transcriber = aai.Transcriber()

        transcript = transcriber.transcribe("temp/test.mp4")
        words = transcript.export_subtitles_srt(chars_per_caption=18)
        f = open("temp/subtitles.srt","a")
        f.write(words)
        f.close()
        outputSub = "temp/withSubs.mp4"

        # Adds subtitles to not blurred video and combines non blurred to blurred to make final video
        add_subtitles("temp/test.mp4", "temp/subtitles.srt", outputSub, self.topbot, self.size)
        CombinePad(outputSub, "temp/blurred.mp4", "finals/" + self.savename + ".mp4")

        Clock.schedule_once(lambda dt: self.uiUpdate.final_video("finals/" + self.savename + ".mp4"), 0)
        time.sleep(1)
        # Clean temp files
        files = glob.glob('temp/*')
        for f in files:
            os.remove(f)

        # Set data of specific video
        entry = {
                "name": self.savename + ".mp4",
                "uploaded": False,
                "quality": 0,
                "checked": False,
                "length": math.floor(self.duration),
                "creationTime": str(datetime.datetime.now().year) +"-" + str(datetime.datetime.now().month) +"-" + str(datetime.datetime.now().day) + "-" + str(datetime.datetime.now().hour) +"-" + str(datetime.datetime.now().minute),
            }

        # Saves video to database
        with open("videodata.json", "r+") as f:
            currentData =json.load(f)
            f.seek(0)
            currentData[self.savename + ".mp4"] =  entry
            f.write(json.dumps(currentData, indent=4))
            f.truncate()

        print("TOTAL COST OF VIDEO IS : " + str(self.totalCost) + "$")
        return "finals/" + self.savename
    
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
    def fetch_photos(self,storyParsed):
        for i in range(self.sent):
            # Process the sentance to make image generation more accurate
            Clock.schedule_once(lambda dt: self.uiUpdate.num_update(i + 1, self.sent), 0)
            Clock.schedule_once(lambda dt: self.uiUpdate.bar_update(), 0)
            print(storyParsed[i])
            self.imgprompt  = promptE(f"Turn the next sentence into a text to image ai prompt which I can generate accurately with: {storyParsed[i]}. {self.imgprompt}") #, change any instance of son or child to {subject}
            if self.secondImgPrompt != None:
                self.imgprompt = promptE(f"In the sentance : { self.imgprompt }, make the following changes : { self.secondImgPrompt }" )
            print(self.imgprompt)
            
            if i==0: Clock.schedule_once(lambda dt: self.uiUpdate.promps_update(storyParsed[i], self.imgprompt), 0)

            # Generate image based on processed sentance
            filename, cost = generate(self.imgprompt,i)

            if i!=0: Clock.schedule_once(lambda dt: self.uiUpdate.promps_update(storyParsed[i], self.imgprompt), 0)
            Clock.schedule_once(lambda dt: self.uiUpdate.image_update(filename), 0)

            # Allows user to reject image and redo it
            if self.debug:
                userInput = input(f"\033[1;32;40m saved into {filename}, Enter new prompt, or Press Enter to Continue... \n")
                while userInput != '':
                    filename, newcost = generate(userInput,i)
                    cost += newcost
                    userInput = input(f"\033[1;32;40m saved into {filename}, Enter new prompt, or Press Enter to Continue... \n")

            self.picText.append([storyParsed[i], filename])
            self.totalCost += cost
            self.create_videos()
    """