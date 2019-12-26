from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import multiprocessing
import time
from nudenet import NudeClassifier

# use relative paths it makes life easier
# this converts the video into frames

def cut(path,part):
    clip = VideoFileClip(path)
    durn= int(clip.duration)
    for x in range(0, durn, 5):
        fname = "/root/Documents/trained/sclips/vid/" + part + "/" + str(x)+".jpeg"
        print("Current dir: /",part,"current-frame: ",part,str(x),".jpeg")
        clip.save_frame(fname, t=x)
    print("its done !")

def clsfy(location, classifier):
    data = classifier.classify(location)
    print(data[location]['safe'])

    if data[location]['safe'] < 0.6:
        return False
    else:
        return True

def lop(lis, classifier, location, info_lis):
    for x in lis:
        loc = location + str(x)
        if clsfy(loc, classifier):
            info_lis.append(loc)

if __name__ == "__main__":

    #change here for input path

    print("main has started : ", time.ctime())
    clip_loc = "/root/tvf/got.mp4"

    vclip = VideoFileClip(clip_loc)
    print("duration of the video : " , vclip.duration)
    print("FPS : ",vclip.fps)
    duration = int(vclip.duration)
    try:
        os.mkdir("/root/Documents/trained/sclips/temp_vid/")
    except:
        pass


    try:
        os.mkdir("/root/Documents/trained/sclips/vid/part-1/")
    except:
        pass

    try:
        os.mkdir("/root/Documents/trained/sclips/vid/part-2/")
    #to reduce ambiguity we will put frames in different folders
    except:
        pass

    dur = int(duration/2)

    start_time= 0
    end_time = dur

    ffmpeg_extract_subclip(clip_loc, start_time, end_time, targetname="/root/Documents/trained/sclips/temp_vid/part1.mp4")
    print("part-1 generated")

    start_time= dur + 1
    end_time = duration
    ffmpeg_extract_subclip(clip_loc, start_time, end_time, targetname="/root/Documents/trained/sclips/temp_vid/part2.mp4")


    print("part-2 generated")

    print("starting Multi-processing current pid : ", os.getpid())

    p1 = multiprocessing.Process(target=cut, args=("/root/Documents/trained/sclips/temp_vid/part1.mp4","part-1", ))
    p2 = multiprocessing.Process(target=cut, args=("/root/Documents/trained/sclips/temp_vid/part2.mp4","part-2", ))

    print("processes have begun : ", time.ctime())

    p1.start()
    p2.start()


    print("The parallel processes p1:",p1.pid," p2: ", p2.pid)

    p1.join()
    p2.join()
    print("processes have stopped :",time.ctime())

    classifier = NudeClassifier('../classifier_model')
    # clsfy("../deli.jpeg", classifier)
    #clsfy("../profile.jpeg", )

    dir_list1 = os.listdir("./vid/part-1/")
    dir_list2 = os.listdir("./vid/part-2/")

    info_lis1 = []
    info_lis2 = []

    # process1 = multiprocessing.Process(target=lop, args=(dir_list1, classifier, "./vid/part-1/", info_lis1, ))
    # process2 = multiprocessing.Process(target=lop, args=(dir_list2, classifier, "./vid/part-2/", info_lis2, ))
    #
    # process1.start()
    # process2.start()
    #
    # process1.join()
    # process2.join()

    lop(dir_list1, classifier, "./vid/part-1/", info_lis1)
    lop(dir_list1, classifier, "./vid/part-2/", info_lis2)

    print("info_lis1:", info_lis1)
    print("info_lis2:", info_lis2)
