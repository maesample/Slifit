import numpy as np

def sizeExtracter(fileName):
    objFile = open(fileName, 'r')
    verticalSize = 0
    horizontalSizeList = []

    for line in objFile:
        split = line.split()

        if not len(split):
            continue
        if len(split) == 1:
            verticalSize = split[0]
        else:
            horizontalSizeList.append(map(float, split[:]))

    objFile.close()

    return float(verticalSize), horizontalSizeList

if __name__ == "__main__":
    verticalSize, horizontalSizeList = sizeExtracter("./out_size.txt")

    print(verticalSize)
    print(horizontalSizeList)