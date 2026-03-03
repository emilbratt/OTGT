* this directory contians all services that exposes an http server

* they communicate with each other via rest api

* they are also available from external sources

### directory overview

```
OTGT/Datawarehouse/server/
  |
  ├── barcode_generator/ -> request barcodes and QR-codes from JSON data
  |
  ├── cip_info/ -> inventory information and placements
  |
  ├── cip_co/ -> create and handle customer orders
  |
  └── spreadsheet_generator/ -> request .xlsx spreadsheet from JSON data
```
