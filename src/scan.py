from util import scan_as_rect
from util import find_horizontal_vertical_lengthes
import numpy as np
import argparse
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to image")
args = vars(ap.parse_args())

# read image
image = cv2.imread(args["image"])
warped = scan_as_rect(image)

# show
cv2.imshow("scanned", imutils.resize(warped, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()


# find vertical, horizontal length
hor_length, vertical_length, matric_per_pixel = find_horizontal_vertical_lengthes(warped)

# output
print("%f" % (vertical_length*matric_per_pixel))
for h in hor_length:
    print("%f %f %f" % (h[0]*matric_per_pixel, h[1]*matric_per_pixel, h[2]*matric_per_pixel))
