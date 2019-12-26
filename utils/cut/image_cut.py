from moviepy.editor import VideoFileClip
from utils.clrs import color

def cut(path, start, end, step):
    clip = VideoFileClip(path)
    for x in range(start, end, step):
        # need to do os.mkdir
        fname = "../temp/"+str(x)+".jpeg"
        color.green(fname)
        clip.save_frame(fname, t=x)
    color.yellow("it is done !")
