import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute,value))
    return L

def int2BoolStr (value):
    if value == 0:
        return 'false'
    else:
        return 'true'

def parseBusinessLine(data):
    return \
        "INSERT INTO business (businessId, name, neighborhood, address, city, state, zipcode, latitude, longitude, stars, review_count, openStatus, reviewrating, numCheckins) " + \
        "VALUES (" +  \
        "'" + data['business_id'] + "'," +  \
        "'" + cleanStr4SQL(data['name']) + "'," + \
	    "'" + cleanStr4SQL(data['neighborhood']) + "'," + \
        "'" + cleanStr4SQL(data['address']) + "'," + \
        "'" + cleanStr4SQL(data['city']) + "'," +  \
        "'" + data['state'] + "'," + \
        "'" + data['postal_code'] + "'," +  \
        str(data['latitude']) + "," +  \
        str(data['longitude']) + "," + \
        str(data['stars']) + "," + \
        str(data['review_count']) + "," + \
        int2BoolStr(data['is_open']) + "," + \
        " 0.0 , 0);"

def parseBusinessJson(jsonFile, cur, conn):
    line = jsonFile.readline()

    while line:
        data = json.loads(line)
        
        #inserting business data
        business_str =  parseBusinessLine(data)
        #try:
        cur.execute(business_str)
        # except:
        #     print("error inserting business data")
        #     print(business_str)
        #     quit()

        #business id
        business = data['business_id']

        #get categories
        try:
            for category in data['categories']:
                category_str = "INSERT INTO BusinessCategory (businessId, category) VALUES ('" + business + "','" + cleanStr4SQL(category) + "');"
                cur.execute(category_str) #inserting each category
        except:
            print("error inserting business categories")
            print(data['categories'])
            print(category_str)
            quit()
        

        #get hours
        try:
            for (day,hours) in data['hours'].items():
                hours_str = "INSERT INTO BusinessHours (businessId, day, openTime, closeTime) VALUES ('" + business + "','" + str(day) + "'," + "TO_TIMESTAMP('" + str(hours.split('-')[0]) + "', 'HH24:MI')::TIME" + ", " + "TO_TIMESTAMP('" + str(hours.split('-')[1]) + "', 'HH24:MI')::TIME" + ");"
                cur.execute(hours_str) #inserting hours of operation
        except:
            print("error inserting business hours")
            print(data['hours'].items())
            print(hours_str)
            quit()

        #get attributes
        #try:
        for (attr,value) in data['attributes'].items():
            if isinstance(value, bool):
                value = str(value).lower()
                attr_str = "INSERT INTO BusinessAttribute (businessId, name, value) VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(attr) + "','" + cleanStr4SQL(value) + "');"
                cur.execute(attr_str)
            elif isinstance(value, dict):
                for (subattr,subvalue) in value.items():
                    subvalue = str(subvalue).lower()
                    attr_str = "INSERT INTO BusinessAttribute (businessId, name, value) VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(attr + "_" + subattr) + "','" + cleanStr4SQL(subvalue) + "');"
                    cur.execute(attr_str)
            elif isinstance(value, str):
                attr_str = "INSERT INTO BusinessAttribute (businessId, name, value) VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(attr) + "','" + cleanStr4SQL(value) + "');"
                cur.execute(attr_str)
            elif isinstance(value, int):
                attr_str = "INSERT INTO BusinessAttribute (businessId, name, value) VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(attr) + "','" + str(value) + "');"
                cur.execute(attr_str)
        # except:
        #     print("error inserting business attributes")
        #     print(data['attributes'])
        #     print(attr_str)
        #     quit()
        conn.commit()
        

        line = jsonFile.readline()

def parseReviewLine(data):
    return \
        "'" + data['review_id'] + "'," +  \
        "'" + data['user_id'] + "'," + \
        "'" + data['business_id'] + "'," + \
        str(data['stars']) + "," + \
        "'" + data['date'] + "'," + \
        "'" + cleanStr4SQL(data['text']) + "" + "'," +  \
        str(data['useful']) + "," +  \
        str(data['funny']) + "," + \
        str(data['cool'])

def parseReviewJson(jsonFile, cur, conn):
    line = jsonFile.readline()
    while line:
        data = json.loads(line)
        review_str = parseReviewLine(data)
        #try:
        cur.execute("INSERT INTO rating (reviewId, userId, businessId, stars, date, text, useful_vote, funny_vote, cool_vote) VALUES (" + review_str + ");")
        # except:
        #     print("error inserting review data")
        #     print(review_str)
        #     quit()
        line = jsonFile.readline()
    conn.commit()
    
def parseCheckinJson(jsonFile, cur, conn):
    line = jsonFile.readline()

    while line:
        data = json.loads(line)
        business_id = data['business_id']
        for (dayofweek,time) in data['time'].items():
            for (hour,count) in time.items():
                checkin_str = "'" + business_id + "',"  \
                                "'" + str(dayofweek) + "'," + \
                                "TO_TIMESTAMP('" + str(hour) + "', 'HH24:MI')::TIME" + "," + \
                                str(count)
                try:
                    cur.execute("INSERT INTO checkin (businessId, day, hour, count) VALUES (" + checkin_str + ");")
                except:
                    print("error inserting checkin data")
                    print(checkin_str)
                    quit()
        conn.commit()
        line = jsonFile.readline()

def parseJsonData(filename, dataType, conn):
    jsonFile = open(filename,"r")
    print("parsing " + dataType)
    cur = conn.cursor()

    match dataType:
        case "business":
            parseBusinessJson(jsonFile, cur, conn)

        case "review":
            parseReviewJson(jsonFile, cur, conn)

        case "checkin":
            parseCheckinJson(jsonFile, cur, conn)

        case _:
            print("unknown data type")

    cur.close()
    jsonFile.close()

#load sql files
sqlFile = open("./zipData.sql","r")
zipcodeDataSQL = sqlFile.read()
sqlFile.close()

sqlFile = open("./CPDG_relations_v2.sql","r")
sqlDDL = sqlFile.read()
sqlFile.close()

sqlFile = open("./CPDG_UPDATE.sql","r")
sqlUpdate = sqlFile.read()
sqlFile.close()

#connect to database
password = input("Enter postgres password:")
try:
    conn = psycopg2.connect(f"dbname='milestone3db' user='postgres' host='localhost' password={password}")
except:
    print('Unable to connect to the database!')
    exit()

#create tables
cur = conn.cursor()
cur.execute(sqlDDL)
conn.commit()

#fill tables
cur.execute(zipcodeDataSQL)
conn.commit()
parseJsonData("./Yelp-CptS451/yelp_business.JSON", "business", conn)
parseJsonData("./Yelp-CptS451/yelp_checkin.JSON", "checkin", conn)
parseJsonData("./Yelp-CptS451/yelp_review.JSON", "review", conn)

#update tables
cur.execute(sqlUpdate)
conn.commit()
cur.close()
conn.close()