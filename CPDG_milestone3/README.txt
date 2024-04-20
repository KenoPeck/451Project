Instructions to start application:

1. Open windows command prompt and enter:
psql -h localhost -p 5432 -U postgres

2. then enter:
CREATE DATABASE milestone3db;

3. place zipData.sql file and Yelp-CptS451 folder in same directory as JSONParser.py

4. then run:
JSONParser.py

5. once JSONParser.py finishes run:
UserInterface.py