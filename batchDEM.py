"""batchDEM.py

DESCRIPTION:
------------
    The purpose of this script is to batch download all DEM files that are
    located on a particular website.  To make this easier for the user, several
    options are given to the user, of which are described below:
        1. Asks the user what website to parse and where to store the data.
        2. Downloads any and all files that are ZIP files (how DEMs are stored).
        3. Extracts data in the ZIP files and then deletes the ZIP files as to
           avoid extraneous information.
        4. Gives the user to re-project all DEM files that were downloaded with
           respect to another feature class that is already defined.
        5. Gives the user the option to change the file type of these DEM files
           to a general raster grid file.
        6. Allows for the user to merge the DEM files into one cohesive raster
           file.  Also available is the option to exclude some DEM files.  This
           is because in some instances, websites have some data which could
           potentially overlap with other files.  This is optional.
        7. Allows the user to then take this merged mosaic and add it into a
           map that they are currently working on.  Note that the map must
           already exist for this option to work.
SOURCES:
--------
    MOUSE VS. PYTHON:
    ----------------
        http://www.blog.pythonlibrary.org/2012/06/07/python-101-how-
        to-download-a-file/
    BEAUTIFUL SOUP DOCUMENTATION:
    -----------------------------
        https://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup
    zipfile ONLINE DOCUMENTATION:
    -----------------------------
        https://docs.python.org/3/library/zipfile.html
    THREAD: DELETING FILES WITH PYTHON:
    -----------------------------------
        http://forums.devshed.com/python-programming-
            11/deleting-files-python-108565.html
    urllib.request DOCUMENTATION:
    -----------------------------
        https://docs.python.org/3/library/urllib.request.html
    Adding a new raster to ArcGIS Pro:
    ----------------------------------
        http://gis.stackexchange.com/questions/12464/adding-raster-layer-without
            -lyr-file-using-arcpy
            This source was used for the adding the merged raster to a saved
            project.It is for ArcGIS for Desktop, so I had to make
            some conversions.
AUTHOR:
-------
    Nicholas P. Taliceo
    Em. Nicholas.Taliceo@utdallas.edu   Web. www.NicholasTaliceo.com

18 December 2016
"""

import arcpy
import os
import urllib.request
# Needs to be manually installed.  See Beautiful Soup documentation.
import bs4
import requests
import zipfile

# Have the DEM files all saved in a single folder. This folder location will
# then be stored as the arcpy.env.workspace.
folder = input("\n" + "Please your working directory: ")
print("The folder location has been set!\n")
arcpy.env.workspace = folder
os.chdir(folder)

# ------------------------------------------------------------------------------
# PART 1--Downloading DEM files from the web.-----------------------------------
# ------------------------------------------------------------------------------

# Input the url that we are trying to parse.
url = input("Please input the url link EXACTLY as it appears in your browser: ")
print("Searching through the input url...")

# PART 1a.--Use BeautifulSoup to open a link and view its HTML contents.--------
while True:
    try:
        connection = urllib.request.urlopen(url)
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        connection.close()
        break
    except (ValueError, urllib.error.URLError):
        url = input("That's not a valid url.  Please try again: ")

# PART 1b.--Parse the HTML and search for the <a> tags, containing links.-------
print("Finding downloadable files...")
# For the entire HTML document, look for all of the 'a' tags, which
# go along with the <a href="LINK_HERE"></a> format.
aTags = soup.find_all('a')
# Put all <a href="..."></a> in a list.  If part of the main link (which
# downloads usually are, then it just stores the relevant pathname).
raw_links = []
# Put all of the .zip file links (that's how DEMs are stored online) in a list.
download_links = []
# Find all of the <a>'s.
for link in aTags:
    raw_links.append(link.get('href'))
# Put all of the .zip links from raw_links in a new list.
for link in raw_links:
    if type(link) == str:
        if link[-3:] == 'zip':
            download_links.append(link)

# PART 1c.--Find the main URL (i.e., before the .com) and .zip file extension.--
# Determine how many dashes it takes from the end to get to the .com.
dashes = url.count('/') - 2
# Split the entire extension from url away from the .com.
main_url = url.rsplit('/', dashes)[0]

# PART 1d.--Download each link contained on the main webpage.-------------------
print("Downloading DEM files to your local folder...")
for zip in download_links:
    # Get the full download link.
    zip_url = main_url + zip
    # Find the number of '/' in the zip_url extension.
    dashes_zip_url = zip_url.count('/')
    # Save the basename of each file as: base-name.zip
    file_name = zip_url.rsplit('/', dashes_zip_url)[dashes_zip_url]
    try:
        f = urllib.request.urlopen(zip_url)
        print('Downloading %s' % file_name)
        data = f.read()
        # Writes the zip file to your current directory.
        if __name__ == '__main__':
            with open(file_name, "wb") as code:
                code.write(data)
                z = zipfile.ZipFile(file_name)
                # Extracts the contents within the zip files to a new folder
                # of the same name, sans the '.zip' ending.
                newPath = folder + '//' + file_name[:-4]
                z.extractall(newPath)
                z.close()
        path_name = folder
        # Deletes the .zip file to avoid too many folders within directory.
        os.remove(path_name + '\\' + file_name)
    except (urllib.error.HTTPError):
        print("The file %s does not exist! Trying the next file..." % file_name)
        pass

for folders in os.listdir(folder):
    # Check to see if the folder is actually a folder and not a file.
    if os.path.isfile(folders) == True:
        pass
    # If the folder is a folder with contents in it, then do the following:
    elif os.path.isfile(folders) == False:
        for files in os.listdir(folders):
            if __name__ == '__main__':
                if files.endswith('.dem'):
                    # Rename the .dem files within the folders to have the same
                    # names as the parent folders.
                    newName = folders + '.dem'
                    newFile = os.replace(
                        os.path.realpath(folders) + '\\' + files,
                        os.path.realpath(folders) + '\\' + newName)
                    # Now, use os.replace() to copy this newly named file and
                    # save it in the main folder
                    os.replace(os.path.realpath(folders) + '\\' + newName,
                               os.path.realpath(folder) + '\\' + newName)
    else:
        pass

print("\n" + "Files have successfully finished downloading! Congratulations!")

# ------------------------------------------------------------------------------
# PART 2--Performing geoprocessing operations on the downloaded DEMs.-----------
# ------------------------------------------------------------------------------

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
input("")
proj_prompt = input("\n" + "Would you like to re-project your DEM files (Y/N)? ")
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
raster_prompt = input("\n" + "Convert the DEM files to other format (Y/N)? ")
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
        exclude = input("\n" + "Do you want to exclude some DEM files (Y/N)?: ")
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
        exclude = input("\n" + "Do you want to exclude some DEM files (Y/N)?: ")
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
    print("aprx variable successfully created!")
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
