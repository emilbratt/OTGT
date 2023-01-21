* this directory contians all services that exposes an http server

* they communicate with each other via rest api

* they are also available from external sources

### directory overview

```
OTGT/Datawarehouse/server/
  |
  ├── barcode_generator/ -> request barcodes and QR-codes from JSON data
  |
  ├── cip_info/ -> main web-ui for interacting with all services
  |
  └── spreadsheet_generator/ -> request .xlsx spreadsheet from JSON data
```
