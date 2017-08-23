"""webScrapeDEM.py

DESCRIPTION:
------------
    This is a tutorial from www.blog.pythonlibrary.org, from the blog
    Mouse vs. Python, titled, "Python 101: How to Download a File".

    There is information for both Python 2 and Python 3...there for different
    packages that work best for each version of Python.

SOURCES:
--------
    This code has been modified significantly from various other sources, and
    many online documentation links were used.

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

AUTHOR:
-------

    Nicholas P. Taliceo
    Em. Nicholas.Taliceo@utdallas.edu   Web. www.NicholasTaliceo.com

18 December 2016
"""

import arcpy
import os
import urllib.request
# Needs to be downloaded manually.  See the Beautiful Soup docs (above).
import bs4
import requests
import zipfile

folder = input("Please your working directory: ")
print("The folder location has been set!" + "\n")
arcpy.env.workspace = folder
os.chdir(folder)

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
print("\n" + "Finding downloadable files...")
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

print("\n" + "Files have successfully finished downloading!  Congratulations!")