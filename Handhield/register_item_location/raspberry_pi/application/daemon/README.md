This app is an service that repeatedly checks for new barcodes and shelf-values
that the interface has stored and then uploads them to the api

It´s main purpose is to bring the values to the datawarehouse
database using the api found in cip_info and remove values where
either a successful upload was present or where X amount of tries
has lead to no successful uploads 
