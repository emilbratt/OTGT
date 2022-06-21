#!/usr/bin/env python3

# from CloudHandle import Upload
import Environment
import CloudHandle
import DatabaseHandle

def main():

    cloud = CloudHandle.Download()
    cloud = CloudHandle.Upload()

    conf = Environment.database_retail()
    retailhandle = DatabaseHandle.Retail(conf)
    conf = Environment.database_datawarehouse()
    datawarehousehandle = DatabaseHandle.Datawarehouse(conf)


if __name__ == '__main__':
    main()
