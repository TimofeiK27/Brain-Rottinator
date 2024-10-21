import pysrt, random
from moviepy.editor import *
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def add_subtitles(video_path, subtitle_path, output_path, TopBottom):
    # Load video
    video = VideoFileClip(video_path)
    
    # Load subtitles
    subs = pysrt.open(subtitle_path)
    
    # Create a list to hold all the subtitle clips
    subtitle_clips = []

    for sub in subs:
        # Create a TextClip for each subtitle
        # 65 for 512x512, 115 for 1080x1080, 200 for 1520x1520
        txt_clip = TextClip(sub.text, fontsize=115, color='white', font='Impact', stroke_color='black', stroke_width=3, bg_color='none')

        #45 px is at top, -120 for 540 and 1080, 280 for 1520
        if TopBottom=='top':
            txt_clip = txt_clip.set_position(('center', video.size[1] - 180)).set_duration(sub.duration.seconds + sub.duration.milliseconds / 1000)
        else:
            txt_clip = txt_clip.set_position(('center', 80)).set_duration(sub.duration.seconds + sub.duration.milliseconds / 1000)
        txt_clip = txt_clip.set_start(sub.start.seconds + sub.start.milliseconds / 1000 - 0.25)

        # Add to subtitle clips list
        subtitle_clips.append(txt_clip)

    # Create a CompositeVideoClip
    video = CompositeVideoClip([video] + subtitle_clips)

    # Write the result to a file
    video.write_videofile(output_path, codec='libx264', fps=video.fps)
