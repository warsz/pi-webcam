import csv
from datetime import datetime
import picamera
import picamera.array
import numpy as np
from time import sleep


def append_to_log(filename, row):
    with open(filename, 'a') as csvfile:
        fieldnames = ['date', 'time', 'light_meter_value', 'settings']
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )
        writer.writerow(row)


def light_meter():
    row = get_time()
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            print("Initializing Pi Camera")
            sleep(2)
            camera.exposure_mode = 'off'
            camera.capture(stream, format='rgb')
            # pixAverage = int(np.average(stream.array[...,1]))
            pixAverage = np.average(stream.array[...,1])
            row['light_meter_value'] = pixAverage
            row['settings'] = None
    return row


def get_time():
    dt = datetime.now()
    return {
        'date': dt.date(),
        'time': '{:02d}:{:02d}'.format(dt.hour, dt.minute)
    }

def white_balance_cal():
    # need to sample pixels [1906,522] to [1910,524]
    return rg, bg

def main():
    row = light_meter()
    append_to_log(
        '/home/pi/Devel/webcam/light_meter_log.csv',
        row
    )


if __name__ == "__main__": main()
