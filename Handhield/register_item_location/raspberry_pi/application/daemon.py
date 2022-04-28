#!/usr/bin/env python3
from time import sleep

import Database
import API


def handle_failed_jobs():
    '''
        all jobs where status = 2 and at least 1 week old will be included
        and if still failed, will be deleted forever
    '''
    api = API.Connect()
    jobs = Database.SelectFailedJobs()
    for job in jobs:
        job_id = job[0]
        reg_time = job[1]
        item = job[2]
        shelf = job[3]
        api.get_article_id(item)
        if api.status_code == 200: # article id found = valid barcode
            data = {'article_id': api.body['articleid'], 'shelf': shelf}
            api.post_placement(data)
            if api.status_code == 201: # placement was updated
                print(reg_time + ' PLACEMENT ' + str(item) + ' and shelf ' + shelf +  ' OK')
                Database.DeleteJob(job_id)
            else: # unsuccessful on 2nd try,, so we delete job
                print(reg_time + ' PLACEMENT ' + str(item) + ' and shelf ' + shelf +  ' ERROR')
                print('DELETE job for item ' + str(item))
                Database.DeleteJob(job_id)
        else: # no article id found and since this is 2nd try, delete job
            print('DELETE job for item ' + str(item))
            Database.DeleteJob(job_id)


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
            data = {'article_id': api.body['articleid'], 'shelf': shelf}
            api.post_placement(data)
            if api.status_code == 201: # placement was updated
                print(reg_time + ' PLACEMENT ' + str(item) + ' and shelf ' + shelf +  ' OK')
                Database.DeleteJob(job_id)
            elif api.status_code == 502: # valid barcode but error on update placement
                print(reg_time + ' PLACEMENT ' + str(item) + ' and shelf ' + shelf + ' ERROR')
                Database.DeleteJob(job_id)
            else: # unexpected, so we keep the job
                Database.UpdateJobFail(job_id)
        else: # article id not found = invalid barcode or connection error (this job should be re-tried)
            print(reg_time + ' PLACEMENT ' + str(item) + ' and shelf ' + shelf + ' FAIL')
            Database.UpdateJobFail(job_id)

def mainloop():
    Database.StartDatabase() # will force create db and table if not exists
    handle_failed_jobs()
    while True:
        handle_new_jobs()
        sleep(1)


if __name__ == '__main__':
    mainloop()
