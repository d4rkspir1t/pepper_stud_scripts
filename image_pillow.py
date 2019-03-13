#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Get an image. Display it and save it using PIL."""

import qi
import argparse
import sys
import time
import Image
import numpy as np
import cv2


def main(session):
    """
    First get an image, then show it on the screen with PIL.
    """
    # Get the service ALVideoDevice.

    # video_service = session.service("ALVideoDevice")
    # resolution = 2    # VGA
    # colorSpace = 11   # RGB
    #
    # videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)
    #
    # t0 = time.time()
    #
    # # Get a camera image.
    # # image[6] contains the image data passed as an array of ASCII chars.
    # naoImage = video_service.getImageRemote(videoClient)
    #
    # t1 = time.time()
    #
    # # Time the image transfer.
    # print "acquisition delay ", t1 - t0
    #
    # video_service.unsubscribe(videoClient)
    #
    #
    # # Now we work with the image returned and save it as a PNG  using ImageDraw
    # # package.
    #
    # # Get the image size and pixel array.
    # imageWidth = naoImage[0]
    # imageHeight = naoImage[1]
    # array = naoImage[6]
    # image_string = str(bytearray(array))
    #
    # # Create a PIL Image from our pixel array.
    # im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
    #
    # # Save the image.
    # im.save("camImage.png", "PNG")
    #
    # im.show()
    vid_service = session.service('ALVideoDevice')
    # subscribe top camera
    AL_kTopCamera = 1
    AL_kQVGA = 1  # 320x240
    AL_kBGRColorSpace = 13
    captureDevice = vid_service.subscribeCamera(
        "test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)

    # create image
    width = 320
    height = 240
    image = np.zeros((height, width, 3), np.uint8)

    while True:

        # get image
        result = vid_service.getImageRemote(captureDevice)

        if result == None:
            print 'cannot capture.'
        elif result[6] == None:
            print 'no image data string.'
        else:
            # print result
            # translate value to mat
            values = map(ord, str(bytearray(result[6])))
            # print(values)
            i = 0
            for y in range(0, height):
                for x in range(0, width):
                    #image.itemset((y, x, 0), values[i+0])
                    image.itemset((y, x, 0), values[i + 0])
                    image.itemset((y, x, 1), values[i + 1])
                    image.itemset((y, x, 2), values[i + 2])
                    i += 3

            # show image
            cv2.imshow("pepper-top-camera-320x240", image)

        # exit by [ESC]
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.2",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)