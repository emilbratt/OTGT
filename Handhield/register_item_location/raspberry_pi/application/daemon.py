#!/usr/bin/env python3

import sys
from time import sleep

import Database
import API


def handle_failed_jobs():
    '''
        all jobs where status = 2 and at least 1 week old will be included
        and if http OK and still failed, will be deleted forever
    '''
    api = API.Connect()
    jobs = Database.SelectFailedJobs()
    for job in jobs:
        job_id = job[0]
        reg_time = job[1]
        item = job[2]
        shelf = job[3]
        api.get_article_id(item)
        if api.status_code == 200: # HTTP OK and article id found = valid barcode
            article_id = api.body['articleid']
            data = {'article_id': article_id, 'shelf': shelf}
            api.post_placement(data)
            if api.status_code == 201: # placement was updated
                print(reg_time + ' UPDATE PLACEMENT ' + str(item) + ' and shelf ' + shelf +  ' HTTP 201 OK')
                Database.DeleteJob(job_id)
            else: # unsuccessful on 2nd try,, so we delete job
                print(reg_time + ' UPDATE PLACEMENT ' + str(item) + ' and shelf ' + shelf +  ' HTTP ' + str(api.status_code) + ' FAIL')
                print('DELETE job for item ' + str(item))
                Database.DeleteJob(job_id)
        elif api.status_code == 404: # HTTP OK no article id found and since this is 2nd try, delete job
            print('DELETE job for item ' + str(item))
            Database.DeleteJob(job_id)
        else:
            print('NO CONTACT WITH API, SKIP DELETING JOB ' + str(item))


def handle_new_jobs():
    '''
        all jobs where status = 0 will be included
    '''
    api = API.Connect()
    jobs = Database.SelectNewJobs()
    for job in jobs:
        job_id = job[0]
        reg_time = job[1]
        item = job[2]
        shelf = job[3]
        api.get_article_id(item)
        if api.status_code == 200: # article id found = valid barcode
            article_id = api.body['articleid']
            data = {'article_id': article_id, 'shelf': shelf}
            api.post_placement(data)
            if api.status_code == 201: # placement was updated, we can delete job
                print(reg_time + ' UPDATE PLACEMENT ' + str(item) + ' and shelf ' + shelf +  ' HTTP 201 OK')
                print('DELETE job for item ' + str(item))
                Database.DeleteJob(job_id)
            elif api.status_code == 502: # valid barcode but error on update placement
                print(reg_time + ' UPDATE PLACEMENT ' + str(item) + ' and shelf ' + shelf + ' HTTP 502 FAIL')
                Database.UpdateJobFail(job_id)
            else: # unexpected, so we keep the job
                Database.UpdateJobFail(job_id)
        elif api.status_code == 404: # internal server errer most likely due to invalid EAN
            print(reg_time + ' GET ARTICLE ID ' + str(item) + ' and shelf ' + shelf + ' HTTP 404 NOT FOUND')
            Database.UpdateJobFail(job_id)
        elif api.status_code == 500: # internal server errer most likely due to invalid EAN
            print(reg_time + ' GET ARTICLE ID ' + str(item) + ' and shelf ' + shelf + ' HTTP 500 INTERNAL ERROR')
            Database.UpdateJobFail(job_id)
        else: # article id not found = invalid barcode or connection error (this job should be re-tried)
            print(reg_time + ' GET ARTICLE ID ' + str(item) + ' and shelf ' + shelf + ' HTTP ERROR')
            Database.UpdateJobFail(job_id)


def mainloop():
    Database.StartDatabase() # will force create db and table if not exists
    handle_failed_jobs()
    while True:
        handle_new_jobs()
        sys.stdout.flush()
        sleep(1)


if __name__ == '__main__':
    mainloop()
