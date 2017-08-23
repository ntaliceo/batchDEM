----------
README.txt
----------

----------------------------
AUTHOR & CONTACT INFORMATION
----------------------------

Nicholas P. Taliceo
Em.  Nicholas.Taliceo@utdallas.edu
Web. www.NicholasTaliceo.com

------------------
DATE LAST MODIFIED
------------------

12 December 2016

------------------------
FOLDER TABLE OF CONTENTS
------------------------

1. README.txt
2. batchDEM.py
3. webScrapeDEM.py
4. fileConversionDEM.py
5. output (folder)
6. demo (folder)
	
----------------------------
INDIVIDUAL FILE DESCRIPTIONS
----------------------------

1. README.txt

	The README file for this folder.

2. batchDEM.py

	This is a Python 3 file that is designed to batch download all files 
	from a user-specified webpage as .ZIP files, and then extracting all 
	.dem files to the main folder, specified by the user.
	
	From there, the user has several options to modify and work with these 
	.dem files:
	
		1. The user can specify where to store the files and from what
		   web address the script should search through.
		2. Downloads any and all files from the web as .zip files and then 
		   extracts the .dems files, yet retains the other files for future
		   use and/or reference.  Note that the script will automatically
		   rename the .dem files to the name of its parent folder in order to
		   ensure name uniqueness and to avoid overwriting data.
		3. Deletes the ZIP files to avoid storing extraneous information.  
		   Note that the script automatically extracts the ZIP files to a 
		   new folder of the same name.
		4. Gives the user the ability to re-project the newly downloaded .dem
		   files to a pre-existing file, such as a shapefile.  Note that one 
		   must give the complete path name, including the file's extension
		   in order for the script to perform this process.
		5. This script then gives the user the opportunity to change the 
		   file type from a .dem file to an Esri Grid file.  The user simply
		   needs to indicate yes or no (Y/N).
		6. The script allows the user to merge the DEM files into a new raster
		   mosaic.  Again, the user only needs to specify yes or no (Y/N).
		   Note that this option has the ability to exclude particular files,
		   such as potential replicas or otherwise undesired DEMs.
		7. Finally, if one is working with ArcGIS Pro and is currently working
		   in a project with other data, this script has the ability to 
		   incorporate this new raster mosaic into your current ArcGIS Pro
		   project by including the entire pathname of the .aprx file that
		   comprises your project.
		   
	This is the main file located in this folder, and is the primary script
	intended to be utilized by the end-user.
		
3. webScrapeDEM.py

	This is another Python 3 file that completes steps 1--3 of batchDEM.py.  
	The main purpose of this script is for the sole purpose of downloading
	several .dem files from the web, already knowing that the subsequent 
	options will not be utilized.  
	
	Note that this script will prompt the user to input a folder to store the
	downloaded data as well as prompt the user for a web address to download
	the data from.
	
4. fileConversionDEM.py

	This is another Python 3 file that completes steps 4--7 of batchDEM.py.
	The main purpose of this script is to use the latter options of 
	batchDEM.py when one already has several DEM files downloaded.
	
	Note that this script will again ask for a folder that contains the DEM 
	files.  All subsequent geoprocessing that is completed with the use of 
	this file will be stored in this folder.
	
5. output (folder)

	This is simply an empty folder that is intended to be a suggested 
	download and geoprocessing results location for work associated with the 
	aforementioned scripts.  That said, this folder is simply a suggestion, 
	and is no way hard-coded in any of the associated scripts.  
	
	Note:  this is NOT a default location--a folder location must always be 
	specified.

6. demo (folder)

	This is a folder that contains all of the components used in the 
	in-class demonstration on 06 December 2016.  Contents include: a short
	presentation file, another empty output file to save data, and a folder named
	"Nantucket" that contains shapefiles of Massachusetts, Nantucket County, and
	and ArcGIS Pro workspace associated with those files.
	
-------------
SPECIAL NOTES
-------------

i. Suggested (but not necessary) Website
----------------------------------------

The following website is the primary website that was used to complete 
tests and debugging:

http://www.webgis.com/terr_us75m.html

ii. When the script might break
-------------------------------

This will mainly occur if your files do not exist or if you give the incorrect
pathname.  Namely, if the file pathnames for your known shapefile (for DEM 
re-projection) or the .aprx ArcGIS Pro project is incorrect, the script will
likely crash.  Although this could be fixed by continually asking the user
to re-input the pathname, or just pass the task, this manual operation 
should be solved with a simple copy/paste of the pathname into the 
console window.



