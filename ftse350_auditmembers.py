#!/usr/bin/env python 
"""\
ftse350_auditmembers.py
Script Writer: Tony Fregoli
Date: 27/09/2023
Script Purpose: Details of all FTSE 350 Audit Committee Members at a given date 

Usage: python ftse350_auditmembers.py <API_KEY> <date>
Example: python ftse350_auditmembers.py 20230607
"""

from datetime import datetime
import refinitiv.data as rd
import pandas as pd
import json
import time
import sys

#Functions
def getFtse350Officers(ftse):

    print('Building Ftse350 Officer List. Please wait.\n')

    ftse350_officers = '{'

    company_count = 1
    
    for company in ftse.itertuples(index = False, name = None):
        
        company_ric = company[0]
        company_lei = company[1]
        company_name = company[2]
        
        while True:
            try:
                officers = rd.get_data(universe = [company_ric], fields = ['TR.ODOfficerFullName(ODRnk=R1:R1000)',
                                                                           'TR.ODOfficerRank(ODRnk=R1:R1000)',
                                                                           'TR.ODOfficerFirstName(ODRnk=R1:R1000)',
                                                                           'TR.ODOfficerMiddleName(ODRnk=R1:R1000)',
                                                                           'TR.ODOfficerLastName(ODRnk=R1:R1000)',
                                                                           'TR.ODOfficerStartDate(ODRnk=R1:R1000)',
                                                                           'TR.ODDirectorStartDate(ODRnk=R1:R1000)',
                                                                           'TR.ODOfficerPositionStartDate(ODRnk=R1:R1000)',
                                                                           'TR.ODOfficerPositionDesc(ODRnk=R1:R1000)']
                                                                           
                )
                break
            except Exception as error:
                print("API error occurred:", error)
                print("Trying again in 30 seconds.")
                time.sleep(30)
        
        #officers_count = officers[officers.columns[0]].count()
        print(f'[{company_count}/350] - Collecting Officers basic information for {company_name}...')
        
        ftse350_officers = ftse350_officers + f'"{company_name}" : ["{company_ric}", "{company_lei}", ' 
        
        company_officers = '{'
        
        for officer in officers.itertuples(index = False, name = None):
            
            officer_name = officer[1].strip()
            officer_rank = officer[2]
            officer_first_name = officer[3].strip()
            officer_middle_name = officer[4].strip()
            officer_last_name = officer[5].strip()
            officer_start_date = officer[6]
            director_start_date = officer[7]
            position_start_date = officer[8]
            position_description = officer[9].strip()
            
            if officer_name == '':
                continue
            #else:
            #    print(f'Adding: {officer_name}...')

            company_officers = company_officers + f'"{officer_rank}" : ["{officer_name}", "{officer_first_name}", "{officer_middle_name}", "{officer_last_name}", "{officer_start_date}", "{director_start_date}", "{position_start_date}", "{position_description}"], '
            
        company_officers = company_officers[0:-2] + '}'
        
        ftse350_officers = ftse350_officers + company_officers + '], '
        
        company_count +=1
    
    ftse350_officers = ftse350_officers[0:-2] + '}'
    
    temp = open( "ftse350_officers.json", 'w' )
    temp.write(ftse350_officers)
    temp.close()
    
    return eval(ftse350_officers)


def getFtse350OfficersCount(ftse_officers):
    officers_count = 0
    for company in ftse_officers:
        officers_count = officers_count + len(ftse_officers[company][2])
    return officers_count

def getFtse350OfficersCommittees(ftse_officers):
    ftse_officers_count = getFtse350OfficersCount(ftse_officers)
    current_ftse_officer = 1
    
    for company in ftse_officers:
        company_ric = ftse_officers[company][0]
        company_lei = ftse_officers[company][1]
        company_officers = ftse_officers[company][2]
        
        for company_officer_rank, company_officer_details in company_officers.items():
            print(f'[{current_ftse_officer}/{ftse_officers_count}] - Getting Committee data for {company_officer_details[0]} ({company})...')
            
            while True:
                try:
                    company_officer_committee_details = rd.get_data(universe = [company_ric], fields = [f'TR.ODOfficerCommitteeName(ODRnk=R{company_officer_rank})',
                                                                                              f'TR.ODOfficerCommitteePosition(ODRnk=R{company_officer_rank})',
                                                                                              f'TR.ODOfficerCommitteeStartDate(ODRnk=R{company_officer_rank})']
                    )
                    break
                except Exception as error:
                    print("API error occurred:", error)
                    print("Trying again in 30 seconds.")
                    time.sleep(30)

            company_officer_committee_details['LEI'] = company_lei
            company_officer_committee_details['Company Name'] = company
            company_officer_committee_details['Officer Rank'] = company_officer_rank
            company_officer_committee_details['Officer Full Name'] = company_officer_details[0]
            company_officer_committee_details['Officer First Name'] = company_officer_details[1]
            company_officer_committee_details['Officer Middle Name'] = company_officer_details[2]
            company_officer_committee_details['Officer Last Name'] = company_officer_details[3]
            company_officer_committee_details['Officer Start Date'] = company_officer_details[4]
            company_officer_committee_details['Director Start Date'] = company_officer_details[5]
            company_officer_committee_details['Position Start Date'] = company_officer_details[6]
            company_officer_committee_details['Position Description'] = company_officer_details[7]
            
            if 'ftse_officers_committees' in locals():
                ftse_officers_committees = pd.concat([ftse_officers_committees, company_officer_committee_details])
            else:
                ftse_officers_committees = company_officer_committee_details
            
            current_ftse_officer +=1
            
    return ftse_officers_committees           


# Main
if __name__ == "__main__":
    API_KEY = sys.argv[1]
    ftse350_date = sys.argv[2]
 
    session = rd.session.desktop.Definition(app_key = API_KEY).get_session()
    session.open()

    rd.session.set_default(session)

    try:
        ftse350_date = sys.argv[1]
    except:
        #today
        ftse350_date = datetime.today().strftime('%Y%m%d')

    print(f'Retrieving FTSE350 as of {ftse350_date}. Please wait.')
    ftse350 = rd.get_data(universe = [f'0#.FTLC({ftse350_date})'], fields = ['TR.LegalEntityIdentifier', 'TR.CommonName'])

    #ftse350_officers =  json.load(open("ftse350_officers2.json"))
    #ftse350_officers = getFtse350Officers(ftse350.iloc[0:100])
    ftse350_officers = getFtse350Officers(ftse350)
    
    ftse350_officers_committees = getFtse350OfficersCommittees(ftse350_officers)
    ftse350_audit_officers = ftse350_officers_committees.loc[ftse350_officers_committees['Committee Name'] == 'Audit']
    
    print(f'Saving FTSE350 Audit Committee Officers to ftse350_{ftse350_date}_audit_officers.csv.')
    ftse350_audit_officers.to_csv(f'ftse350_{ftse350_date}_audit_officers.csv', index = False)
    