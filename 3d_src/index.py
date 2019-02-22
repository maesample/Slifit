import objParser as op
import sizeParser as sp

if __name__ == "__main__":
    vertexList, vertexBeforeTxt, vertexAfterTxt = op.objVertexExtract('../3dModels/rightSlipper.obj')
    verticalSize, horizontalSizeList = sp.sizeExtracter("./out_size.txt")

    modelVerticalMax = 112.5584
    modelVerticalMin = -198.523
    modelVerticalSize = modelVerticalMax - modelVerticalMin
    modelVerticalCenter = modelVerticalSize / 2

    A4VerticalSize = 297
    A4HorizontalSize = 210
    A4VerticalCenter = A4VerticalSize / 2
    A4HorizontalCenter = A4HorizontalSize / 2

    for i in range(len(vertexList)):
        # vertexList[i][0] *= 2.0
        # if i < (len(vertexList) / 2):
        #     vertexList[i][0] *= 2.0
        # else:
        #     vertexList[i][0] *= -2.0
        vertexRatio = (vertexList[i][2] - modelVerticalMin) / modelVerticalSize
        RatioFitVertexList = list(filter(lambda x: (x[2] / verticalSize) > vertexRatio, horizontalSizeList))
        # RatioFitVertexList = map(lambda x: (x[2] / verticalSize) > vertexRatio, horizontalSizeList)
        # print(RatioFitVertexList[0])

        if not len(RatioFitVertexList):
            continue
        else:
            RatioFitVertex = RatioFitVertexList[0]
            # print(RatioFitVertex)
            #
            if vertexList[i][0] > 0:
                print((A4HorizontalCenter - RatioFitVertex[0]))
                vertexList[i][0] *= (A4HorizontalCenter - RatioFitVertex[0])
            else:
                print((RatioFitVertex[1] - A4HorizontalCenter))
                vertexList[i][0] *= (RatioFitVertex[1] - A4HorizontalCenter)

    op.objSave('../3dModels/0221obj2.obj', vertexList, vertexBeforeTxt, vertexAfterTxt)
