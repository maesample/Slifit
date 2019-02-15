import numpy as np
import math
import argparse
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

PROCESSING_SIZE = 512.0
ratio = image.shape[0] / PROCESSING_SIZE
orig = image.copy()
image = imutils.resize(image, height=int(PROCESSING_SIZE))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray[gray < 190] = 70
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)


# calculate matric/pixel
# image = cv2.drawContours(image, cnts[0], -1, (0, 255, 0), 3)
peri = cv2.arcLength(cnts[0], True)
approx = cv2.approxPolyDP(cnts[0], 0.02*peri, True)
lb = approx[0][0]
lt = approx[1][0]
rb = approx[2][0]
rt = approx[3][0]
if lb[1] < lt[1]:
    lb, lt = lt, lb
if rb[1] < rt[1]:
    rb, rt = rb, rt
if lb[0] > rb[0]:
    lb, rb = rb, lb
if lt[0] > rt[0]:
    lt, rt = rt, lt
delta = [lb[0] - rb[0], lb[1] - rb[1]]
width = math.sqrt(delta[0]*delta[0] + delta[1]*delta[1])
delta = [lb[0] - lt[0], lb[1] - lt[1]]
height = math.sqrt(delta[0]*delta[0] + delta[1]*delta[1])
matric_per_pixel = 3.0/((width+height)/2.0)




# find horizontal lines passing foot
foot = cnts[len(cnts)-1]
foot = list(map(lambda x: (x[0][0], x[0][1]), foot))
foot = sorted(foot, key=lambda x: x[1], reverse=False)
print(foot)

hor_lines = []
top_y = foot[0][1]
now_y = foot[0][1]
left = right = foot[0]
i = 0
MIN_RECOG = 10
while i < len(foot):
    if foot[i][1] != now_y:
        if (right[0]-left[0]) > MIN_RECOG:
            hor_lines.append(((left, right), left[1]-top_y))
        now_y = foot[i][1]
        left = right = foot[i]
    elif foot[i][0] < left[0]:
        left = foot[i]
    elif foot[i][0] > right[0]:
        right = foot[i]
    i += 1

for line in hor_lines:
    image = cv2.line(image, line[0][0], line[0][1], (0, 255, 0), 1)



# def measuring_distances(cnt):
#     cnt = list(map(lambda x: (x[0][0], x[0][1]), foot))
#     cnt = sorted(cnt, key=lambda x: x[1], reverse=False)
#     distances = []
#     top_y = cnt[0][1]
#     now_y = cnt[0][1]
#     left = cnt[0]
#     i=0
#     while i < len(cnt):
#         if cnt[i][1] != now_y:
#             distances.append((left[0], left[1]-top_y))
#             now_y = cnt[i][1]
#             left = cnt[i]
#         elif cnt[i][0] < left[0]:
#             left = cnt[i]
#         i += 1
#
#     ACCEPT_INCREASING = 10
#     result = [distances[0]]
#     i = 1
#     while i < len(distances):
#         if (distances[i][0] - distances[i-1][0]) < ACCEPT_INCREASING:
#             result.append(distances[i])
#             i += 1
#         else:
#             while i < len(distances) and distances[i-1][0] - distances[i][0] < ACCEPT_INCREASING:
#                 i += 1
#
#     return (result, top_y)
#
# d = measuring_distances(foot)
# print(d)
# d = list(map(lambda x: (x[0]*matric_per_pixel, x[1]*matric_per_pixel), d))
# print(d)


# image = cv2.drawContours(image, cnts[len(cnts)-1], -1, (0, 255, 0), 3)
cv2.imshow("im", image)
cv2.waitKey(0)
# cv2.destroyAllWindows()
