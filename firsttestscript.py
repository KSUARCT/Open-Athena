import math
x = float(input("Pixels from the top left corner of the image on the X axis "))
y = float(input("Pixles from the top left corner of the image on the Y axis "))
focalLength = float(input("Focal length of lens "))
mmWidthPerPixel = float(input("Width per pixel in mm "))
ccdHeightPixels = float(input("Height per Pixel in mm "))
pixelAspectRatio = mmWidthPerPixel/ccdHeightPixels
imageWidth = float(input("Width of image "))
imageHeight = float(input("Height of image "))
roll = float(input("roll"))
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
#k3 = float(input("Radial Distortion of lens R3 "))
p1 = float(input("Tangential distortion of lens T1 "))
p2 = float(input("Tangential distortion of lens T2 "))
yCorrectedNormalized = yNormalized
xCorrectedNormalized = xNormalized
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

azimuth = math.degrees(azimuth)
elevation = math.degrees(elevation)
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