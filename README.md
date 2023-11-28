# AuditCommitteeMembers
 _Details of all FTSE 350 Audit Committee Members at a given date_

 This Python script leverages the **London Stock Exchange** [Refinitiv Data API](https://github.com/LSEG-API-Samples/Example.DataLibrary.Python) to retrieve key information for all the FTSE 350 companies Audit Committee members at a given date.
 The results are saved in a csv file, please check the [output](https://github.com/tonyfregoli/AuditCommiteeMembers/blob/main/Example%20Output/ftse350_20230911_audit_officers.csv) in the Example folder.

## Requirements 
- **A LSEG Refinitiv Data API Key is necessary to run this script**. Please be aware that the Refinitiv Data Platform and the Refinitiv Data API are paid products.
- Install the Refinitiv package and pandas
```shell
pip install refinitiv.data
pip install pandas
```
 ## Script execution

 From your python shell invoke the script includeing the date on which the snapshot of the committee members is required in the format `yyyymmdd`, for instance:
 ```shell
python ftse350_auditmembers.py 20231127
```

## Output

The output is a CSV file with the following fields:
- Instrument
- Committee Name
- Committee Position of the Director
- Committee Start Date
- LEI
- Company Name
- Officer Rank
- Officer Full Name
- Officer First Name
- Officer Middle Name
- Officer Last Name
- Officer Start Date
- Director Start Date
- Position Start Date
- Position Description


 
