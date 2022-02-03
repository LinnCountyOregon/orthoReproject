# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# orthoReproject.py
# Created on: 2018-06-28 12:20:22.00000
#   
# Description: Reproject a directory of arcGIS grid images into WGS_1984_Web_Mercator_Auxiliary_Sphere
#   and auto detect transformation and cell size conversion.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, os, sys
# from arcpy.sa import *

#outDir = "\\\\LC-GIS\\f\\orthos_2017_final_Delivery\\Orthos2017_WebMercator.gdb"
#outDir = "\\\\LC-GIS\\f\\Historic_Aerial_Photos\\1948_grid_webMercator"
#outDir = "\\\\LC-GIS\\f\\LebanonOrthos_2017\\Lebanon\\Raster\\2017\\Raster Data\\Lebanon2017_Orthos_webM.gdb"
#outDir = "\\\\LC-GIS\\f\\albany2002\\test\\webmercator_2\\albany2002_orthos_webm.gdb"
#outDir = "\\\\lc-gis\\f\\Historic_Aerial_Photos\\1975_Aerials\\Aerials_1975_webM.gdb"
#outDir = "\\\\lc-gis\\f\\Historic_Aerial_Photos\\Orthos_1996_webMercator.gdb"
#outDir = "\\\\lc-gis\\f\\Orthos2021\\Orthos2021_Lyons_Mill_City_webMercator.gdb"
#outDir = "\\\\lc-gis\\f\\Orthos2021\\Orthos2021_Linn_County_webMercator.gdb"
outDir = "\\\\lc-gis\\f\\Orthos2021\\Orthos2021_revised_Linn_County_webMercator.gdb"

if not arcpy.Exists(outDir):
    print("Creating geodatabase")
    arcpy.CreateFileGDB_management("\\\\lc-gis\\f\\Orthos2021","Orthos2021_revised_Linn_County_webMercator.gdb")

# get list of rasters from existing directory
arcpy.env.workspace = "\\\\lc-gis\\f\\Orthos2021\\210004 Linn County - Revised\\Revised Orthophotography Data\\GeoTIFF"
rasterList = arcpy.ListRasters()

# get list of rasters from existing raster catalog
# rasterList = []
# with arcpy.da.SearchCursor("\\\\LC-GIS\\ortho4\\Orthos96\\Orthos96_Catalog.dbf",['IMAGE']) as cursor:
#     for row in cursor:
#        rasterList.append(row[0])


# Local variables:
# inCoordSys1 = "PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl',GEOGCS['GCS_NAD83_WASHINGTON_OREGON_HPGN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['false_easting',8202099.737532808],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-120.5],PARAMETER['standard_parallel_1',44.33333333333334],PARAMETER['standard_parallel_2',46.0],PARAMETER['latitude_of_origin',43.66666666666666],UNIT['Foot',0.3048]]"
inCoordSys2 = "PROJCS['NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl',GEOGCS['GCS_North_American_1983_HARN',DATUM['D_North_American_1983_HARN',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',8202099.737532808],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-120.5],PARAMETER['Standard_Parallel_1',44.33333333333334],PARAMETER['Standard_Parallel_2',46.0],PARAMETER['Latitude_Of_Origin',43.66666666666666],UNIT['Foot',0.3048]]"
outCoordSys = "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"

# the transformation only seems to be needed with the GCS_North_American_1983 input, not the GCS_NAD83_WASHINGTON_OREGON_HPGN

# cellSize for 1948 tiff reproject to meters
#cellSize = "0.3 0.3"
# cellSize for 2017 Lebanon 0.25 ft reproject to meters (1.44x0.3048xcellSizeInFt)
# cellSize for 1967 photos
#cellSize = "0.65 0.65"
# cellSize for 1975 photos
# cellSize = "2.8 2.8"
# cellSize for 1978 photos (4.8 ft x 0.3048)
# cellSize = "1.45 1.45"

# rasterList = ["\\\\LC-GIS\\ortho1\\orthos_2000\\14s03w\\14s03wa.tif"]
for rasterName in rasterList:
    if arcpy.Exists(rasterName):
        # reproject each raster in the workspace
        outRasterName = os.path.split(rasterName)[1]
        outRasterName = 'webM_' + os.path.splitext(outRasterName)[0]
        outRasterName = outRasterName.replace(' ','_')
        outRasterName = outRasterName.replace('-','_')
        inCoordSys = str(arcpy.CreateSpatialReference_management("", rasterName))
        print("**Reprojecting: " + rasterName + " with input projection: " + inCoordSys)
    
        # check for projection unknown
        if 'B286C06B-0879-11D2-AACA-00C04FA33C20' in inCoordSys:
            print("** Coordinate system unknown ** Setting to StatePlane_Oregon_North_FIPS_3601_Feet_Intl")
            arcpy.DefineProjection_management(rasterName, inCoordSys2)
            inCoordSys = str(arcpy.CreateSpatialReference_management("", rasterName))

        # check for state plane input projection
        if not 'NAD_1983_HARN_StatePlane_Oregon_North_FIPS_3601_Feet_Intl' in inCoordSys:
            print("*************Alert! input coordinate system is not FIPS 3601 StatePlane")

        runReproject = 1
        transForm = ""

        if 'GCS_North_American_1983_HARN' in inCoordSys:
            transForm = "NAD_1983_HARN_To_WGS_1984_2"
        elif 'GCS_NAD83_WASHINGTON_OREGON_HPGN' in inCoordSys:
            print("HPGN detected. No transformation.")
        else:
            print("Error!! input coordiate system not recognized")
            runReproject = 0

        print("... and transformation: " + transForm)

        # get cellSize of input raster
        cellSizeResult = arcpy.GetRasterProperties_management(rasterName, "CELLSIZEX")
        print("... and input cell size: " + cellSizeResult.getOutput(0))

        # convert cell size from feet to meters and also a conversion factor that seems necessary because of the projection. Otherwise input and output cell size will be different.
        cellSizeFloat = float(cellSizeResult.getOutput(0)) * 0.3048 * 1.333
        cellSize = str(cellSizeFloat) + " " + str(cellSizeFloat)

        # Process: Project Raster
        if runReproject:
            if not arcpy.Exists(outDir + "\\" + outRasterName):
                arcpy.ProjectRaster_management(rasterName, outDir + "\\" + outRasterName, outCoordSys, "CUBIC", cellSize, transForm, "0 0", inCoordSys, "NO_VERTICAL")
        # rasterFeet = arcpy.Raster(outDir + "\\" + rasterName) / 0.3048
        # rasterFeet.save(outDir + "\\" + os.path.splitext(rasterName)[0] + "_ft.img")
        # delete the reprojected raster that has values in meters
        # arcpy.Delete_management(outDir + "\\" + rasterName)

print("done.")

