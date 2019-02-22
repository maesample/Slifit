from util import scan_as_rect
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
cv2.imshow("original", imutils.resize(image, height=650))
# cv2.imshow("scanned", imutils.resize(warped, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()

