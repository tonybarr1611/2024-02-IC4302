CREATE TABLE STATUS (
    statusId INT PRIMARY KEY,
    status VARCHAR(255)
);

CREATE TABLE CIRCUIT (
    circuitId INT PRIMARY KEY,
    circuitRef VARCHAR(255),
    name VARCHAR(255),
    location VARCHAR(255),
    country VARCHAR(255),
    lat FLOAT,
    lng FLOAT,
    alt INT,
    url VARCHAR(255)
);

CREATE TABLE CONSTRUCTOR_RESULT (
    constructorResultId INT PRIMARY KEY,
    raceId INT,
    constructorId INT,
    points INT,
    status VARCHAR(255),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId)
);

CREATE TABLE CONSTRUCTOR_STANDING (
    constructorStandingsId INT PRIMARY KEY,
    raceId INT,
    constructorId INT,
    points INT,
    position INT,
    positionText INT,
    wins INT,
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId)
);

CREATE TABLE CONSTRUCTOR (
    constructorId INT PRIMARY KEY,
    constructorRef VARCHAR(255),
    name VARCHAR(255),
    nationality VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE DRIVER_STANDING (
    driverStandingsId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    points INT,
    position INT,
    positionText INT,
    wins INT,
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId)
);

CREATE TABLE DRIVER (
    driverId INT PRIMARY KEY,
    driverRef VARCHAR(255),
    assignedNumber VARCHAR(255),
    code VARCHAR(255),
    forename VARCHAR(255),
    surname VARCHAR(255),
    dob DATE,
    nationality VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE LAP_TIME (
    raceId INT,
    driverId INT,
    lap INT,
    position INT,
    timeObtained VARCHAR(255),
    milliseconds INT,
    PRIMARY KEY (raceId, driverId, lap),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId)
);

CREATE TABLE PIT_STOP (
    raceId INT,
    driverId INT,
    stop INT,
    lap INT,
    timeObtained VARCHAR(255),
    duration FLOAT,
    milliseconds INT,
    PRIMARY KEY (raceId, driverId, stop),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId)
);

CREATE TABLE QUALIFYING (
    qualifyId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    assignedNumber INT,
    position INT,
    q1 VARCHAR(255),
    q2 VARCHAR(255),
    q3 VARCHAR(255),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId)
);

CREATE TABLE RACE (
    raceId INT PRIMARY KEY,
    year INT,
    round INT,
    circuitId INT,
    name VARCHAR(255),
    calendarDate DATE,
    timeObtained TIME,
    url VARCHAR(255),
    fp1_date DATE,
    fp1_time TIME,
    fp2_date DATE,
    fp2_time TIME,
    fp3_date DATE,
    fp3_time TIME,
    quali_date DATE,
    quali_time TIME,
    sprint_date DATE,
    sprint_time TIME,
    FOREIGN KEY (circuitId) REFERENCES CIRCUIT(circuitId)
);

CREATE TABLE RESULT (
    resultId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    assignedNumber INT,
    grid INT,
    position INT,
    positionText INT,
    positionOrder INT,
    points INT,
    laps INT,
    timeObtained VARCHAR(255),
    milliseconds INT,
    fastestLap INT,
    rank INT,
    fastestLapTime VARCHAR(255),
    fastestLapSpeed FLOAT,
    statusId INT,
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId),
    FOREIGN KEY (statusId) REFERENCES STATUS(statusId)
);

CREATE TABLE SEASON (
    year INT PRIMARY KEY,
    url VARCHAR(255)
);

CREATE TABLE SPRINT_RESULT (
    resultId INT PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId INT,
    assignedNumber INT,
    grid INT,
    position INT,
    positionText INT,
    positionOrder INT,
    points INT,
    laps INT,
    timeObtained VARCHAR(255),
    milliseconds INT,
    fastestLap INT,
    fastestLapTime VARCHAR(255),
    statusId INT,
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId),
    FOREIGN KEY (statusId) REFERENCES STATUS(statusId)
);

LOAD DATA INFILE './data/circuits.csv'
INTO TABLE CIRCUIT
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(circuitId, circuitRef, name, location, country, lat, lng, alt, url);

LOAD DATA INFILE './data/constructor_results.csv'
INTO TABLE CONSTRUCTOR_RESULT
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(constructorResultId, raceId, constructorId, points, status);

LOAD DATA INFILE './data/constructor_standings.csv'
INTO TABLE CONSTRUCTOR_STANDING
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(constructorStandingsId, raceId, constructorId, points, position, positionText, wins);

LOAD DATA INFILE './data/constructors.csv'
INTO TABLE CONSTRUCTOR
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(constructorId, constructorRef, name, nationality, url);

LOAD DATA INFILE './data/driver_standings.csv'
INTO TABLE DRIVER_STANDING
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(driverStandingsId, raceId, driverId, points, position, positionText, wins);

LOAD DATA INFILE './data/drivers.csv'
INTO TABLE DRIVER
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(driverId, driverRef, assignedNumber, code, forename, surname, dob, nationality, url);

LOAD DATA INFILE './data/lap_times.csv'
INTO TABLE LAP_TIME
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(raceId, driverId, lap, position, timeObtained, milliseconds);

LOAD DATA INFILE './data/pit_stops.csv'
INTO TABLE PIT_STOP
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(raceId, driverId, stop, lap, timeObtained, duration, milliseconds);

LOAD DATA INFILE './data/qualifying.csv'
INTO TABLE QUALIFYING
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(qualifyId, raceId, driverId, constructorId, assignedNumber, position, q1, q2, q3);

LOAD DATA INFILE './data/races.csv'
INTO TABLE RACE
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(raceId, year, round, circuitId, name, calendarDate, timeObtained, url, fp1_date, fp1_time, fp2_date, fp2_time, fp3_date, fp3_time, quali_date, quali_time, sprint_date, sprint_time);

LOAD DATA INFILE './data/results.csv'
INTO TABLE RESULT
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(resultId, raceId, driverId, constructorId, assignedNumber, grid, position, positionText, positionOrder, points, laps, timeObtained, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId);

LOAD DATA INFILE './data/seasons.csv'
INTO TABLE SEASON
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(year, url);

LOAD DATA INFILE './data/sprint_results.csv'
INTO TABLE SPRINT_RESULT
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(resultId, raceId, driverId, constructorId, assignedNumber, grid, position, positionText, positionOrder, points, laps, timeObtained, milliseconds, fastestLap, fastestLapTime, statusId);

LOAD DATA INFILE './data/status.csv'
INTO TABLE STATUS
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(statusId, status);
