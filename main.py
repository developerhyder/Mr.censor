from moviepy.editor import VideoFileClip
import os
import time
from nudenet import NudeClassifier
import multiprocessing


def cut(path, start, end, step):
    clip = VideoFileClip(path)
    for x in range(start, end, step):
        # need to do os.mkdir
        fname = "../temp/"+str(x)+".jpeg"
        print(fname)
        clip.save_frame(fname, t=x)
    print("it is done")

def clsfy(location, classifier):
    # this method is to classify the frames
    data = classifier.classify(location)
    print("frame: ",location,"safe :",data[location]['safe'])

    #change this variable as per the accuracy of the mode
    how_safe = 0.4

    if data[location]['safe'] < how_safe:
        return False
    else:
        return True

def lop(lis, classifier, location, info_lis):
    for x in lis:
        if clsfy(loc, classifier):
            info_lis.append(loc)

if __name__ == "__main__":

    # and the main begins
    print("The main started at", time.ctime())

    clip_loc = "/root/tvf/got.mp4"

    vclip = VideoFileClip(clip_loc)
    print("The duration of the clip : ", vclip.duration)
    print("FPS :", vclip.fps)

    duration = int(vclip.duration)

    try:
        os.mkdir("../temp/")
    except:
        pass

    print("Main process : ",os.getpid())

    start = 0
    end = int(duration/2)
    step = 5
    p1 = multiprocessing.Process(target=cut, args=(clip_loc, start, end, step, ))
    start = int(duration/2)
    end = duration
    p2 = multiprocessing.Process(target=cut, args=(clip_loc, start, end, step))

    p1.start()
    p2.start()

    print("p1 :",p1.pid,"p2 :",p2.pid)

    p1.join()
    p2.join()

    # later code is to classify the elements
>>>>>>> idris
