#!/usr/bin/env python3
import sys
import math
from math import sin, asin, cos, atan2, sqrt
import decimal # more float precision with Decimal objects
from geotiff import GeoTiff
decimal.getcontext().prec = 30
from parseGeoTIFF import getAltFromLatLon, binarySearchNearest, getGeoFileFromUser, getGeoFileFromString
from getTarget import *
from AzimuthThetaOffset import *
def main():
    # replace this with filename of DEM you wish to use.
    #     if it is not in the same directory as this script, you will need to
    #     provide a complete file path.
    DEMFILENAME = "monroe_NY.tif"
    latitude = decimal.Decimal(input("Latitude "))
    longitude = decimal.Decimal(input("Longitude "))
    altitude = decimal.Decimal(input("Altitude ")) # altitude must be in EGM96 vertical datum, not WGS84
    # azimuth represents the direction of the aircraft's camera.
    # Starts from North @ 0°, increasing clockwise (e.g. 90° is East)
    azimuth = decimal.Decimal(input("Azimuth "))
    # theta represents degrees downwards from the horizon (forwards)
    theta = decimal.Decimal(input("Theta "))
    pixelX = decimal.Decimal(input("X axis pixel selection "))
    pixelY = decimal.Decimal(input("Y axis pixel selection "))
    focalLength = decimal.Decimal(input("focal length "))
    imageWidth = decimal.Decimal(input("image width "))
    imageHeight = decimal.Decimal(input("image Height "))
    rollAngle = decimal.Decimal(input("rollAngle "))
    k1 = decimal.Decimal(input("k1 "))
    k2 = decimal.Decimal(input("k2 "))
    p1 = decimal.Decimal(input("p1 "))
    p2 = decimal.Decimal(input("p2 "))

    AzimuthTheta = AzimuthThetaOffset(pixelX,pixelY,focalLength,4056,3040,imageWidth,imageHeight,rollAngle,1,k1,k2,p1,p2)
    offsetAzimuth, offsetTheta = AzimuthTheta
    print(offsetAzimuth)
    print(offsetTheta)
    offsetAzimuth = decimal.Decimal(offsetAzimuth)
    offsetTheta = decimal.Decimal(offsetTheta)
    azimuth = azimuth+offsetAzimuth
    theta = theta-offsetTheta

    # Load GeoTIFF Digital Elevation Model and its parameters
    elevationData, (x0, dx, dxdy, y0, dydx, dy) = getGeoFileFromString(DEMFILENAME)
    nrows, ncols = elevationData.shape
    x1 = x0 + dx * ncols
    y1 = y0 + dy * nrows
    xParams = (x0, x1, dx, ncols)
    yParams = (y0, y1, dy, nrows)

    # calculate target
    target = resolveTarget(latitude, longitude, altitude,  azimuth, theta, elevationData, xParams, yParams)

    # break out tuple representing target into component parts
    slantRangeToTarget, targetLat, targetLon, targetAlt, terrainAlt = target

    # print out the results. Replace this with whatever output format you desire.
    print(azimuth)
    print(theta)
    print(f'Calculated Target (lat,lon): {round(targetLat, 6)}, {round(targetLon, 6)} Alt: {round(targetAlt, 6)} meters AMSL')
    print(f'estimated terrainAlt was: {round(terrainAlt,6)}')
    print(f'Slant Range to Target was: {round(slantRangeToTarget,6)} meters')


if __name__ == "__main__":
    main()
