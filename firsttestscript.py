import math
x = float(input("Pixels from the top left corner of the image on the X axis "))
y = float(input("Pixles from the top left corner of the image on the Y axis "))
focalLength = float(input("Focal length of lens "))
mmWidthPerPixel = float(input("Width per pixel in mm "))
ccdHeightPixels = float(input("CCD Height per Pixel in mm "))
pixelAspectRatio = float(input("Aspect ratio of each pixel "))
imageWidth = float(input("Width of image "))
imageHeight = float(input("Height of image "))
digitalZoomRatio = float(input("Digital zoom ratio of image, set to 1 if uncropped. "))
scaleRatio = imageWidth * digitalZoomRatio / mmWidthPerPixel
alphaX = focalLength/mmWidthPerPixel
alphaY = alphaX/pixelAspectRatio
fx = alphaX
fy = alphaY
cx = imageWidth/2.0
cy = imageHeight/2.0
xDistorted = x - cx
yDistorted = y - cy
yNormalized = (yDistorted)/fy
xNormalized = (xDistorted)/fx
yUndistorted = yDistorted
xUndisorted = xDistorted
k1 = float(input("Radial Distortion of lens R1 "))
k2 = float(input("Radial Distortion of lens R2 "))
k3 = float(input("Radial Distortion of lens R3 "))
p1 = float(input("Tangential distortion of lens T1 "))
p2 = float(input("Tangential distortion of lens T2 "))
yCorrectedNormalized = yNormalized
xCorrectedNormalized = xNormalized
if(k1 != 0) and (k2 != 0) and (k3 != 0) and (p1 != 0) and (p2 != 0):
    r2 = (xNormalized*xNormalized)+ (yNormalized*yNormalized)
    r4 = r2 * r2
    xCorrectedNormalized = xNormalized * (1 + k1 * r2 + k2 * r4)
    yCorrectedNormalized = yNormalized * (1 + k1 * r2 + k2 * r4)
    xCorrectedNormalized = xCorrectedNormalized + (2 * p1 * xNormalized * yNormalized + p2 * (r2 + 2 * xNormalized * xNormalized))
    yCorrectedNormalized = yCorrectedNormalized + (p1 * (r2 + 2 * yNormalized * yNormalized) + 2 * p2 * xNormalized * yNormalized)
xUndistorted = xCorrectedNormalized * fx
yUndistorted = yCorrectedNormalized * fy
azimuth = math.atan2(xUndistorted, fx)
elevation = math.atan2(yUndistorted, fy)

adjustAzimith = math.degrees(azimuth)
adjustElevation = math.degrees(elevation)
print(adjustAzimith)
print(adjustElevation)
