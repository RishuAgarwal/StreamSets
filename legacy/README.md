This script deletes Jobs from StreamSets Control Hub 3.x older than a configurable number of days before now.
Jobs must have INACTIVE status to be processed, and must have been run at least once.

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

 - Set the variable DRY_RUN = True
   - to list the Jobs identified for deletion without deleting any Jobs

 - Set the variable DRY_RUN = False
   - to list the Jobs identified for deletion and to delete the Jobs

 - Set the variable NUM_DAYS to the number of days to consider a Job old

 - Not Required: Set the variable LABEL to define job Data Collector Label used to mark old jobs for deletion or leave it BLANK.

Usage Instructions:

Run the script with the variable DRY_RUN = True to print a list of Jobs that are marked for deletion.

After running a DRY_RUN, inspect the list of Jobs identified for deletion.

If all goes well, then run the script again with DRY_RUN = False to delete the Jobs
