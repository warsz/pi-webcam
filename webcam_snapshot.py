import os
from datetime import datetime as dt
from fractions import Fraction
from time import sleep

import numpy as np

import picamera
import picamera.array




# setup local
date = dt.now()
kwargs = {
    'path': '/home/pi/Pictures/webcam/',
    'path_transfer': '/home/pi/Devel/webcam/',
    'pic_name': 'olnesseter.png',
    'test_pic': 'test.png',
    'date': date,
    'filename': 'perlebu_{}_{:02d}-{:02d}-{:02d}.png'.format(
        date.date(), date.hour, date.minute, date.second
    ),
    'resolution': (1920, 1080),
    'iso': 60,
    'framerate': (1, 1),
    'sensor_mode': 1,
    'shutter_speed': 1,
    'cam_warm_up': 2,
    # pixel region pointing to a whiteelement in the picture
    # which is used for white balance calibration. Indicate your own!
    'calib_x_range': (1906, 1910),
    'calib_y_range': (522, 524),
    # 'calib_x_range': (1883, 1885), # test
    # 'calib_y_range': (542, 547), # test
}


def take_snapshot(**kwargs):
    with picamera.PiCamera() as camera:
        camera.resolution = kwargs['resolution']
        camera.iso = kwargs['iso']
        if kwargs['iso']==800:
            camera.sensor_mode = kwargs['sensor_mode']
            camera.framerate = kwargs['framerate']
            camera.shutter_speed = kwargs['shutter_speed']
            g = (7.80, 7.60) # (1.20, 1.30)
        else:
            g = (1.00, 1.20) # (1.20, 1.20) # keep for now
            # g = calib_white(camera, **kwargs) # use for measurement and calibration
        camera.awb_gains = g
        camera.start_preview()
        camera.led = False
        # camera warm-up time
        sleep(kwargs['cam_warm_up'])
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        camera.awb_mode = 'off'
        camera.capture(kwargs['test_pic'])


def calib_white(camera, **kwargs):
    camera.awb_mode = 'off'
    # begin with far off values
    rg, bg = (0.5, 0.5)
    camera.awb_gains = (rg, bg)
    with picamera.array.PiRGBArray(camera) as output:
        for j in range(30):
            camera.capture(output, format='rgb', use_video_port=True)
            r, g, b = (
                np.mean(
                    output.array[
                        kwargs['calib_x_range'][0] : kwargs['calib_x_range'][1],
                        kwargs['calib_y_range'][0] : kwargs['calib_y_range'][1],
                        i,
                    ]
                )
                for i in range(3)
            )
            # need to stop reading from video_port or get overflow
            output.seek(0)
            output.truncate()
            if abs(r - g) > 2:
                if r > g:
                    rg -= 0.1
                else:
                    rg += 0.1
            if abs(b - g) > 2:
                if b > g:
                    bg -= 0.1
                else:
                    bg += 0.1
            camera.awb_gains = (rg, bg)
    return (rg, bg)


def main():
    # snapshot day
    kwargs['test_pic'] = 'day.png'
    take_snapshot(**kwargs)

    # snapshot night light
    # Force sensor mode 3 (the long exposure mode), set
    # the framerate to 1/6fps, the shutter speed to 6s,
    # and ISO to 800 (for maximum gain)
    kwargs['test_pic'] = 'dark_light.png'
    kwargs['iso'] = 800
    kwargs['sensor_mode'] = 3
    kwargs['framerate'] = Fraction(1, 2)
    kwargs['shutter_speed'] = 2000000
    kwargs['cam_warm_up'] = 30
    take_snapshot(**kwargs)
    
    # snapshot night no light
    # Force sensor mode 3 (the long exposure mode), set
    # the framerate to 1/6fps, the shutter speed to 6s,
    # and ISO to 800 (for maximum gain)
    kwargs['test_pic'] = 'dark_no_light.png'
    kwargs['framerate'] = Fraction(1, 6)
    kwargs['shutter_speed'] = 6000000
    take_snapshot(**kwargs)
    
    # measure size which indicates quality
    day_size = os.stat('day.png').st_size
    night_light_size = os.stat('dark_light.png').st_size
    night_no_light_size = os.stat('dark_no_light.png').st_size
    
    # select the bigest file which will have most detail
    best_pic = 'day.png'
    best_size = day_size
    if best_size < night_light_size:
        best_size = night_light_size
        best_pic = 'dark_light.png'
    if best_size < night_no_light_size:
        best_size = night_no_light_size
        best_pic = 'dark_no_light.png'
    cmd = "cp {} {}".format(best_pic, kwargs['path']+kwargs['filename'])
    print(cmd)
    os.system(cmd)

    # timestamp picture
    # once moved to right angle remove the crop option
    cmd = "convert {} -crop 1200x1080+720+0 -fill white -pointsize 20 -geometry +100+100 -background Black label:\'{}\' -append {}".format(
        kwargs['path'] + kwargs['filename'],
        'Olnessaeter ' + str(kwargs['date']),
        kwargs['path_transfer'] + kwargs['pic_name']
    )
    os.system(cmd)
    cmd = "convert {} {}".format(
        kwargs['path_transfer'] + "olnesseter.png",
        kwargs['path_transfer'] + "olnesseter.jpg"
    )
    os.system(cmd)

if __name__ == "__main__":
    main()

