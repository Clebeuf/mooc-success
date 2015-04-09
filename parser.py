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

    counter = 0;

    
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

            if 'other' not in str.lower(record['final_cc_cname_DI']):
                filteredRecords.append(record)

            counter = counter + 1

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
# Development index
#----------------------------------------------------------------------------------------------
def addDevelopment(data):
    countries = []
    newData = []

    for line in data:

        # if line['final_cc_cname_DI'] not in countries:
        #     countries.append(line['final_cc_cname_DI'])

        if line['final_cc_cname_DI'] == 'United States':
            line['HDI'] = 0.914
        elif line['final_cc_cname_DI'] == 'Brazil':
            line['HDI'] = 0.744
        elif line['final_cc_cname_DI'] == 'Canada':
            line['HDI'] = 0.902
        elif line['final_cc_cname_DI'] == 'United Kingdom':
            line['HDI'] = 0.892
        elif line['final_cc_cname_DI'] == 'India':
            line['HDI'] = 0.586
        elif line['final_cc_cname_DI'] == 'Portugal':
            line['HDI'] = 0.822
        elif line['final_cc_cname_DI'] == 'Poland':
            line['HDI'] = 0.834
        elif line['final_cc_cname_DI'] == 'Australia':
            line['HDI'] = 0.933
        elif line['final_cc_cname_DI'] == 'Spain':
            line['HDI'] = 0.869
        elif line['final_cc_cname_DI'] == 'Germany':
            line['HDI'] = 0.911
        elif line['final_cc_cname_DI'] == 'Ukraine':
            line['HDI'] = 0.734
        elif line['final_cc_cname_DI'] == 'Russian Federation':
            line['HDI'] = 0.778
        elif line['final_cc_cname_DI'] == 'Indonesia':
            line['HDI'] = 0.684
        elif line['final_cc_cname_DI'] == 'Egypt':
            line['HDI'] = 0.682
        elif line['final_cc_cname_DI'] == 'China':
            line['HDI'] = 0.719
        elif line['final_cc_cname_DI'] == 'Philippines':
            line['HDI'] = 0.660
        elif line['final_cc_cname_DI'] == 'Pakistan':
            line['HDI'] = 0.537
        elif line['final_cc_cname_DI'] == 'Mexico':
            line['HDI'] = 0.756
        elif line['final_cc_cname_DI'] == 'Bangladesh':
            line['HDI'] = 0.558
        elif line['final_cc_cname_DI'] == 'Nigeria':
            line['HDI'] = 0.558
        elif line['final_cc_cname_DI'] == 'Japan':
            line['HDI'] = 0.890
        elif line['final_cc_cname_DI'] == 'Greece':
            line['HDI'] = 0.853
        elif line['final_cc_cname_DI'] == 'Colombia':
            line['HDI'] = 0.711
        elif line['final_cc_cname_DI'] == 'France':
            line['HDI'] = 0.884
        elif line['final_cc_cname_DI'] == 'Morocco':
            line['HDI'] = 0.617
        else:
            print "error with country"

    return data


#----------------------------------------------------------------------------------------------
# Divide on explored
#----------------------------------------------------------------------------------------------
def exploredFilter(records):

    explored = []

    x = 0

    for record in records:
        if record['explored'] == 0:
            pass
            # temp = json.dumps(record)
            # temp = temp + ","
        else:
            explored.append(record)

    return explored

#----------------------------------------------------------------------------------------------
# main
#----------------------------------------------------------------------------------------------
def main():
    rawData = open(sys.argv[1])
    
    records = createArray(rawData)
    
    formattedRecords = formatRecords(records)
    
    filteredRecords = filterRecords(formattedRecords)
    
    # explored = exploredFilter(filteredRecords)

    finalData = addDevelopment(filteredRecords)

    print json.dumps(finalData)


if __name__ == '__main__':
    main()
