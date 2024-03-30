from datetime import datetime as dt
from time import sleep
import picamera
import os

# setup local
path = '/home/pi/Pictures/webcam/'
path_transfer = '/home/pi/Devel/webcam/'
pic_name = 'olnesseter.png'
ISO = [100, 200, 320, 400, 500, 640, 800]
s_speeds = [
    100, 200, 300, 400,
    500, 1000, 1500, 2000,
    2500, 3000, 3500, 4000,
    4500, 5000, 5500, 6000,
    6500, 7000, 7500, 8000,
    8500, 9000, 9500, 10000
]


def get_filename(
    date, hour, minute,
    iso, s_speed
):
    filename = 'camtest_{}_{:02d}-{:02d}_{}_{:05d}.png'.format(
        date, hour, minute, iso, s_speed
    )
    return filename


def snapshot(
    path, filename,
    iso, s_speed
):
    with picamera.PiCamera() as camera:
        # camera.resolution = (600, 400)
        camera.resolution = (1920, 1080)
        camera.sensor_mode = 3
        camera.shutter_speed = s_speed
        camera.iso = iso
        camera.led = False
        # camera warm-up time
        camera.start_preview()
        sleep(2)
        camera.exposure_mode = 'off'
        camera.capture(path+filename)


t = dt.now()
for iso in ISO:
    for speed in s_speeds:
	filename = get_filename(
            t.date(), t.hour, t.minute, iso, speed
        )
        print(filename)
        snapshot(
            path, filename, iso, speed
        )


# timestamp picture
# once moved to right angle remove the crop option
# cmd = "convert {} -crop 1200x1080+720+0 -fill red -pointsize 16 -geometry +100+100 -background Black label:\'{}\' -append {}".format(
#     path+filename,
#     str(date),
#     path_transfer+pic_name
# )
# os.system(cmd)

