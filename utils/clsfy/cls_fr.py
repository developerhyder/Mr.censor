from nudenet import NudeClassifier
from utils.clrs import color


def clsfy(location, classifier):
    # this method is to classify the frames
    data = classifier.classify(location)
    color.green("frame: "+str(location)+" safe : "+str(data[location]['safe']))

    #change this variable as per the accuracy of the mode
    how_safe = 0.4

    if data[location]['safe'] < how_safe:
        return False
    else:
        return True
