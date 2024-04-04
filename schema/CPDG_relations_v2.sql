CREATE TABLE zipcodeData (
    zipcode varchar(5),
    medianIncome int,
    meanIncome int,
    population int,
    Primary Key (zipcode)
);

CREATE TABLE business (
    businessId char(22),
    name varchar(100),
    neighborhood varchar(30),
    address varchar(200),
    city varchar(20),
    state varchar(20),
    zipcode varchar(5) NOT NULL,
    latitude varchar(15),
    longitude varchar(15),
    stars decimal(2,1),
    review_count int,
    openStatus boolean,
    reviewrating decimal(2,1),
    numCheckins int,
    FOREIGN KEY (zipcode) REFERENCES zipcodeData(zipcode),
    Primary Key (businessId)
);

CREATE TABLE BusinessAttribute (
    businessId char(22),
    name VARCHAR(64),
    value VARCHAR(64),
    FOREIGN KEY (businessId) REFERENCES business(businessId),
    Primary Key (businessId, name)
);

CREATE TABLE BusinessCategory (
    businessId char(22),
    category VARCHAR(64),
    FOREIGN KEY (businessId) REFERENCES business(businessId),
    Primary Key (businessId, category)
);

CREATE TABLE BusinessHours (
    businessId char(22),
    day VARCHAR(10),
    openTime TIME,
    closeTime TIME,
    FOREIGN KEY (businessId) REFERENCES business(businessId),
    Primary Key (businessId, day)
);

CREATE TABLE yelpuser (
    userId char(22) primary key,
    name varchar(20)
);

CREATE TABLE rating (
    reviewId char(22),
    userId char(22) NOT NULL,
    businessId char(22) NOT NULL,
    stars int,
    date DATE,
    text varchar(1500),
    useful_vote int,
    funny_vote int,
    cool_vote int,
    FOREIGN KEY (businessId) REFERENCES business(businessId),
    Primary Key (reviewId)
);

CREATE TABLE checkin (
    businessId char(22),
    day varchar(9),
    hour TIME,
    count int,
    Primary Key (businessId, day, hour),
    FOREIGN KEY (businessId) REFERENCES business(businessId)
);