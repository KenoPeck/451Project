CREATE TABLE zipcode (
    zipcodeNumber varchar(5),
    avgIncome int,
    medianIncome int,
    population int,
    Primary Key (zipcodeNumber)
);

CREATE TABLE business (
    businessId char(22),
    name varchar(20),
    state varchar(20),
    city varchar(20),
    zipcode varchar(5) NOT NULL,
    FOREIGN KEY (zipcode) REFERENCES zipcode(zipcodeNumber),
    Primary Key (businessId)
);

CREATE TABLE yelpuser (
    userId char(22) primary key,
    name varchar(20)
);

CREATE TABLE rating (
    reviewId char(22),
    stars int,
    text varchar(1500),
    businessId char(22) NOT NULL,
    userId char(22) NOT NULL,
    FOREIGN KEY (businessId) REFERENCES business(businessId),
    FOREIGN KEY (userId) REFERENCES yelpuser(userId),
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