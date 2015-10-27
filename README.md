ftp_to_str
==========
###### _A small Python module to retrive a text file with FTP and convert the data to a string_

Requirements
============
Nothing outside the Python 2.6 standard library

Usage example
=============
```python
from ftp_to_str import ftp_to_str

job_status = ftp_to_str(host='some.ftp.host', file_path='batch_job.log')

if 'Program was executed successfully' in job_status:
    print 'Job status is OK'
    exit(0)
    
else:
    print 'Job status is NOT OK'
    exit(1)
```
