from moviepy.editor import VideoFileClip
import shutil, os, sys
import time
from utils.clrs import welcome
from nudenet import NudeClassifier
import multiprocessing
from utils.cut import image_cut
from utils.clrs import color


def clsfy(location, classifier, how_safe):
    #this method is to classify the frames
    data = classifier.classify(location)
    #change this variable as per the accuracy of the mode

    if data[location]['safe'] < how_safe:
        color.red("frame: "+ str(location) + " safe: "+str(data[location]['safe']))
        #shutil.move(location, '../tmp')
        return True
    else:
        color.green("frame: "+str(location)+" safe : "+str(data[location]['safe']))
        return False

def lop(lis, classifier, location):
    info_lis= []
    for x in lis:
        loc = location + str(x)
        if clsfy(loc, classifier, 0.2):
            info_lis.append(loc)
    return info_lis
def cals(frame, classifier, vclip):
    vclip.save_frame("../accu/"+str(frame)+"-0.jpeg", t=frame)
    vclip.save_frame("../accu/"+str(frame)+"-1.jpeg", t=frame+0.1)
    vclip.save_frame("../accu/"+str(frame)+"-2.jpeg", t=frame+0.2)
    vclip.save_frame("../accu/"+str(frame)+"-3.jpeg", t=frame+0.5)
    vclip.save_frame("../accu/"+str(frame)+"-4.jpeg", t=frame+0.7)
    vclip.save_frame("../accu/"+str(frame)+"-5.jpeg", t=frame+0.9)

    caliberate = 0
    for x in range(6):
        loc = "../accu/"+str(frame)+"-"+str(x)+".jpeg"
        if clsfy(loc, classifier, 0.1):
            caliberate += 1

    if (caliberate/6) > 0.5:
        return True
    else:
        return False

def run_meth(fname):
    started_at = time.time()

    color.red("The main started at "+str(time.ctime()))
      #later on clip_loc = var
    clip_loc = fname

    vclip = VideoFileClip(clip_loc)
    color.red("The duration of the clip : " + str(vclip.duration))
    debug_console= "FPS :" + str(vclip.fps)
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
      #later code is to classify the elements

    color.red("The time elapsed : "+str(stopped_at - started_at))
    started_at = time.time()
    color.yellow("\n\n--->The classification started  : "+str(started_at))
    classifier = NudeClassifier("../classifier_model")
    img_lis = os.listdir('../temp/')
    info_lis = []
    info_lis = lop(img_lis, classifier, '../temp/')

    stopped_at = time.time()
    color.yellow("\n\n---> classification took : "+str(stopped_at-started_at))
    debug_console = "---> classification took : "+str(stopped_at-started_at)
      #info_lis has all the potential nsfw frames
    print(info_lis)
    frame_values = []
    for img_loc in info_lis:
         #frame_sec is to get the second on which the frame was retrieved
         #handle exceptions here
         x = image_cut.frame_sec(img_loc)
         if x == None:
             pass
         else:
             frame_values.append(x)
    try:
        os.mkdir("../accu/")
    except:
        pass

    try:
        os.mkdir("../final/")
    except:
        pass

    updated_info_lis= []
    for frame in frame_values:
        if cals(frame, classifier, vclip):
            updated_info_lis.append(frame)

    for frm in updated_info_lis:
        vclip.save_frame("../final/"+str(frm)+".jpeg", t=frm)

    print("It is done")
    #os.system("firefox -new-tab 'http://127.0.0.1:5000/'")
    return updated_info_lis

if __name__ == "__main__":
    welcome.welc()
    # change the folder path when you build the front end
    p_NSFW = []
    p_NSFW= run_meth("/root/tvf/got.mp4")
    color.purple("The Following seconds in the video have NSFW content: ")
    for nsfw in p_NSFW:
        print("-->", nsfw)
