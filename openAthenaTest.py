from openAthenaComp import *

setVariables(21, 4056, 3040, 0,0,0,0,0,1,"northGA.tif")
lat,long,alt,terAlt = targetLocation(33.9365683, -84.5274698, 500, 126, 25, 2028, 1520, 0)
print(lat)
print(long)
print(alt)
print(terAlt)