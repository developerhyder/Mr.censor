from moviepy.editor import VideoFileClip
import os
import time
from utils.clrs import welcome
from nudenet import NudeClassifier
import multiprocessing
from utils.cut import image_cut
from utils.clsfy import cls_fr
from utils.clrs import color


def lop(lis, classifier, location, info_lis):
    for x in lis:
        if cls_fr.clsfy(loc, classifier):
            info_lis.append(loc)

if __name__ == "__main__":

    welcome.welc()
    # and the main begins
    started_at = time.time()
    color.red("The main started at "+str(time.ctime()))

    var = input(color.green_str("Enter the path (for now type something): "))

    #later on clip_loc = var
    clip_loc = "/root/tvf/got.mp4"

    vclip = VideoFileClip(clip_loc)
    color.red("The duration of the clip : " + str(vclip.duration))
    color.red("FPS :" + str(vclip.fps))

    duration = int(vclip.duration)

    try:
        os.mkdir("../temp/")
    except:
        pass

    print("Main process : ",os.getpid())

    start = 0
    end = int(duration/4)
    step = 5
    p1 = multiprocessing.Process(target=image_cut.cut, args=(clip_loc, start, end, step, ))
    start = int(duration/4)
    end = int(duration/2)
    p2 = multiprocessing.Process(target=image_cut.cut, args=(clip_loc, start, end, step))

    start = int(duration/2)
    end = int(duration/1.33)
    p3 = multiprocessing.Process(target=image_cut.cut, args=(clip_loc, start, end, step))

    start = int(duration/1.33)
    end = duration
    p4 = multiprocessing.Process(target=image_cut.cut, args=(clip_loc, start, end, step))

    p1.start()
    p2.start()
    p3.start()
    p4.start()


    color.green("p1 : "+str(p1.pid)+"p2 :"+str(p2.pid))

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    stopped_at = time.time()

    color.red("The time elapsed : "+str(stopped_at - started_at))

#need to write

    # later code is to classify the elements
