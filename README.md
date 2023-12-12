# Audit Committee Members
 _Details of all FTSE 350 Audit Committee Members at a given date_

_Audit Committee Members_ leverages the **London Stock Exchange** [Refinitiv Data API](https://github.com/LSEG-API-Samples/Example.DataLibrary.Python) to retrieve key information for all the Audit Committee members of the FTSE 350 companies at a given date.
The results are saved in a csv file, please check the [output](https://github.com/tonyfregoli/AuditCommiteeMembers/blob/main/Example%20Output/ftse350_20230911_audit_officers.csv) in the Example folder.

## Requirements 
- **A LSEG Refinitiv Data API Key is necessary to run this script**. Be aware that the Refinitiv Data Platform and the Refinitiv Data API are paid products.
- Install the Refinitiv package and pandas
  ```shell
  pip install refinitiv.data
  pip install pandas
  ```
- Make sure to have the _Eikon_ Desktop app running in the background   

## Script execution

From your python shell invoke the script including the API key as first argument and the date on which the snapshot of the committee members is required (in the format `yyyymmdd`) as second argument, for instance:
```shell
python ftse350_auditmembers.py abcdefghi123456789 20231127
```

## Output

The output is a CSV file with the following fields:
- Instrument
- Committee Name  
  `Audit only`
- Committee Position of the Director  
  `indicates whether the individual is Chair or Member of the Audit Committee`
- Committee Start Date  
  `when the individual joined the Audit Committee`
- LEI
- Company Name
- Officer Rank
- Officer Full Name
- Officer First Name
- Officer Middle Name
- Officer Last Name
- Officer Start Date
- Director Start Date  
  `when the individual joined the Board for the first time`
- Position Start Date  
  `start date of the role taken by the individual at the snapshot date`   
- Position Description  
  `description of the role taken by the individual at the snapshot date`   


 
