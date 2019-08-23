#create a subset of data to work with
#select 10 buisnesses with over 500 reviews for test purposes
#select 500 reviews per business
#create two new respective json files with the subset of data

import json


def creat_Rev_File(rev_Path,max_Review,bus_Id):
    with open(rev_Path, encoding="utf8") as rp:
        foundCount=0
        line = rp.readline()
        while line and foundCount<max_Review:
                datastore = json.loads(line)
                if(datastore["business_id"]==bus_Id):
                    #print(line)
                    try:
                        fr.write(line)
                    except:
                        foundCount=foundCount-1
                        pass
                    foundCount=foundCount+1

                line = rp.readline()

        
#sets the file paths/names for the main data sets
bus_Path = "yelp_academic_dataset_business.json" 
rev_Path = "yelp_academic_dataset_review.json"

#set number of businesses needed
num_bus=10
#set number of reviews per business needed
num_rev=500


fb= open("business_Subset.json","w+")
fr= open("review_Subset.json","w+")

with open(bus_Path, encoding="utf8") as fp:
    foundCount=0
    line = fp.readline()
    while line and foundCount<num_bus:
        datastore = json.loads(line)
        
        if(datastore["review_count"]>num_rev):
            print("run"+str(foundCount))
            creat_Rev_File(rev_Path,num_rev,datastore["business_id"])
            fb.write(line)
            print("Done"+str(foundCount))

            foundCount=foundCount+1
        
        line = fp.readline()

fr.close()
fb.close()


