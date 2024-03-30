from datetime import datetime as dt
from time import sleep
import picamera
import os

# setup local
path = '/home/pi/Pictures/webcam/'
path_transfer = '/home/pi/Devel/webcam/'
pic_name = 'olnesseter.png'
date = dt.now()
filename = 'perlebu_{}_{:02d}-{:02d}-{:02d}.png'.format(
    date.date(),
    date.hour,
    date.minute,
    date.second
)

# snapshot
with picamera.PiCamera() as camera:
   # camera.resolution = (600, 400)
   camera.resolution = (1920, 1080)
   camera.iso = 60
   camera.start_preview()
   camera.led = False
   # camera warm-up time
   sleep(2)
   camera.capture(path+filename)

# timestamp picture
# once moved to right angle remove the crop option
cmd = "convert {} -crop 1200x1080+720+0 -fill white -pointsize 20 -geometry +100+100 -background Black label:\'{}\' -append {}".format(
    path+filename,
    'Olnessaeter '+str(date),
    path_transfer+pic_name
)
os.system(cmd)
cmd = "convert {} {}".format(
    path_transfer+"olnesseter.png",
    path_transfer+"olnesseter.jpg"
)
os.system(cmd)

