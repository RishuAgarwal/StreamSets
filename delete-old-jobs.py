#!/usr/bin/env python
# coding: utf-8


'''
This script deletes Jobs from StreamSets Control Hub 3.x
older than a configurable number of days before now. Jobs must have
INACTIVE status to be processed, and must have been run at least once.

Note that Control Hub will automatically delete Jobs that have never been run after one year.

Prerequisites:
 - Python 3.6+; Python 3.9+ preferred

 - StreamSets SDK for Python v3.12.1
   See: https://docs.streamsets.com/sdk/latest/installation.html

 - Username and password for a user with Organization Administrator role

 - To avoid including secrets in the script, export these two environment variables
   prior to running the script:
        export USER=<your Org Admin USER ID in the form user@org>
        export PASS=<your PASSWORD>

 - Set the variable DRY_RUN = True to list the Jobs identified for deletion
      without actually deleting any Jobs

 - Set the variable DRY_RUN = False to list the Jobs identified for deletion
      and to actually delete the Jobs

 - Set the variable NUM_DAYS to the number of days to consider a Job old

 - Not Required: Set the variable LABEL to define job Data Collector Label used to mark old jobs
   for deletion or leave it BLANK.

Usage Instructions:

Run the script with the variable DRY_RUN = True to print a list of Jobs that are marked for deletion.

After running a DRY_RUN, inspect the list of Jobs identified for deletion.

If all goes well, then run the script again with DRY_RUN = False to actually delete the Jobs

'''

import os
from time import time
import sys
import datetime
from streamsets.sdk import ControlHub
import warnings

warnings.filterwarnings('ignore')

ControlHub.VERIFY_SSL_CERTIFICATES = False

## User Variables ##################

# DRY_RUN
# Set DRY_RUN = True to list the jobs identified for deletion
# without actually deleting any Jobs 
# Set DRY_RUN = False to delete the Jobs
DRY_RUN = False

# Get user_id from environment
#SCH_USER=os.getenv('USER')
#If USER environment variable is not set, provide the Org Admin USER ID
SCH_USER="<>"

# Get password from the environment
#SCH_PWD=os.getenv('PASS')
#If PASS environment variable is not set, provide the Org Admin USER ID Password
SCH_PWD="<>"

# Control Hub URL, e.g. https://cloud.streamsets.com
SCH_URL="<>"

# Number of days before today to search for jobs to delete
NUM_DAYS = <>

# SDC Label to identify old jobs to delete or leave it BLANK
LABEL = '<>'

## End User Variables ##############

#calculate timestamp for filtering old jobs - now minus NUM_DAYS in ms
now = round(time() * 1000)
num_to_ms = NUM_DAYS * 24 * 60 * 60 * 1000
as_of = now - num_to_ms
dt = datetime.datetime.fromtimestamp(as_of / 1000.0)

try:
    print('Connecting to Control Hub')

    sch = ControlHub(SCH_URL,username=SCH_USER,password=SCH_PWD)

    print('Connected to Control Hub')
    
    # Get jobs for deletion
    print(f'\nRetrieving inactive jobs finished before {dt}\n"')
    jobs = [job for job in sch.jobs if job.history and job.history[0].finishTime < as_of and job.status == 'INACTIVE']
    filtered_jobs = []
    for job in jobs:
        if ((not LABEL) or (LABEL in job.data_collector_labels)):
            filtered_jobs.append(job)
    # Exit if no old Jobs found
    if filtered_jobs is None or len(filtered_jobs) == 0:
        print('Script halted. No old Jobs found\n')
        sys.exit(0)

    # Print list of Jobs marked for deletion
    print(f'\nJobs targeted for deletion:')
    print(60 * '-')
    for job in filtered_jobs:
        last_run_finish_time = datetime.datetime.fromtimestamp(job.history[0].finishTime/1000.0)
        print('Job: \'' + job.job_name + '\'     Last Run: ' + last_run_finish_time.strftime("%Y-%m-%d %H:%M:%S") )
    print(60 * '-')
    print(f'Total Number of Jobs targeted for deletion: {len(filtered_jobs)}')
      
    # If not a DRY_RUN, delete the selected Jobs
    if not DRY_RUN:
        do_it = input('\nDo you want to delete the selected Jobs? (Y/N)?')
        #Delete Jobs
        if do_it == 'Y':
            print('Deleting selected Jobs...')
            for job in filtered_jobs:
                try:
                    print('Deleting Job \'' + job.job_name + '\'')
                    sch.delete_job(job)
                except Exception as e:
                    print(f"An exception occurred while trying to delete the Job {job.job_name}") 
                    print(str(e)) 
                    print('The script will exit without trying to delete any more Jobs')
                    sys.exit(-1)
        else:
            print('\nScript aborted; no Jobs deleted')        
        
except Exception as e:
    print(e)