#!/usr/bin/env python3

# from CloudHandle import Upload
import Environment
import CloudHandle
import DatabaseHandle

def main():
    print(Environment.get('cloudstorage', 'host'))
    print(Environment.get('cloudstorage', 'user_autoreport'))
    cloud = CloudHandle.Download()
    cloud = CloudHandle.Upload()
    retailhandle = DatabaseHandle.Retail()
    datawarehousehandle = DatabaseHandle.Datawarehouse()


if __name__ == '__main__':
    main()
