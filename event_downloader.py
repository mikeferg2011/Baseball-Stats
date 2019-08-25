import urllib.request
import os
import zipfile

# How to map different columns and options
# https://www.pitchbypitch.com/tag/bevent/

decades = list(range(1910,2020,10))
#decades = list(range(1910,1920,10))
user_dir = "D:/GitHub/Baseball-Stats/event_files/"

os.chdir(user_dir)

for i in decades:
    print(i)
    url = "https://www.retrosheet.org/events/"+ str(i) +"seve.zip"
    file_name = user_dir+str(i)+"seve.zip"
    urllib.request.urlretrieve(url, file_name)
    
    zip_ref = zipfile.ZipFile(file_name) # create zipfile object
    zip_ref.extractall(user_dir) # extract file to dir
    zip_ref.close() # close file
    os.remove(file_name) # delete zipped file
