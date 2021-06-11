import time
from datetime import datetime
import cv2
from werkzeug.debug import Console

while True:
    temp = datetime.now()
    timee = "{:04d}{:02d}{:02d} {:02d}:{:02d}:{:02d}".format(temp.year, temp.month, temp.day,temp.hour,temp.minute,temp.second)
    print(timee,end="\r",flush=False)


