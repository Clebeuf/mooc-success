#!/usr/bin/python
import sys
import re
import string


#----------------------------------------------------------------------------------------------
# createList(afinnfile)
#   -creates a dictionary of words
#----------------------------------------------------------------------------------------------
def createList(file):
    terms = [] # initialize an empty dictionary
    #creates a dictionary of words and their sentiment values
    for line in file:
        
        line = re.sub(r"\n", "", line)           #remove the newline characters

        terms.append(line.upper())
    
    #returns the dictionary
    return terms



#----------------------------------------------------------------------------------------------
# findEnglishTweets(fp)
#   -parses the tweet file and extracts english tweets
#   -returns a dictionary of english tweets
#----------------------------------------------------------------------------------------------
def divideTweets(tweet_file, male, female):
    tweets = []
    male_tweets = [] # initialize an empty list
    female_tweets = [] # initialize an empty list
    numM = 0
    numF = 0
    
    
    for line in tweet_file:
        temp = line[:]
        if not '\"lang\":\"en\"' in temp:
            #print 'not english:'
            pass
        if '\"lang\":\"en\"' in temp:
            matchobj = re.match(r'(.*)\",\"text\":\"(.*)\",\"source\"', temp)
            if matchobj:
                #print matchobj.group(2)     #prints the tweets
                if (matchobj.group(2)).startswith('\\u'):               # the way I dealt with the strange \u8908 tweets
                    pass
                else:
                    s = matchobj.group(2)
                    
                    #format the tweets - ie. remove irrelavant information
                    s = re.sub(r"http:(\S)*", "", s)    #remove the http://...
                    s = re.sub(r"&\S\S\;", "", s)    #remove the &xx 
                    s = re.sub(r"&\S\S\S\;", "", s)    #remove the &xxx
                    s = re.sub(r"\\u\S\S\S\S", "", s)   #remove the unicode characters
                    s = re.sub(r"\\n", "", s)           #remove the newline characters
                    s = re.sub(r"\\S", "", s)          #remove the \characters
                    s = re.sub(r"\'", "", s)          #remove the \characters
                    s = re.sub(r"\-", "", s)          #remove the \characters
                    
                    
                    
                    words = re.split('[^a-zA-Z\-]',s)
                    words = [value.upper() for value in words if value != '']   # remove the empty words
                    
                    fflag = 0
                    mflag = 0
                    
                    for word in words:
                        if word in male:
                            mflag = 1
                        if word in female:
                            fflag = 1
            
                    if fflag == 1 and mflag == 0:
                        female_tweets.append(words)
                        numF = numF +1
                    elif fflag == 0 and mflag == 1:
                        male_tweets.append(words)
                        numM = numM +1

    return male_tweets, female_tweets





#----------------------------------------------------------------------------------------------
# Create an array of variables for each record
#----------------------------------------------------------------------------------------------
def createArray(rawData):
    newData = []

    for line in rawData:
        temp = line[:]

        #remove the newline characters
        temp = re.sub(r"\r\n", "", temp)

        # Split into variables
        words = re.split('[,]',temp)

        # Remove New Line
        newData.append(words[:])

    print newData
    return newData



#----------------------------------------------------------------------------------------------
# main
#----------------------------------------------------------------------------------------------
def main():
    rawData = open(sys.argv[1])
    fTweets = createArray(rawData)




if __name__ == '__main__':
    main()
