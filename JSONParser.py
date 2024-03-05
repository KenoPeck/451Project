import json


def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ")

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute,value))
    return L

def parseBusinessLine(data):
    return \
        "'" + cleanStr4SQL(data['name']) + "'," + \
        "'" + cleanStr4SQL(data['address']) + "'," + \
        "'" + cleanStr4SQL(data['city']) + "'," +  \
        "'" + data['state'] + "'," + \
        "'" + data['postal_code'] + "'," +  \
        str(data['latitude']) + "," +  \
        str(data['longitude']) + "," + \
        str(data['stars']) + "," + \
        str(data['review_count']) + "," + \
        str(data['is_open'])

def parseBusinessJson(jsonFile, outfile):
    line = jsonFile.readline()

    while line:
        data = json.loads(line)
        
        business_str =  parseBusinessLine(data)
        outfile.write(business_str + '\n')

        #business id
        business = data['business_id']

        #get categories
        for category in data['categories']:
            category_str = "'" + business + "','" + category + "'"
            outfile.write(category_str + '\n')

        #get hours
        for (day,hours) in data['hours'].items():
            hours_str = "'" + business + "','" + str(day) + "','" + str(hours.split('-')[0]) + "','" + str(hours.split('-')[1]) + "'"
            outfile.write( hours_str +'\n')

        #get attributes
        for (attr,value) in getAttributes(data['attributes']):
            attr_str = "'" + business + "','" + str(attr) + "','" + str(value)  + "'"
            outfile.write(attr_str +'\n')

        line = jsonFile.readline()

def parseReviewLine(data):
    return \
        "'" + data['review_id'] + "'," +  \
        "'" + data['user_id'] + "'," + \
        "'" + data['business_id'] + "'," + \
        str(data['stars']) + "," + \
        "'" + data['date'] + "'," + \
        "'" + cleanStr4SQL(data['text']) + "'," +  \
        str(data['useful']) + "," +  \
        str(data['funny']) + "," + \
        str(data['cool'])

def parseReviewJson(jsonFile, outfile):
    line = jsonFile.readline()
    while line:
        data = json.loads(line)
        review_str = parseReviewLine(data)
        outfile.write(review_str +'\n')
        line = jsonFile.readline()

#parse top level json data of single user
def parseUserLine(data):
    return \
        "'" + data['user_id'] + "'," + \
        "'" + cleanStr4SQL(data["name"]) + "'," + \
        "'" + cleanStr4SQL(data["yelping_since"]) + "'," + \
        str(data["review_count"]) + "," + \
        str(data["fans"]) + "," + \
        str(data["average_stars"]) + "," + \
        str(data["funny"]) + "," + \
        str(data["useful"]) + "," + \
        str(data["cool"])
        
def parseUserJson(jsonFile, outfile):
    line = jsonFile.readline()
    while line:
        data = json.loads(line)
        
        user_str = parseUserLine(data)
        outfile.write(user_str+"\n")

        user_id = data["user_id"]
        for friend in data["friends"]:
            friend_str = "'" + user_id + "','" + friend + "'" + "\n"
            outfile.write(friend_str)
        line = jsonFile.readline()
    
def parseCheckinJson(jsonFile, outfile):
    line = jsonFile.readline()

    while line:
        data = json.loads(line)
        business_id = data['business_id']
        for (dayofweek,time) in data['time'].items():
            for (hour,count) in time.items():
                checkin_str = "'" + business_id + "',"  \
                                "'" + dayofweek + "'," + \
                                "'" + hour + "'," + \
                                str(count)
                outfile.write(checkin_str + "\n")
        line = jsonFile.readline()

def parseJsonData(filename, dataType):
    jsonFile = open(filename,"r")
    outfile =  open(filename + ".txt", "w")
    print("parsing " + dataType)

    match dataType:
        case "business":
            parseBusinessJson(jsonFile, outfile)

        case "user":
            parseUserJson(jsonFile, outfile)

        case "review":
            parseReviewJson(jsonFile, outfile)

        case "checkin":
            parseCheckinJson(jsonFile, outfile)

        case _:
            print("unknown data type")

    outfile.close()
    jsonFile.close()


parseJsonData(".//yelp_user.JSON", "user")
parseJsonData(".//yelp_business.JSON", "business")
parseJsonData(".//yelp_checkin.JSON", "checkin")
parseJsonData(".//yelp_review.JSON", "review")


