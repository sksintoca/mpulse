The requested web api server code is attached.
There is a setup.sh script to setup the project and install python requirements.
The web server is set to run at localhost:5000

I implemneted the requested apis for:

The applications should have end points to do the following:
1. get all members for a given account
2. get member by:
    - id
    - phone_number
    - client_member_id  (this is equivalent to a medical record number, or mrn)
3. create new member

Also implemented an upload api and there is a uploadfile.sh for testing
there is also a cleardb.sh to delete all rows for testing purposes.

For the extra question part of the handling duplicate entries is accomplished by 
setting the phone_number and client_member_id fields as UNIQUE then catching the exception
when those rows are trying to be inserted. To properly handle those I would want to log 
the attempts in a database so they can be tracked.

To handle the batch processing of large files I would spin off a background task, 
using Celery and do the importing there.

I have included a few .sh scripts to help with setup and testing. 
There are always further improvements to be made.

I appreciate the opportunity 
Steve