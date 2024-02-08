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
import pyproj

def openAthena(lat,long,alt, azi,theta,pixelX, pixelY, focalLength,imageWidth,imageHeight,rollAngle,k1,k2,p1,p2,pixelAspectRatio):
    # replace this with filename of DEM you wish to use.
    #     if it is not in the same directory as this script, you will need to
    #     provide a complete file path.
    DEMFILENAME = "monroe_NY.tif"
    latitude = decimal.Decimal(lat)
    longitude = decimal.Decimal(long)
    alt = decimal.Decimal(alt)
    #WGS84 = pyproj.CRS.from_epsg(4326)
    #EGM96 = pyproj.CRS.from_epsg(5773)
    #trs = pyproj.Transformer.from_crs(WGS84, EGM96)
    #EGMLat, EGMLong, alt = trs.transform(latitude, longitude, alt)
    altitude = decimal.Decimal(alt) # altitude must be in EGM96 vertical datum, not WGS84
    # azimuth represents the direction of the aircraft's camera.
    # Starts from North @ 0°, increasing clockwise (e.g. 90° is East)
    azimuth = decimal.Decimal(azi)
    # theta represents degrees downwards from the horizon (forwards)
    theta = decimal.Decimal(theta)
    pixelX = decimal.Decimal(pixelX)
    pixelY = decimal.Decimal(pixelY)
    focalLength = decimal.Decimal(focalLength)
    imageWidth = decimal.Decimal(imageWidth)
    imageHeight = decimal.Decimal(imageHeight)
    rollAngle = decimal.Decimal(rollAngle)
    k1 = decimal.Decimal(k1)
    k2 = decimal.Decimal(k2)
    p1 = decimal.Decimal(p2)
    p2 = decimal.Decimal(p2)
    pixelAspectRatio = decimal.Decimal(pixelAspectRatio)

    AzimuthTheta = AzimuthThetaOffset(pixelX,pixelY,focalLength,imageWidth,imageHeight,rollAngle,1,k1,k2,p1,p2, pixelAspectRatio)
    offsetAzimuth, offsetTheta = AzimuthTheta
    #print(offsetAzimuth)
    #print(offsetTheta)
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
    #print(azimuth)
    #print(theta)
    #print(f'Calculated Target (lat,lon): {round(targetLat, 6)}, {round(targetLon, 6)} Alt: {round(targetAlt, 6)} meters AMSL')
    #print(f'estimated terrainAlt was: {round(terrainAlt,6)}')
    #print(f'Slant Range to Target was: {round(slantRangeToTarget,6)} meters'
    return ((round(targetLat,6), round(targetLon,6), round(targetAlt,6), round(terrainAlt, 6)))

#if __name__ == "__main__":
#    main()
def Targeting(lat, long, alt, azi, theta, pixelX, pixelY, rollAngle):
    """
    lat = Latitude of plane in decimal format
    long = Longitude of plane in decimal format
    alt = Altitude of plane in EGM96 format 
    azi = Degrees camera is facing - 0 is north, 180 is south, 90 is east, 270 is west.
    theta = Angle camera is facing downwards. Make sure to add plane inclination downwards as well - otherwise results may be innacurate.
    pixelX = The pixels from the top left of the image of the target on the X axis.
    pixelY = The pixels from the top left of the image of the target on the Y axis.
    rollAngle = the yaw of the plane.
    
    All inputs are taken as decimals, but any integer or float input will work.

    Returns tuple of latitude of target, longitude of target, EGM96 altitude of target, and ground altitude of target.
    """
    return openAthena(lat, long, alt, azi, theta, pixelX, pixelY, 21, 4056, 3040, rollAngle, .134437, -.24607, -0.000175531, -0.000580392, 1)

latt, longg, altt, terr = Targeting(43.164885, -77.471996, 174.565, 250, -26, 2028, 1520, 0.483809)
print(latt)
print(longg)
print(altt)
print(terr)