import picamera
import picamera.array
import numpy as np

# picture size
x = 1920
y = 1080
# sample window
# x1 = 1672
# x2 = 1674
# y1 = 518
# y2 = 521
x1 = 464
x2 = 636
y1 = 912
y2 = 972
step = 0.01
threshold = 1
# place white sheet of paper infront of the camera and run the code
with picamera.PiCamera() as camera:
    camera.resolution = (x, y)
    camera.awb_mode = 'off'
    # Start off with ridiculously low gains
    rg, bg = (0.1, 0.1)
    # camera.awb_gains = (rg, bg)
    with picamera.array.PiRGBArray(camera, size=(x, y)) as output:
        # Allow 30 attempts to fix AWB
        for i in range(300):
            # Capture a tiny resized image in RGB format, and extract the
            # average R, G, and B values
            # camera.capture(output, format='rgb', resize=(x, y), use_video_port=True)
            camera.awb_gains = (rg, bg)
            camera.capture(output, format='rgb', use_video_port=True) 
            # print(output.array[y1:y2,x1:x2,0])
            # print(output.array[y1:y2,x1:x2,1])
            # print(output.array[y1:y2,x1:x2,2])
             
            # r, g, b = (np.mean(output.array[..., i]) for i in range(3))
            r, g, b = (np.mean(output.array[y1:y2, x1:x2, i]) for i in range(3))
            print('R:%5.2f, B:%5.2f = (%5.2f, %5.2f, %5.2f)' % (
                rg, bg, r, g, b))
            # Adjust R and B relative to G, but only if they're significantly
            # different (delta +/- 2)
            if abs(r - g) > threshold:
                if r > g:
                    rg -= step
                    # rg += step
                    #pass
                else:
                    rg += step
                    # rg -= step
                    #pass
            if abs(b - g) > threshold:
                if b > g:
                    bg -= step
                    # bg += step
                    pass
                else:
                    bg += step
                    # bg -= step
                    pass
            # camera.awb_gains = (rg, bg)
            output.seek(0)
            output.truncate()
