"""fileConversionDEM.py

DESCRIPTION:
------------
    This file takes in several DEM files, re-projects them with respect to a
    known file that you're already working with in the map-frame, and finally
    converts the .dem file to a general Grid file.

SOURCES:
--------
    http://gis.stackexchange.com/questions/12464/adding-raster-layer-without
    -lyr-file-using-arcpy
        This source was used for the adding the merged raster to a saved
        project.It is for ArcGIS for Desktop, so I had to make some conversions.

AUTHOR:
-------

    Nicholas P. Taliceo
    Em. Nicholas.Taliceo@utdallas.edu   Web. www.NicholasTaliceo.com

18 December 2016
"""

import arcpy
import os

folder = input("Please your working directory: ")
print("The folder location has been set!" + "\n")
arcpy.env.workspace = folder
os.chdir(folder)

# PART 2a.--Read in the DEM files into a new list for further usage.------------
# Create an empty list to store the DEM file locations.
dems = []
# Iterate through the files in the particular folder, only selecting DEMs.
for filename in os.listdir(folder):
    if filename.endswith(".dem") or filename.endswith(".DEM"):
        # Append the DEM file names to the 'dems' list.
        dems.append(filename)
    else:
        pass

# Create a list no_extension which is the dems list sans extension
# no_extension will be used to save the DEM converted files.
no_extension = []
for dem in dems:
    no_extension.append(dem[0:-4] + ".tif")

# PART 2b.--Re-project the DEM files with respect to another file.--------------
proj_prompt = input("Would you like to re-project your DEM files (Y/N)? ")
if proj_prompt.lower() == 'y':
    # Ask the user for the file they wish to project by.
    coor_system = input("Please provide the data set that you wish to project "
                        "these files by: ")
    for dem in dems:
        # Re-project each DEM file in DEMs to the known coordinate system.
        arcpy.DefineProjection_management(dem, coor_system)
else:
    pass

# PART 2c.--DEM conversion to another general raster feature class.-------------
raster_prompt = input("Convert the DEM files to raster (Y/N)? ")
dems_converted = []
if raster_prompt.lower() == 'y':
    # Iterate through the list of DEM files.
    i = 0
    while i < len(dems):
        arcpy.DEMToRaster_conversion(folder + "\\" + dems[i],
                                     folder + "\\" + no_extension[i])
        dems_converted.append(folder + "\\" + no_extension[i])
        i += 1
else:
    pass

# PART 2d.--Merge the DEMs together via mosaic to new raster.-------------------
mosaic_prompt = input("\n" + "Create a new raster mosaic of the dem files (Y/N)? ")
# This is the name of the new merged raster.
mosaic_name = "merged_rasters.tif"
# There are two options--the user either defined chose to convert the DEMs to
# a regular Esri grid or not.  We need to merge whichever one the user chose.
if mosaic_prompt.lower() == 'y':
    # If the DEMs were converted to another raster, then...
    if raster_prompt.lower() == 'y':
        dems_converted_semi = ""
        print("\n" + "The files to be merged are: ")
        print(dems_converted)
        # Before you start merging the rasters, ask to exclude extraneous files.
        exclude = input("Do you want to exclude some DEM files (Y/N)?: ")
        while exclude.lower() == 'y':
            excludeRaster = input("Please input a  file, with its extension: ")
            dems_converted.remove(excludeRaster)
            exclude = input("Exclude another file (Y/N)?: ")
        # The input rasters need to be a string of rasters separated by a comma;
        # we need to take the list of rasters and convert to a string.
        for i in dems_converted:
            if i != dems_converted[-1]:
                dems_converted_semi = dems_converted_semi + i + ";"
            else:
                dems_converted_semi = dems_converted_semi + i
        arcpy.MosaicToNewRaster_management(dems_converted_semi, folder,
                                           mosaic_name, number_of_bands=1)
    # If the user chose not to convert to a general raster, then do this...
    if raster_prompt.lower() != 'y':
        dems_converted_semi = ""
        print("\n" + "The files to be merged are: ")
        print(dems)
        # Before you start merging the rasters, ask to exclude extraneous files.
        exclude = input("Do you want to exclude some DEM files (Y/N)?: ")
        while exclude.lower() == 'y':
            excludeRaster = input("Please input a  file, with its extension: ")
            dems.remove(excludeRaster)
            exclude = input("Exclude another file (Y/N)?: ")
        # Ibid.
        for i in dems:
            if i != dems[-1]:
                dems_converted_semi = dems_converted_semi + i + ";"
            else:
                dems_converted_semi = dems_converted_semi + i
        arcpy.MosaicToNewRaster_management(dems_converted_semi, folder,
                                           mosaic_name, number_of_bands=1)
if mosaic_prompt.lower != 'y':
    pass

# PART 2e.--Take the new merged raster and add it to a pre-existing map.--------
import_prompt = input("\n" + "Add the merged raster mosaic to your map (Y/N)? ")
if import_prompt.lower() == "y":
    # Ask the user to input the .aprx file link.
    project = input("Please input the entire path name of the .aprx file "
                    "of map being worked on: ")
    # Create a variable declaring the ArcGIS Pro project.
    aprx = arcpy.mp.ArcGISProject(project)
    # Creates a map variable; assumes that only one map is present.
    map_current = aprx.listMaps()[0]
    print("A map has been found!")
    # Declare a variable representing the pathname of the variable.
    raster_path = folder + "//" + mosaic_name
    # Declare a variable representing the raster's name in the map.
    raster_lyr_name = "Merged DEM Raster Mosaic"
    print("Adding the raster mosaic to your project...")
    # Create a temporary raster layer.
    add_raster = arcpy.MakeRasterLayer_management(raster_path, raster_lyr_name)
    layer = add_raster.getOutput(0)
    # Add the temporary raster layer to the map and save.
    map_current.addLayer(layer)
    aprx.save()
    print("\n" + "The raster mosaic has been successfully added to your project!")
else:
    pass

input("\n" + "Press ENTER to continue.")
print("\n" + "This script has ended.  Goodbye!")