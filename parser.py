#!/usr/bin/python
import sys
import re
import string
import json
from decimal import *

#----------------------------------------------------------------------------------------------
# Create an array of variables for each record
#----------------------------------------------------------------------------------------------
def formatRecords(records):
    formattedRecords = []

    lables = records[0]

    for record in records[1:]:

        d = {}

        for x in range(0, len(record)-1):
            d[lables[x]] = record[x]

        formattedRecords.append(d)

    return formattedRecords


#----------------------------------------------------------------------------------------------
# Create an array of variables for each record
# course_id,userid_DI,viewed,explored,certified,final_cc_cname_DI,LoE_DI,YoB,gender,grade,nevents,ndays_act,nplay_video,nchapters,nforum_posts,incomplete_flag
#----------------------------------------------------------------------------------------------
def filterRecords(records):
    filteredRecords = []

    for record in records:

        # remove incomplete records & convert into proper types
        if record['YoB'].isdigit() and record['grade'].isdigit() and record['ndays_act'].isdigit() and record['nplay_video'].isdigit() and record['nchapters'].isdigit() and record['nforum_posts'].isdigit():
            record['YoB'] = int(record['YoB'])
            record['grade'] = float(record['grade'])
            record['nevents'] = int(record['nevents'])
            record['ndays_act'] = int(record['ndays_act'])
            record['nplay_video'] = int(record['nplay_video'])
            record['nchapters'] = int(record['nchapters'])
            record['nforum_posts'] = int(record['nforum_posts'])

            # If the location is other convert it to unknown
            if 'other' in str.lower(record['final_cc_cname_DI']):
                record['final_cc_cname_DI'] = 'unknown'
            
            # split the course info into the school, year, and course ID
            courseInfo = re.split('[/]',record['course_id'])
            record['school'] = courseInfo[0]
            record['course_id'] = courseInfo[1]
            record['year'] = courseInfo[2]

            # find the year
            courseYear = re.split('[_]',record['year'])
            record['year'] = int(courseYear[0])

            # convert into integer values
            record['viewed'] = int(record['viewed'])
            record['explored'] = int(record['explored'])
            record['certified'] = int(record['certified'])

            filteredRecords.append(record)


    return filteredRecords

#----------------------------------------------------------------------------------------------
# Create an array of variables for each record
#----------------------------------------------------------------------------------------------
def createArray(rawData):
    newData = []

    for line in rawData:
        temp = line[:]

        # split records by \r
        records = re.split('\r',temp)

        for record in records:     

            # Split into variables
            record = re.split('[,]',record)

            # Remove invalid records
            if (record[len(record)-1]) != "1":
                newData.append(record)

    return newData


#----------------------------------------------------------------------------------------------
# main
#----------------------------------------------------------------------------------------------
def main():
    rawData = open(sys.argv[1])
    
    records = createArray(rawData)
    
    formattedRecords = formatRecords(records)
    
    filteredRecords = filterRecords(formattedRecords)
    
    print json.dumps(filteredRecords)


if __name__ == '__main__':
    main()
