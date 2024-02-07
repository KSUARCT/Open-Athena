import math
import decimal
decimal.getcontext().prec = 30
def AzimuthThetaOffset(xa,ya,focalLength,mmWidthPerPixel,ccdHeightPixels,imageWidth,imageHeight,roll,digitalZoomRatio,k1,k2,p1,p2):

    #xa = decimal.Decimal(input("Pixels from the top left corner of the image on the X axis "))
    #ya = decimal.Decimal(input("Pixles from the top left corner of the image on the Y axis "))
    #focalLength = decimal.Decimal(input("Focal length of lens in 35mm format "))
    #mmWidthPerPixel = decimal.Decimal(input("Width per pixel in mm "))
    #ccdHeightPixels = decimal.Decimal(input("Height per Pixel in mm "))
    #imageWidth = decimal.Decimal(input("Width of image "))
    #imageHeight = decimal.Decimal(input("Height of image "))
    #roll = decimal.Decimal(input("roll"))
    #digitalZoomRatio = decimal.Decimal(input("Digital zoom ratio of image, set to 1 if uncropped. "))
    xa = decimal.Decimal(xa)
    ya = decimal.Decimal(ya)
    focalLength = decimal.Decimal(focalLength)
    mmWidthPerPixel = decimal.Decimal(mmWidthPerPixel)
    ccdHeightPixels = decimal.Decimal(ccdHeightPixels)
    imageWidth = decimal.Decimal(imageWidth)
    imageHeight = decimal.Decimal(imageHeight)
    roll = decimal.Decimal(roll)
    digitalZoomRatio = decimal.Decimal(digitalZoomRatio)

    pixelAspectRatio = decimal.Decimal(4/3)
    #scaleRatio = imageWidth * digitalZoomRatio / mmWidthPerPixel
    alphaX = (imageWidth * digitalZoomRatio) * focalLength / decimal.Decimal(36.0) 
    alphaX = decimal.Decimal(alphaX)
    alphaY = alphaX / pixelAspectRatio
    fx = alphaX
    fy = alphaY
    cx = imageWidth/decimal.Decimal(2)
    cy = imageHeight/decimal.Decimal(2)
    xDistorted = xa - cx
    xDistorted = decimal.Decimal(xDistorted)
    yDistorted = ya - cy
    yDistorted = decimal.Decimal(yDistorted)
    xNormalized = xDistorted/fx
    yNormalized = yDistorted/fy
    xUndistorted = xDistorted
    yUndistorted = yDistorted
    #k1 = decimal.Decimal(input("Radial Distortion of lens R1 "))
    #k2 = decimal.Decimal(input("Radial Distortion of lens R2 "))
    #k3 = decimal.Decimal(input("Radial Distortion of lens R3 "))
    #p1 = decimal.Decimal(input("Tangential distortion of lens T1 "))
    #p2 = decimal.Decimal(input("Tangential distortion of lens T2 ")) 
    x = xNormalized
    y = yNormalized
    r2 = x*x + y*y
    r4 = r2 * r2
    xCorrectedNormalized = x * (1 + k1 * r2 + k2 * r4)
    yCorrectedNormalized = y * (1 + k1 * r2 + k2 * r4)
    xCorrectedNormalized = xCorrectedNormalized + (2 * p1 * x * y + p2 * (r2 + 2 * x * x))
    yCorrectedNormalized = yCorrectedNormalized + (p1 * (r2 + 2 * y * y) + 2 * p2 * x * y)
    xUndistorted = xCorrectedNormalized * fx
    yUndistorted = yCorrectedNormalized * fy
    azimuth = math.atan2(xUndistorted, fx)
    elevation = math.atan2(yUndistorted, fy)

    azimuth = math.degrees(azimuth)
    elevation = math.degrees(elevation)
    print(azimuth)
    print(elevation)
    psi = azimuth
    theta = elevation
    cameraRoll = roll
    theta = -1.0 * theta
    psi = math.radians(psi)
    theta = math.radians(theta)
    cameraRoll = math.radians(cameraRoll)
    x = math.cos(theta) * math.cos(psi)
    y = math.cos(theta) * math.sin(psi)
    z = math.sin(theta)
    rotationMatrix = [[1,0,0], [0, math.cos(cameraRoll), -math.sin(cameraRoll)], [0, math.sin(cameraRoll), math.cos(cameraRoll)]]
    rotatedVector = [rotationMatrix[0][0] * x + rotationMatrix[0][1] * y + rotationMatrix [0][2] * z,rotationMatrix[1][0] * x + rotationMatrix[1][1] * y + rotationMatrix [1][2] * z,rotationMatrix[2][0] * x + rotationMatrix[2][1] * y + rotationMatrix [2][2] * z]
    correctedPsi = math.atan2(rotatedVector[1], rotatedVector[0])
    correctedTheta = math.atan2(rotatedVector[2], math.sqrt(rotatedVector[0] * rotatedVector[0] + rotatedVector[1] * rotatedVector[1]))
    correctedPsi = math.degrees(correctedPsi)
    correctedTheta = math.degrees(correctedTheta)
    correctedTheta = correctedTheta * -1


    print(correctedPsi)
    print(correctedTheta)
    return correctedPsi, correctedTheta