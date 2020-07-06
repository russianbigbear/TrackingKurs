import cv2
import sys
from ObjectTrackingFile import *


if __name__ == "__main__":

    #Паттерн стратегия
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    type_num = input("Choose tracking method:\n"
                     "0)'BOOSTING'\n"
                     "1)'MIL'\n"
                     "2)'KCF'\n"
                     "3)'TLD'\n"
                     "4)'MEDIANFLOW'\n"
                     "5)'GOTURN'\n"
                     "6)'MOSSE'\n"
                     "7)'CSRT'\n"
                     "Your choose: ")
    tracker_type = tracker_types[int(type_num)]

    if False:
        video = cv2.VideoCapture("videos/run.mp4")

        # Видео не открылось
        if not video.isOpened():
            print("Could not open video")
            sys.exit()

        # Чтение первого кадра
        ok, frame = video.read()
        if not ok:
            print("Cannot read video file")
            sys.exit()

        # Выбр другой ограничительной рамки
        bounding_box = cv2.selectROI(frame, False)

        my_obj_tracker = ObjectTracking(video, tracker_type)
        my_obj_tracker.TrackObjectV(frame, bounding_box)
    else:
        my_obj_tracker = ObjectTracking(None, tracker_type)
        my_obj_tracker.TrackObject()

    exit(0)

