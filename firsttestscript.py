import math
xa = float(input("Pixels from the top left corner of the image on the X axis "))
ya = float(input("Pixles from the top left corner of the image on the Y axis "))
focalLength = float(input("Focal length of lens in 35mm format "))
mmWidthPerPixel = float(input("Width per pixel in mm "))
ccdHeightPixels = float(input("Height per Pixel in mm "))
imageWidth = float(input("Width of image "))
imageHeight = float(input("Height of image "))
pixelAspectRatio = 4/3
roll = float(input("roll"))
digitalZoomRatio = float(input("Digital zoom ratio of image, set to 1 if uncropped. "))
scaleRatio = imageWidth * digitalZoomRatio / mmWidthPerPixel
alphaX = (imageWidth * digitalZoomRatio) * focalLength / 36.0 
alphaY = alphaX / pixelAspectRatio
fx = alphaX
fy = alphaY
cx = imageWidth/2.0
cy = imageHeight/2.0
xDistorted = xa - cx
yDistorted = ya - cy
xNormalized = xDistorted/fx
yNormalized = yDistorted/fy
xUndistorted = xDistorted
yUndistorted = yDistorted
k1 = float(input("Radial Distortion of lens R1 "))
k2 = float(input("Radial Distortion of lens R2 "))
#k3 = float(input("Radial Distortion of lens R3 "))
p1 = float(input("Tangential distortion of lens T1 "))
p2 = float(input("Tangential distortion of lens T2 "))
x = xNormalized
y = yNormalized
r2 = x*x + y*y
r4 = r2 * r2
xCorrectedNormalized = x * (1 + k1 * r2 + k2 * r4)
yCorrectedNormalized = y * (1 + k1 * r2 + k2 * r4)
print(yCorrectedNormalized)
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