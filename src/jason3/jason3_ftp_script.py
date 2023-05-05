import ftplib

# GUI look at folders in FTP server
# https://www.ncei.noaa.gov/data/oceans/jason3/

# Connect to the FTP server
ftp = ftplib.FTP("ftp-oceans.ncei.noaa.gov")

# Login with a username and password
ftp.login("anonymous", "")

# goto jason3 folder
ftp.cwd("/pub/data.nodc/jason3/")

# list the dirs inside it
print(ftp.dir())

# change working directory to specific cycle of specific product
ftp.cwd("gdr/gdr/cycle000/")

# Open a file for writing
with open("filename_you_want_to_save_with.nc", "wb") as f:
    # Download the file from the FTP server
    ftp.retrbinary(
        "RETR JA3_GPN_2PfP000_117_20160212_011109_20160212_020721.nc", f.write
    )


# Disconnect from the FTP server
ftp.quit()
