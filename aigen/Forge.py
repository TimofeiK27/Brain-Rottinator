import os, time, threading, multiprocessing as mp, threading

os.environ["KIVY_LOG_MODE"] = "PYTHON"
os.environ["KIVY_VIDEO"] = "ffpyplayer"
from dotenv import load_dotenv
import kivy, time
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.image import Image

from kivy.uix.video import Video
from ffpyplayer.player import MediaPlayer


from genarotter import CreatePrompt
#Window.clearcolor = (1, 1, 1, 1)

from kivy.config import Config
Config.set('kivy', 'video', 'ffpyplayer')

from kivy.clock import Clock

class InputWindow(Screen):
    subject = ObjectProperty(None)
    setting = ObjectProperty(None)
    emotion = ObjectProperty(None)
    action = ObjectProperty(None)
    solution = ObjectProperty(None)
    length = ObjectProperty(None)
    voice = ObjectProperty(None)

    def forge(self):
        sm.current = "gen"
        prompt = CreatePrompt(self.subject.text, self.setting.text, self.emotion.text, self.action.text, self.solution.text, self.length.text)
        sm.get_screen("gen").Generate(prompt,self.subject.text)

        label = Label(text=f'Prompt:\n\n {prompt}')
        label.bind(width=lambda *x: label.setter('text_size')(label, (label.width * .92, None)))
        
        pop = Popup(title='Generating Video',
                    content=label,
                    size_hint=(None, None), size=(400, 400))

        pop.open()

    def clear(self):
        self.subject.text=''
        self.setting.text=''
        self.emotion.text=''
        self.action.text=''
        self.solution.text=''
        self.length.text=''




class GenWindow(Screen):
    def back_btn(self):
        self.ids.progress_bar.value = 0
        sm.current = "main"
        image = self.ids.curimage
        image.source = 'placeholder.jpg'

    def Generate(self, prompt, subject):
        from gen import generateVideo2
        imgprompt = f"""make it descriptive and visual and breif about {subject}, Max 10 words only use 10 words, only return edited sentance"""
        secondImgPrompt = f"""Rewrite with only 10 words, only return edited sentance"""
        p1 = threading.Thread(target=generateVideo2, args=("Test", prompt, imgprompt, secondImgPrompt, self))
        p1.start()

    def bar_update(self):
        self.ids.progress_bar.value = 0
        Clock.schedule_interval(self.update_progress_bar, .088)

    def update_progress_bar(self, dt):
        progress_bar = self.ids.progress_bar
        if progress_bar.value >= 100:
            Clock.unschedule(self.update_progress_bar)
        else:
            progress_bar.value += 1

    def image_update(self, filename):
        image = self.ids.curimage
        image.source = f'{filename}'
        image.reload() 
        self.ids.progress_bar.value = 100

    def promps_update(self, sent, img_pt):
        sentence = self.ids.sentence
        image_prompt = self.ids.image_prompt
        sentence.text = sent
        image_prompt.text = img_pt

    def num_update(self, num, den):
        sentence = self.ids.img_num
        sentence.text = f'Generating Image {num} of {den}'

    def show_video(self, filename):
        sm.transition = SlideTransition(direction='up')
        sm.current = "video"
        sm.get_screen("video").display_video(filename)
        self.ids.curimage.source = 'placeholder.jpg'
        self.ids.curimage.reload()
        self.promps_update("Fetching Story...", "Generating Image Prompt...")
        self.num_update(1, "*")
        self.ids.progress_bar.value=0

    def final_video(self,filename):
        sm.get_screen("video").final_video(filename)

class VideoWindow(Screen):
    def back_btn(self):
        self.ids.progress_bar.value = 0
        sm.current = "main"
        video = self.ids.curvideo
        video.source = ''

    def bar_update(self):
        self.ids.progress_bar.value = 0
        Clock.schedule_interval(self.update_progress_bar, .088)

    def update_progress_bar(self, dt):
        progress_bar = self.ids.progress_bar
        if progress_bar.value >= 100:
            Clock.unschedule(self.update_progress_bar)
        else:
            progress_bar.value += 1

    def display_video(self, filename):
        self.bar_update()
        self.ids.curvideo.source=filename
        self.ids.curvideo.state='play'
        self.ids.curvideo.reload()

    def final_video(self, filename):
        self.ids.curvideo.state = 'stop'  # Stop the video playback
        self.ids.curvideo.source = ''  # Clear the video source
        sm.transition = SlideTransition(direction='right')
        sm.current = "final"
        sm.get_screen("final").display_final(filename)

class FinalWindow(Screen):
    def back_btn(self):
        sm.transition = SlideTransition(direction='down')
        sm.current = "main"
        video = self.ids.curvideo
        video.state='pause'
        video.source = ''
        self.filename = None
        self.ids.video_name.text = ''

    def display_final(self, filename):
        self.filename = filename
        self.ids.curvideo.source=filename
        self.ids.curvideo.state='play'
        self.ids.curvideo.reload()

        self.ids.video_name.text=filename[7:]

    def open_file(self):
        os.startfile(os.path.abspath(self.filename))

    def upload_yt(self):
        from uploader import uploadYoutube

        tags = "trending,reels,shorts,clips,shortstory,highlights,rich,interview,tiktok,story,animals,gta,theo von,viral,this week,fortnite clips,fortnite sniper,fortnite 1v1,fortnite,motivational video,clix stream,stream highlights,self improvement tips,self improvement,heavy sniper,self improvement habits,motivation,Man Saves His Dog,Man Saves His Cat,Animal Rescue,animal songs,rescue animals,dodo,perro,the dodo,rescuers,funny animals,stuck,trapped,puppies,for kids"
        desc = self.filename[7:-4] +" and other insane interesting stories, subscribe for more content. #funny #shorts #reels #tiktok #stories #comedy #cat #dog #animalstory #animalshorts #animalrescue #rescue" 
        load_dotenv()
        print(os.environ.get('EMAIL'))
        if not all(item in os.environ for item in ['EMAIL','PASSWORD','LINK']):
            self.ids.video_name.text = "YOUTUBE LOGIN NOT SET UP CORRECTLY"
            return
        upload = threading.Thread(target=uploadYoutube, 
                              args=(self.filename,os.environ.get('EMAIL'),os.environ.get('PASSWORD'),os.environ.get('LINK'),self.filename[7:-4],tags,desc))
        upload.start()
        

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("forge.kv")
sm = WindowManager()


screens = [InputWindow(name="main"), GenWindow(name="gen"), VideoWindow(name="video"), FinalWindow(name="final")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"

class P(FloatLayout):
    pass

def show_popup():
    show = P()
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(400,400))
    popupWindow.open()

class Forge(App):
    def build(self):
        return sm
    
if __name__ == "__main__":
    Forge().run()


#kivy_venv\Scripts\activate