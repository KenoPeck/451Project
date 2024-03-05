CREATE TABLE business (
name VARCHAR(100),
state CHAR(2),
city VARCHAR(50),
PRIMARY KEY (name,state,city)
);

\copy business (name,state,city) FROM 'C:\Users\kenop\Documents\CS\451\milestone1DB.csv' DELIMITER ',' CSV