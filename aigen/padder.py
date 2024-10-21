from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from skimage.filters import gaussian

from moviepy.config import change_settings
change_settings({"FFMPEG_BINARY":"ffmpeg"})

def blur(image):
    """ Returns a blurred (radius=4 pixels) version of the image """    
    return gaussian(image.astype(float), sigma=4)

def CombinePad(name,blurname,output):
    main = VideoFileClip(name)

    topOg = VideoFileClip(blurname)
    top = topOg.without_audio()
    bottomOg = VideoFileClip(blurname)
    bottom = bottomOg.without_audio()
        
    #Fix resolutions
    # size returns WIDTH,HEIGHT
    width,height = top.size 

    print(top.size,bottom.size)

    totalHeight = float(width) / 9 * 16
    clipHeight = (totalHeight - height) / 2

    top = top.crop(x1=0 ,y1=0,x2=width,y2=clipHeight)
    bottom = bottom.crop(x1=0 ,y1=height-clipHeight,x2=width,y2=height)
    #.resize((x,y))
    final_clip = clips_array([[top], [main], [bottom]]).subclip(0,main.duration - .3)

    final_clip.write_videofile(output, codec='libx264')

    print(final_clip.size)

    top.close()
    bottom.close()
    main.close()
    bottomOg.close()
    topOg.close()