import numpy as np

def objVertexExtract(name):
    objFile = open(name, 'r')
    vertexList = []
    didReadVertex = False
    vertexBeforeTxt = ''
    vertexAfterTxt = ''

    for line in objFile:
        split = line.split()

        if not len(split):
            continue
        if split[0] == "v":
            vertexList.append(map(float, split[1:]))
            didReadVertex = True
        else:
            if didReadVertex  == False:
                vertexBeforeTxt += line
            else:
                vertexAfterTxt += line

    objFile.close()

    return vertexList, vertexBeforeTxt, vertexAfterTxt

def objSave(name, vertexList, vertexBeforeTxt, vertexAfterTxt):
    objFile = open(name, 'w')

    objFile.write(vertexBeforeTxt)

    for item in vertexList:
        sum = ''

        for small_item in item:
            sum += ' ' + str(small_item)

        objFile.write('v ' + sum + '\n')

    objFile.write(vertexAfterTxt)

    objFile.close()

if __name__ == "__main__":
    vertexList, vertexBeforeTxt, vertexAfterTxt = objVertexExtract('../3dModels/rightSlipper.obj')

    for i in range(len(vertexList)):
        vertexList[i][0] *= 2.0

    objSave('../3dModels/newObj.obj', vertexList, vertexBeforeTxt, vertexAfterTxt)

