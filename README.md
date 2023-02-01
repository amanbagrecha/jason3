## Download Jason-3 data using python


### Download Jason-3 GPS based orbit and SSHA OGDR
This product is near real time with latency of 5-6 hours with GPS based orbit rather than doris based orbit. It is available through [earthdata](https://cmr.earthdata.nasa.gov/virtual-directory/collections/C2205122298-POCLOUD)

To download,

Run the [jason3_script.py](https://github.com/amanbagrecha/jason3/blob/main/jason3_script.py) with command line options as shown below

```sh
python jason3_script.py --username your_username --password your_password --temporal "2022-01-01T10:00:00Z,2022-01-02T12:00:00Z" --bbox "0,-5,5,0"
```

> **Note**
> Only username and password are mandatory, rest all parameters are set to a default (look in the code to see their value)

To know all the options available
```sh
python jason3_script.py --help
```


Code adapted from [modis-tools](https://github.com/fraymio/modis-tools)


# About Jason-3 Products
Jason-3 has 3 family of products and 8 minor products

3 family of products are
 1. OGDR
 2. IGDR
 3. GDR

Each family has minor products
 - **OGDR** -> OGDR SSHA and native OGDR
 - **IGDR** -> IGDR SSHA and IGDR and S-IGDR
 - **GDR** -> GDR SSHA and GDR and S-GDR

To know more about them refer here

To download these products, we can use FTP server from [NCEI NOAA](https://www.ncei.noaa.gov/data/oceans/jason3/)

> **Note**
> We currently do not have any other way (via https or s3) to download these products. The one available on earthdata is OGDR GPS based product.

Using python, you can download using the jason3_ftp_script.py