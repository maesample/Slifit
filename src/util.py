# https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

import numpy as np
import cv2
import imutils
import math
from skimage.filters import threshold_local

def order_points(pts) :
    rect = np.zeros((4,2), dtype="float32")

    # top-left will have smallest sum
    # bottom-right will have largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # top-right will have smallest diff
    # bottom-left will have largest diff
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect
def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    width0 = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width1 = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width0), int(width1))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    height0 = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height1 = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height0), int(height1))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (max_width, max_height))

    # return the warped image
    return warped

def scan_as_rect(image) :
    # calculate ratio
    ratio = image.shape[0] / 512.0
    orig = image.copy()
    image = imutils.resize(image, height=512)

    # convert to grayscale, find edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # gray[gray < 170] = 30
    edged = cv2.Canny(gray, 75, 200)

    # find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    screen_cnt = None
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)

        # check contour has four points
        if len(approx) == 4:
            screen_cnt = approx
            break

    return four_point_transform(orig, screen_cnt.reshape(4, 2) * ratio)

def find_horizontal_vertical_lengthes(image) :
    PROCESSING_SIZE = 512.0
    matric_per_pixel = 297.0/PROCESSING_SIZE
    image = imutils.resize(image, height=int(PROCESSING_SIZE))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    T = threshold_local(gray, 11, offset=10, method="gaussian")
    gray = (gray > T).astype("uint8") * 255
    edged = cv2.Canny(gray, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    foot = cnts[0]
    foot = list(map(lambda x: (x[0][0], x[0][1]), foot))
    foot = sorted(foot, key=lambda x: x[1], reverse=False)

    height_px = foot[len(foot)-1][1] - foot[0][1]

    top_y = foot[0][1]
    now_y = foot[0][1]
    left = right = foot[0]
    lleft = lright = foot[0]
    MIN_RECOG=10
    hor_lines = [[foot[0], foot[0]]]
    i = 1
    while i < len(foot):
        if foot[i][1] != now_y:
            if math.fabs(left[0]-right[0]) > MIN_RECOG:
                hor_lines.append([left, right])
            now_y = foot[i][1]
            left = right = foot[i]
        elif foot[i][0] < left[0]:
            left = foot[i]
        elif foot[i][0] > right[0]:
            right = foot[i]
        i += 1

    result = []
    for j in range(len(hor_lines)-1):
        result.append((hor_lines[j][0][0], hor_lines[j][1][0], hor_lines[j][0][1]-top_y))
        start_y = hor_lines[j][0][1]-top_y
        length = hor_lines[j+1][0][1] - hor_lines[j][0][1]
        delta = ((hor_lines[j+1][0][0] - hor_lines[j][0][0])/length,
                 (hor_lines[j+1][1][0] - hor_lines[j][1][0])/length)
        for k in range(1, length):
            l = int(hor_lines[j][0][0] + delta[0]*k)
            r = int(hor_lines[j][1][0] + delta[1]*k)
            result.append((l, r, start_y+k))

    for line in result:
        image = cv2.line(image, (line[0], line[2]), (line[1], line[2]), (0, 255, 0), 1)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (result, height_px, matric_per_pixel)

