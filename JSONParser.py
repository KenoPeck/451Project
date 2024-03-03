
import json

def formatForSQL(str):
    return str.replace("'","''").replace("\n"," ")

def getAttributes(attr):
    attrList = []
    for (attribute, value) in list(attr.items()):
        if isinstance(value, dict):
            attrList += getAttributes(value)
        else:
            attrList.append((attribute,value))
    return attrList

def parseBusinessData():
    print("Parsing Business Data...")
    infile = open('.//yelp_business.JSON','r')
    outfile =  open('.//yelp_business.txt', 'w')
    rawDataLine = infile.readline()
    numLines = 0
    while rawDataLine:
        data = json.loads(rawDataLine)
        business = data['business_id']
        business_str =  "'" + formatForSQL(data['name']) + "','" + formatForSQL(data['address']) + "','" + \
                        formatForSQL(data['city']) + "','" + data['state'] + "','" + data['postal_code'] + "'," +  \
                        str(data['latitude']) + "," + str(data['longitude']) + "," + str(data['stars']) + "," + \
                        str(data['review_count']) + "," + str(data['is_open'])
        outfile.write(business_str + '\n')

        for categ in data['categories']:
            categoryStr = "'" + business + "','" + categ + "'"
            outfile.write(categoryStr + '\n')

        for (day,hours) in data['hours'].items():
            hours_str = "'" + business + "','" + str(day) + "','" + str(hours.split('-')[0]) + "','" + str(hours.split('-')[1]) + "'"
            outfile.write( hours_str +'\n')

        for (attr,value) in getAttributes(data['attributes']):
            attr_str = "'" + business + "','" + str(attr) + "','" + str(value)  + "'"
            outfile.write(attr_str +'\n')

        rawDataLine = infile.readline()
        numLines += 1
    print(numLines)
    outfile.close()
    infile.close()
    
def parseReviewData():
    print("Parsing Review Data...")
    infile = open('.//yelp_review.JSON','r')
    outfile =  open('.//yelp_review.txt', 'w')
    rawDataLine = infile.readline()
    numLines = 0
    while rawDataLine:
        data = json.loads(rawDataLine)
        review_str = "'" + data['review_id'] + "','" + data['user_id'] + "','" + \
                        data['business_id'] + "'," + str(data['stars']) + ",'" + \
                        data['date'] + "','" + formatForSQL(data['text']) + "'," +  \
                        str(data['useful']) + "," + str(data['funny']) + "," + str(data['cool'])
        outfile.write(review_str +'\n')
        rawDataLine = infile.readline()
        numLines +=1
    print(numLines)
    outfile.close()
    infile.close()

def parseUserData():
    print("Parsing User Data...")
    infile = open('.//yelp_user.JSON','r')
    outfile =  open('.//yelp_user.txt', 'w')
    rawDataLine = infile.readline()
    numLines = 0
    while rawDataLine:
        data = json.loads(rawDataLine)
        user_id = data['user_id']
        user_str = "'" + user_id + "','" + formatForSQL(data["name"]) + "','" + \
                    formatForSQL(data["yelping_since"]) + "'," + str(data["review_count"]) + "," + \
                    str(data["fans"]) + "," + str(data["average_stars"]) + "," + str(data["funny"]) + "," + \
                    str(data["useful"]) + "," + str(data["cool"])
        outfile.write(user_str+"\n")

        for friend in data["friends"]:
            friend_str = "'" + user_id + "','" + friend + "'\n"
            outfile.write(friend_str)
        rawDataLine = infile.readline()
        numLines +=1

    print(numLines)
    outfile.close()
    infile.close()

def parseCheckinData():
    print("Parsing Checkin Data...")
    infile = open('.//yelp_checkin.JSON','r')
    outfile = open('yelp_checkin.txt', 'w')
    rawDataLine = infile.readline()
    numLines = 0
    while rawDataLine:
        data = json.loads(rawDataLine)
        business_id = data['business_id']
        for (dayofweek,time) in data['time'].items():
            for (hour,count) in time.items():
                checkin_str = "'" + business_id + "','" + dayofweek + "','" + hour + "'," + str(count)
                outfile.write(checkin_str + "\n")
        rawDataLine = infile.readline()
        numLines +=1
    print(numLines)
    outfile.close()
    infile.close()


parseBusinessData()
parseUserData()
parseCheckinData()
parseReviewData()

