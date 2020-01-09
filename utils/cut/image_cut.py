from moviepy.editor import VideoFileClip
from utils.clrs import color
import re

def cut(path, start, end, step):
    clip = VideoFileClip(path)
    for x in range(start, end, step):
        # need to do os.mkdir
        fname = "../temp/"+str(x)+".jpeg"
        color.green(fname)
        clip.save_frame(fname, t=x)
    color.yellow("it is done !")

def frame_sec(str_val):
    x = re.findall("\d+",str_val)
    if not x:
        return None
    else:
        return int(x[0])
